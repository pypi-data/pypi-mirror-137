# Copyright 2021 VMware, Inc.
# SPDX-License-Identifier: Apache-2.0
import json
import logging
import queue
import sys
import threading
from collections import defaultdict
from typing import Iterable
from typing import List
from typing import Optional
from typing import Tuple

from vdk.api.job_input import IIngester
from vdk.api.plugin.plugin_input import IIngesterPlugin
from vdk.internal.builtin_plugins.ingestion import ingester_utils
from vdk.internal.builtin_plugins.ingestion.ingester_configuration import (
    IngesterConfiguration,
)
from vdk.internal.builtin_plugins.ingestion.ingester_utils import AtomicCounter
from vdk.internal.core import errors
from vdk.internal.core.errors import PlatformServiceError
from vdk.internal.core.errors import ResolvableBy
from vdk.internal.core.errors import UserCodeError
from vdk.internal.core.errors import VdkConfigurationError

log = logging.getLogger(__name__)


class IngesterBase(IIngester):
    """
    Plugins can subclass this class to provide different ingestion capabilities.
    This can be done by overriding `ingest_payload`, and provide customizations as
    to what data formats can be send, and what methods for sending are to be used.

    Sending internal telemetry for payloads can be facilitated by using `send` to
    send the telemetry payload.

    The thread pools are provided by vdk and can be customized by the plugins.
    """

    def __init__(
        self,
        data_job_name: str,
        op_id: str,
        ingester: IIngesterPlugin,
        ingest_config: IngesterConfiguration,
    ):
        """
        This constructor must be called by inheritors.

        :param data_job_name: string
            Name of the data job.
        :param op_id: string
            OpId of the data job run.
        :param ingest_config: IngesterConfiguration
            Configuration related to the core ingestion API.
        """
        self._data_job_name = data_job_name
        self._op_id = op_id
        self._ingester = ingester
        self._number_of_worker_threads = ingest_config.get_number_of_worker_threads()
        self._payload_size_bytes_threshold = (
            ingest_config.get_payload_size_bytes_threshold()
        )
        self._log_upload_errors = ingest_config.get_should_log_upload_errors()

        self._payload_aggregator_timeout_seconds = (
            ingest_config.get_payload_aggregator_timeout_seconds()
        )

        self._fail_count = AtomicCounter()
        self._plugin_errors = defaultdict(
            AtomicCounter
        )  # something like {UserCodeError: 10, VdkConfigurationError: 2}
        self._success_count = AtomicCounter()
        self._closed = AtomicCounter()
        self._objects_queue: queue.Queue = queue.Queue(
            ingest_config.get_objects_queue_size()
        )
        self._payloads_queue: queue.Queue = queue.Queue(
            ingest_config.get_payloads_queue_size()
        )
        self._exception_on_failure = (
            ingest_config.get_should_raise_exception_on_failure()
        )

        self._start_workers()

    def send_object_for_ingestion(
        self,
        payload: dict,
        destination_table: Optional[str],
        method: Optional[str],
        target: Optional[str] = None,
        collection_id: Optional[str] = None,
    ):
        """
        Send a self-contained object, asynchronously, for ingestion.

        :param payload: dictionary
            The payload to be send for ingestion.
        :param destination_table: Optional[string]
            (Optional) The name of the table, where the data should be ingested into.
            This parameter does not need to be passed, in case the table is included
            in the payload itself.
        :param method: Optional[string]
            (Optional) Indicates the ingestion method to be used. For example:
                    method="file" -> ingest to file
                    method="http" -> ingest using HTTP POST requests
                    method="kafka" -> ingest to kafka endpoint
            This parameter does not need to be passed, as ingestion plugins set
            a default value for it. In case multiple ingestion plugins are used,
            an `INGEST_METHOD_DEFAULT` environment variable can be set that would
            specify which plugin is to be used by default for ingestion.
        :param target: Optional[string]
            (Optional) Used to identify where the data should be ingested into.
                The value for this parameter depends on the ingest method chosen.
                For "http" method, it would require an HTTP URL.
                    Example: http://example.com/<some>/<api>/<endpoint>
                For "file" method, it would require a file name or path.

                See chosen ingest method (ingestion plugin) documentation for more details on the expected target format.
            This parameter does not need to be used, in case the
            `INGEST_TARGET_DEFAULT` environment variable is set. This can be made by
            plugins, which may set default value, or it can be overwritten by users.
        :param collection_id: Optional[string]
            (Optional) An identifier to indicate that data from different method
            invocations belong to same collection. Defaults to "data_job_name|OpID",
            meaning all method invocations from a data job run will belong to the same collection.
        """
        self.__verify_payload_format(payload_dict=payload)

        if collection_id is None:
            collection_id = "{data_job_name}|{execution_id}".format(
                data_job_name=self._data_job_name, execution_id=self._op_id
            )

        self._send(
            payload_dict=payload,
            destination_table=destination_table,
            method=method,
            target=target,
            collection_id=collection_id,
        )

    def send_tabular_data_for_ingestion(
        self,
        rows: iter,
        column_names: list,
        destination_table: Optional[str],
        method: Optional[str],
        target: Optional[str] = None,
        collection_id: Optional[str] = None,
    ):
        """
        Send tabular data for ingestion. The only condition for the rows and
        columns of the tabular is to for them to be separate Iterator objects.

        :param rows: Iterator
            one of the following: PEP249 Cursor object, Iterable 2 dimensional
            structure, A representation of a two-dimensional array that allows
            iteration over rows. Can be a list of lists, iterator that returns next
            row ("row" = list or tuple of values),
            PEP249 cursor object with successfully executed SELECT statement, etc.
            For example:
                [
                    [row0column0, row0column1]
                    [row1column0, row1column1]
                ]
        :param column_names: list
            the column names of the data in the same order as the values in data
            provided in the rows parameter.
            col[0] - corresponds to row0column0,row1column0,
            col[1] to row0column1, row1column1.
        :param destination_table: Optional[string]
            (Optional) The name of the table, where the data should be ingested into.
            This parameter does not need to be passed, in case the table is included
            in the payload itself.
        :param method: Optional[string]
            (Optional) Indicates the ingestion method to be used. For example:
                    method="file" -> ingest to file
                    method="http" -> ingest using HTTP POST requests
                    method="kafka" -> ingest to kafka endpoint
            This parameter does not need to be passed, as ingestion plugins set
            a default value for it. In case multiple ingestion plugins are used,
            an `INGEST_METHOD_DEFAULT` environment variable can be set that would
            specify which plugin is to be used by default for ingestion.
        :param target: Optional[string]
            (Optional) Used to identify where the data should be ingested into.
                The value for this parameter depends on the ingest method chosen.
                For "http" method, it would require an HTTP URL.
                    Example: http://example.com/<some>/<api>/<endpoint>
                For "file" method, it would require a file name or path.

                See chosen ingest method (ingestion plugin) documentation for more details on the expected target format.
            This parameter does not need to be used, in case the
            `INGEST_TARGET_DEFAULT` environment variable is set. This can be made by
            plugins, which may set default value, or it can be overwritten by users.
        :param collection_id: Optional[string]
            (Optional) An identifier to indicate that data from different method
            invocations belong to same collection. Defaults to "data_job_name|OpID",
            meaning all method invocations from a data job run will belong to the same collection.
        """
        if len(column_names) == 0 and destination_table is None:
            errors.log_and_throw(
                ResolvableBy.USER_ERROR,
                log,
                what_happened="Failed to ingest tabular data",
                why_it_happened="Either column names or destination table must be specified."
                "Without at least one of those we cannot determine how data should be ingested and we abort.",
                consequences="The data will not be ingested and the current call will fail with an exception.",
                countermeasures="Pass column names or destination table as argument.",
            )

        if not ingester_utils.is_iterable(rows):
            errors.log_and_throw(
                ResolvableBy.USER_ERROR,
                log,
                what_happened="Cannot ingest tabular data",
                why_it_happened=f"The rows argument must be an iterable but it was type: {type(rows)}",
                consequences="The data will not be ingested and current call will fail with an exception.",
                countermeasures="Make sure rows is proper iterator object ",
            )

        if not isinstance(column_names, Iterable):
            errors.log_and_throw(
                ResolvableBy.USER_ERROR,
                log,
                what_happened="Cannot ingest tabular data",
                why_it_happened=f"The column_names argument must be a List (or iterable) but it was: {type(rows)}",
                consequences="The data will not be ingested and current call will fail with an exception.",
                countermeasures="Make sure column_names is proper List object ",
            )

        log.info(
            "Posting for ingestion data for table {table} with columns {columns} against endpoint {endpoint}".format(
                table=destination_table, columns=column_names, endpoint=target
            )
        )

        if collection_id is None:
            collection_id = "{data_job_name}|{execution_id}".format(
                data_job_name=self._data_job_name, execution_id=self._op_id
            )

        # fetch data in chunks to prevent running out of memory
        for page_number, page in enumerate(ingester_utils.get_page_generator(rows)):
            ingester_utils.validate_column_count(page, column_names)
            converted_rows = ingester_utils.convert_table(page, column_names)
            log.debug(
                "Posting page {number} with {size} rows for ingestion.".format(
                    number=page_number, size=len(converted_rows)
                )
            )
            for row in converted_rows:
                self.__verify_payload_format(payload_dict=row)
                self._send(
                    payload_dict=row,
                    destination_table=destination_table,
                    method=method,
                    target=target,
                    collection_id=collection_id,
                )

    def _send(
        self,
        payload_dict: dict,
        destination_table: str,
        method: str,
        target: str,
        collection_id: str = None,
    ):
        """
        Send payload to the _objects_queue for processing.)

        :param payload_dict: dict
            Payload to be send to the _objects_queue.
        :param destination_table: string
            The name of the table, where the data should be ingested into.
        :param method: string
            Indicates the ingestion method to be used. E.g.:
                    method="file" -> ingest to file
                    method="http" -> ingest using HTTP POST requests
                    method="kafka" -> ingest to kafka endpoint
        :param target: string
            Used to identify where the data should be ingested into.
                The value for this parameter depends on the ingest method chosen.
                For "http" method, it would require an HTTP URL.
                    Example: http://example.com/<some>/<api>/<endpoint>
                For "file" method, it would require a file name or path.

                See chosen ingest method (ingestion plugin) documentation for more details on the expected target format.
        :param collection_id: string
            (Optional) An identifier to indicate that data from different method
            invocations belong to same collection. Defaults to "data_job_name|OpID",
            meaning all method invocations from a data job run will belong to the same collection.
        """
        self._objects_queue.put(
            (payload_dict, destination_table, method, target, collection_id)
        )

    def _payload_aggregator_thread(self):
        """
        Thread aggregating the ingestion data based on the provided payload size
        threshold and target/collection_id
        """
        aggregated_payload = []
        number_of_payloads = 0
        current_payload_size_in_bytes = 0
        current_target = None
        current_collection_id = None
        current_destination_table = None
        method = None
        while self._closed.value == 0:
            try:
                (
                    payload_dict,
                    destination_table,
                    method,
                    target,
                    collection_id,
                ) = self._objects_queue.get(
                    timeout=self._payload_aggregator_timeout_seconds
                )
            except queue.Empty:
                (
                    aggregated_payload,
                    number_of_payloads,
                    current_payload_size_in_bytes,
                ) = self._queue_payload_for_posting(
                    aggregated_payload,
                    number_of_payloads,
                    destination_table,
                    method,
                    current_target,
                    current_collection_id,
                )
                continue

            # First payload will determine the target and collection_id
            if (
                not current_target
                and not current_collection_id
                and not current_destination_table
            ):
                current_target = target
                current_collection_id = collection_id
                current_destination_table = destination_table

            # When we get a payload with different than current target/collection_id/destination_table,
            # send the current payload and start aggregating for the new one.
            if (
                current_target != target
                or current_collection_id != collection_id
                or current_destination_table != destination_table
            ):
                (
                    aggregated_payload,
                    number_of_payloads,
                    current_payload_size_in_bytes,
                ) = self._queue_payload_for_posting(
                    aggregated_payload,
                    number_of_payloads,
                    current_destination_table,
                    method,
                    current_target,
                    current_collection_id,
                )
                current_target = target
                current_collection_id = collection_id
                current_destination_table = destination_table

            # We are converting to string to get correct memory size. This may
            # cause performance issues.
            # TODO: Propose a way to calculate the object's memory footprint without converting to string.
            string_payload = str(payload_dict)

            if (
                sys.getsizeof(string_payload) + current_payload_size_in_bytes
                > self._payload_size_bytes_threshold
            ):
                (
                    aggregated_payload,
                    number_of_payloads,
                    current_payload_size_in_bytes,
                ) = self._queue_payload_for_posting(
                    aggregated_payload,
                    number_of_payloads,
                    current_destination_table,
                    method,
                    current_target,
                    current_collection_id,
                )
            aggregated_payload.append(payload_dict)
            number_of_payloads += 1
            current_payload_size_in_bytes += sys.getsizeof(string_payload)

    def _queue_payload_for_posting(
        self,
        aggregated_payload: list,
        number_of_payloads: int,
        destination_table: str,
        method: str,
        target: str,
        collection_id: str,
    ):
        """
        Send payload to the _payloads_queue.

        :param aggregated_payload: list
            List of aggregated payloads that are ready for final processing.
        :param number_of_payloads: int,
            Number of payloads to be dequeued from the _objects_queue.
        :param destination_table: string
            The name of the table, where the data should be ingested into.
        :param method: string
            Indicates the ingestion method to be used. E.g.:
                    method="file" -> ingest to file
                    method="http" -> ingest using HTTP POST requests
                    method="kafka" -> ingest to kafka endpoint
        :param collection_id: string
            An identifier to indicate that data from different method
            invocations belong to same collection. Defaults to "data_job_name|OpID",
            meaning all method invocations from a data job run will belong to the
            same collection.
        :param target: string
            Used to identify where the data should be ingested into.
                The value for this parameter depends on the ingest method chosen.
                For "http" method, it would require an HTTP URL.
                    Example: http://example.com/<some>/<api>/<endpoint>
                For "file" method, it would require a file name or path.

                See chosen ingest method (ingestion plugin) documentation for more details on the expected target format.
        """
        if aggregated_payload:
            try:
                self._payloads_queue.put(
                    (
                        aggregated_payload,
                        destination_table,
                        method,
                        target,
                        collection_id,
                    )
                )
            except Exception as e:
                self._fail_count.increment()
                if self._log_upload_errors:
                    log.warning(
                        "Failed to send a payload for ingestion. One or more rows were not ingested.\n"
                        "Exception was: {}".format(str(e))
                    )
            finally:
                for i in range(number_of_payloads):
                    self._objects_queue.task_done()
        # Return statement below is coupled with _payload_aggregator_thread
        # and is used to reset the aggregated payload, number of payloads and
        # its aggregated payload size
        aggregated_payload_reset: list = []
        number_of_payloads_reset: int = 0
        current_payload_size_in_bytes_reset: int = 0
        return (
            aggregated_payload_reset,
            number_of_payloads_reset,
            current_payload_size_in_bytes_reset,
        )

    def _payload_poster_thread(self):
        """
        Thread doing final data preparation (adding additional metadata, telemetry
        data, etc.) and ingesting the data.
        """
        while self._closed.value == 0:
            payload: Optional[Tuple] = None
            ingestion_metadata: Optional[IIngesterPlugin.IngestionMetadata] = None
            exception: Optional[Exception] = None
            try:
                payload = self._payloads_queue.get()
                payload_dict, destination_table, method, target, collection_id = payload

                try:
                    ingestion_metadata = self._ingester.ingest_payload(
                        payload=payload_dict,
                        destination_table=destination_table,
                        target=target,
                        collection_id=collection_id,
                    )

                    self._success_count.increment()
                except VdkConfigurationError as e:
                    self._plugin_errors[VdkConfigurationError].increment()
                    # TODO: logging for every error might be too much
                    # There could be million of uploads and millions of error logs would be hard to use.
                    # But until we have a way to aggregate the errors and show
                    # the most relevant errors it's better to make sure we do not hide an issue
                    # and be verbose.
                    log.exception(
                        "A configuration error occurred while ingesting data."
                    )
                    exception = e
                except UserCodeError as e:
                    self._plugin_errors[UserCodeError].increment()
                    log.exception("An user error occurred while ingesting data.")
                    exception = e
                except Exception as e:
                    self._plugin_errors[PlatformServiceError].increment()
                    log.exception("A platform error occurred while ingesting data.")
                    exception = e

            except Exception as e:
                self._fail_count.increment()
                if self._log_upload_errors:
                    # TODO: When working on row count telemetry we can add the exact number of rows not ingested.
                    log.warning(
                        "Failed to ingest a payload. "
                        "One or more rows were not ingested.\n"
                        "Exception was: {}".format(str(e))
                    )
                    exception = e
            finally:
                self._payloads_queue.task_done()

            # Complete Post-Ingestion operations
            try:
                self._ingester.post_ingest_process(
                    payload=payload_dict,
                    metadata=ingestion_metadata,
                    exception=exception,
                )
            except Exception as e:
                log.info(
                    "Could not complete the post-ingestion operation. "
                    f"The error encountered was: {e}",
                )

    def _start_workers(self):
        """
        Start the worker threads.
        """
        t = threading.Thread(
            target=self._payload_aggregator_thread, name="payload-aggregator"
        )
        t.daemon = True
        t.start()
        for i in range(self._number_of_worker_threads):
            thread_name = f"payload-poster{i}"
            t = threading.Thread(target=self._payload_poster_thread, name=thread_name)
            t.daemon = True
            t.start()

    def close(self):
        """
        Wait for completion of processing of all data added to the payload
        queue and then log the ingestion statistics.
        """
        ingester_utils.wait_completion(
            objects_queue=self._objects_queue, payloads_queue=self._payloads_queue
        )
        self.close_now()

    def close_now(self):
        """
        Close immediately. The method will not wait for the active queue items to get processed.
        """
        if self._closed.get_and_increment() == 0:

            if self._exception_on_failure:
                self._handle_results()

            log.info(
                "Ingester statistics: \n\t\t"
                f"Successful uploads:{self._success_count}\n\t\t"
                f"Failed uploads:{self._fail_count}\n\t\t"
                f"ingesting plugin errors:{self._plugin_errors}\n\t\t"
            )

    def _handle_results(self):
        if self._plugin_errors.get(UserCodeError, AtomicCounter(0)).value > 0:
            self._log_and_throw(
                to_be_fixed_by=ResolvableBy.USER_ERROR,
                countermeasures="Ensure data you are sending is aligned with the requirements",
                why_it_happened="User error occurred. See warning logs for more details. ",
            )
        if self._plugin_errors.get(VdkConfigurationError, AtomicCounter(0)).value > 0:
            self._log_and_throw(
                to_be_fixed_by=ResolvableBy.CONFIG_ERROR,
                countermeasures="Ensure job is properly configured. "
                "For example make sure that target and method specified are correct",
            )
        if (
            self._plugin_errors.get(PlatformServiceError, AtomicCounter(0)).value > 0
            or self._fail_count.value > 0
        ):
            self._log_and_throw(
                to_be_fixed_by=ResolvableBy.PLATFORM_ERROR,
                countermeasures="There has been temporary failure. "
                "You can retry the data job again. "
                "If error persist inspect logs and check ingest plugin documentation.",
            )

    def _log_and_throw(
        self,
        to_be_fixed_by,
        countermeasures,
        why_it_happened="Payloads failed to get posted for ingestion",
    ):
        errors.log_and_throw(
            to_be_fixed_by=to_be_fixed_by,
            log=log,
            what_happened="Failed to post all data for ingestion successfully.",
            why_it_happened=why_it_happened,
            consequences="Some data will not be ingested.",
            countermeasures=countermeasures,
        )

    @staticmethod
    def __verify_payload_format(payload_dict: dict):
        if not payload_dict:
            raise errors.UserCodeError(
                "Payload given to " "ingestion method should " "not be empty."
            )

        elif not isinstance(payload_dict, dict):
            raise errors.UserCodeError(
                "Payload given to ingestion method should be a "
                "dictionary, but it is not."
            )

        # Check if payload dict is valid json
        # TODO: optimize the check - we should not need to serialize the payload every time
        try:
            json.dumps(payload_dict)
        except (TypeError, OverflowError, Exception) as e:
            errors.log_and_throw(
                errors.ResolvableBy.USER_ERROR,
                log,
                "Failed to send payload",
                "JSON Serialization Error. Payload is not json serializable",
                "Payload may be only partially ingested, or not ingested at all.",
                f"See error message for help: {str(e)}",
            )
