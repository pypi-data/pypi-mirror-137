from __future__ import annotations

import math
import os
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    Final,
    List,
    Optional,
    Protocol,
    Tuple,
    cast,
    runtime_checkable,
)
import uuid

from google.protobuf.timestamp_pb2 import Timestamp
import grpc
import tblib

from jetpack import __version__
from jetpack._runtime.errors import JetpackError, RuntimeError
from jetpack._runtime.local import LocalStub
from jetpack._util import jetpickle
from jetpack._util.network import codec
from jetpack.config import instrumentation, k8s, namespace
from jetpack.proto.runtime.v1alpha1 import remote_pb2, remote_pb2_grpc

# Instead of having individual clients per functionality (e.g. job), have a
# single client for our runtime.

# TODO(Landau): Move client functionality out of _job.client and centralize it
# here.

# TODO(landau): make this a param
MAX_MESSAGE_LENGTH: Final[int] = 10485760  # 10MB

# Prevent circular dependency
if TYPE_CHECKING:
    from jetpack._task.task import Task


class Client:
    def __init__(self) -> None:
        host = os.environ.get(
            "JETPACK_RUNTIME_SERVICE_HOST",
            "runtime.jetpack-runtime.svc.cluster.local",
        )
        port = os.environ.get("JETPACK_RUNTIME_SERVICE_PORT", "80")
        self.address: str = f"{host.strip()}:{port.strip()}"
        self.stub: Optional[remote_pb2_grpc.RemoteExecutorStub] = None

    def dial(self) -> remote_pb2_grpc.RemoteExecutorStub:
        if self.stub is None:
            if k8s.is_in_cluster():
                channel = grpc.aio.insecure_channel(
                    self.address,
                    options=[
                        ("grpc.max_send_message_length", MAX_MESSAGE_LENGTH),
                    ],
                )
                self.stub = remote_pb2_grpc.RemoteExecutorStub(channel)
            else:
                self.stub = LocalStub(self)
        return self.stub

    async def set_cron_jobs(
        self,
        cron_jobs: List[remote_pb2.CronJob],
    ) -> remote_pb2.SetCronJobsResponse:
        request = remote_pb2.SetCronJobsRequest(
            namespace=cast(str, namespace.get()),
            hostname=os.environ["HOSTNAME"],
            cron_jobs=cron_jobs,
        )
        stub = self.dial()
        response: remote_pb2.SetCronJobsResponse = await stub.SetCronJobs(request)
        return response

    async def create_task(
        self,
        task: Task,
        args: Optional[Tuple[Any, ...]] = None,
        kwargs: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Creates a Jetpack task. How the task gets executed is up to
        jetpack runtime.

        Keyword arguments:
        task -- task to create
        """

        request = self._build_create_task_request(task, args, kwargs)
        response: remote_pb2.CreateTaskResponse = await self.dial().CreateTask(request)
        task.id = uuid.UUID(response.task_id)
        if task.is_scheduled:
            instrumentation.get_tracer().scheduled_task_created(task)
        else:
            instrumentation.get_tracer().task_created(task)

    async def cancel_task(self, task_id: str) -> bool:
        req = remote_pb2.CancelTaskRequest(task_id=task_id)
        resp: remote_pb2.CancelTaskResponse = await self.dial().CancelTask(req)
        return resp.success

    async def post_result(
        self, exec_id: str, value: Any = None, error: Optional[Exception] = None
    ) -> remote_pb2.PostResultResponse:

        if not exec_id:
            # Note: value=None and error=None is acceptable because a job
            # can run successfully and return nothing.
            raise Exception("An exec_id is required to post a result")

        result = remote_pb2.Result()
        if error:
            result.error.code = remote_pb2.APPLICATION
            result.error.message = str(error)

            result.error.encoded_error = jetpickle.encode(error)
        else:  # order matters, as 'value' can be None
            result.value.encoded_value = jetpickle.encode(value)

        request = remote_pb2.PostResultRequest(
            exec_id=exec_id,
            result=result,
        )

        response = await self.dial().PostResult(request)
        return cast(remote_pb2.PostResultResponse, response)

    async def wait_for_result(self, task_id: uuid.UUID, symbol_name: str) -> Any:
        request = remote_pb2.WaitForResultRequest(task_id=str(task_id))
        response = await self.dial().WaitForResult(request)
        instrumentation.get_tracer().result_returned(task_id, response.result)
        return self._transform_response_exception(response, symbol_name)

    async def get_task(self, task_id: str) -> remote_pb2.GetTaskResponse:
        request = remote_pb2.GetTaskRequest(task_id=task_id)
        response: remote_pb2.GetTaskResponse = await self.dial().GetTask(request)
        return response

    @staticmethod
    def _build_create_task_request(
        task: Task,
        args: Optional[Tuple[Any, ...]],
        kwargs: Optional[Dict[str, Any]],
    ) -> remote_pb2.CreateTaskRequest:
        encoded_args = b""
        if args or kwargs:
            encoded_args = codec.encode_args(
                args if args else None,
                kwargs if kwargs else None,
            ).encode("utf-8")

        if len(encoded_args) > MAX_MESSAGE_LENGTH:
            raise RuntimeError(
                f"Function argument size is over {math.floor(MAX_MESSAGE_LENGTH / 1000000)}MB"
            )

        current_namespace = namespace.get()
        task_proto_obj = remote_pb2.Task(
            qualified_symbol=task.jetpack_function.name(),
            encoded_args=encoded_args,
            hostname=os.environ.get("HOSTNAME", ""),  # k8s sets this
            target_time=Timestamp(seconds=task.target_time),
        )
        if current_namespace:
            task_proto_obj.namespace = current_namespace

        return remote_pb2.CreateTaskRequest(
            task=task_proto_obj, sdk_version=__version__
        )

    @staticmethod
    def _transform_response_exception(
        response: remote_pb2.WaitForResultResponse,
        symbol_name: str,
    ) -> Any:
        if response.result.HasField("error") and response.result.error.encoded_error:
            err = jetpickle.decode(response.result.error.encoded_error)
            jetpack_err = JetpackError(f"chained exception for: {symbol_name}")
            raise jetpack_err from err
        elif response.result.HasField("value"):
            val = jetpickle.decode(response.result.value.encoded_value)
            return val
        else:
            raise RuntimeError(
                f"Either 'value' or 'error' should be specified in response. Got: {response}"
            )


client = Client()
