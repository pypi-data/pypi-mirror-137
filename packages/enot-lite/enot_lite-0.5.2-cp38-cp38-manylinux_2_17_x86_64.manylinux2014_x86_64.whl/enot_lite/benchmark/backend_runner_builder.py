from typing import Any
from typing import Dict
from typing import Type

from enot_lite import backend
from enot_lite.benchmark.backend_runner import EnotBackendRunner
from enot_lite.benchmark.backend_runner import TorchCpuRunner
from enot_lite.benchmark.backend_runner import TorchCudaRunner
from enot_lite.calibration import calibrate

__all__ = [
    'OrtCpuBackendRunnerBuilder',
    'OrtOpenvinoFloatBackendRunnerBuilder',
    'OrtOpenvinoInt8BackendRunnerBuilder',
    'OrtCudaBackendRunnerBuilder',
    'OrtTensorrtFloatBackendRunnerBuilder',
    'OrtTensorrtFloatOptimBackendRunnerBuilder',
    'OrtTensorrtInt8BackendRunnerBuilder',
    'OrtTensorrtInt8QDQBackendRunnerBuilder',
    'TorchCpuBackendRunnerBuilder',
    'TorchCudaBackendRunnerBuilder',
]


class OrtCpuBackendRunnerBuilder:
    def __call__(
        self,
        onnx_model,
        onnx_input: Dict[str, Any],
        inter_op_num_threads,
        intra_op_num_threads,
        enot_backend_runner: Type[EnotBackendRunner],
        **_ignored,
    ):
        backend_instance = backend.OrtCpuBackend(
            model=onnx_model,
            inter_op_num_threads=inter_op_num_threads,
            intra_op_num_threads=intra_op_num_threads,
        )
        return enot_backend_runner(backend_instance, onnx_input)


class OrtOpenvinoFloatBackendRunnerBuilder:
    def __call__(
        self,
        onnx_model,
        onnx_input: Dict[str, Any],
        inter_op_num_threads,
        intra_op_num_threads,
        openvino_num_threads,
        enot_backend_runner: Type[EnotBackendRunner],
        **_ignored,
    ):
        backend_instance = backend.OrtOpenvinoFloatBackend(
            model=onnx_model,
            input_example=onnx_input,
            inter_op_num_threads=inter_op_num_threads,
            intra_op_num_threads=intra_op_num_threads,
            openvino_num_threads=openvino_num_threads,
        )
        return enot_backend_runner(backend_instance, onnx_input)


class OrtOpenvinoInt8BackendRunnerBuilder:
    def __call__(
        self,
        onnx_model,
        onnx_input: Dict[str, Any],
        inter_op_num_threads,
        intra_op_num_threads,
        openvino_num_threads,
        enot_backend_runner: Type[EnotBackendRunner],
        **_ignored,
    ):
        backend_instance = backend.OrtOpenvinoInt8Backend(
            model=onnx_model,
            input_example=onnx_input,
            inter_op_num_threads=inter_op_num_threads,
            intra_op_num_threads=intra_op_num_threads,
            openvino_num_threads=openvino_num_threads,
        )
        return enot_backend_runner(backend_instance, onnx_input)


class OrtCudaBackendRunnerBuilder:
    def __call__(self, onnx_model, onnx_input: Dict[str, Any], enot_backend_runner: Type[EnotBackendRunner], **_ignored):
        backend_instance = backend.OrtCudaBackend(onnx_model)
        return enot_backend_runner(backend_instance, onnx_input)


class OrtTensorrtFloatBackendRunnerBuilder:
    def __call__(self, onnx_model, onnx_input: Dict[str, Any], enot_backend_runner: Type[EnotBackendRunner], **_ignored):
        backend_instance = backend.OrtTensorrtFloatBackend(model=onnx_model, input_example=onnx_input)
        return enot_backend_runner(backend_instance, onnx_input)


class OrtTensorrtFloatOptimBackendRunnerBuilder:
    def __call__(self, onnx_model, onnx_input: Dict[str, Any], enot_backend_runner: Type[EnotBackendRunner], **_ignored):
        backend_instance = backend.OrtTensorrtFloatOptimBackend(model=onnx_model, input_example=onnx_input)
        return enot_backend_runner(backend_instance, onnx_input)


class OrtTensorrtInt8BackendRunnerBuilder:
    def __call__(self, onnx_model, onnx_input: Dict[str, Any], enot_backend_runner: Type[EnotBackendRunner], **_ignored):
        calibration_table = calibrate(model=onnx_model, dataset=onnx_input.values(), batches_count_for_calibration=1)
        backend_instance = backend.OrtTensorrtInt8Backend(
            model=onnx_model,
            input_example=onnx_input,
            calibration_table=calibration_table,
        )
        return enot_backend_runner(backend_instance, onnx_input)


class OrtTensorrtInt8QDQBackendRunnerBuilder:
    def __call__(self, onnx_model, onnx_input: Dict[str, Any], enot_backend_runner: Type[EnotBackendRunner], **_ignored):
        backend_instance = backend.OrtTensorrtInt8QDQBackend(
            model=onnx_model,
            input_example=onnx_input,
        )
        return enot_backend_runner(backend_instance, onnx_input)


class TorchCpuBackendRunnerBuilder:
    def __call__(self, torch_model, torch_input, torch_cpu_runner: Type[TorchCpuRunner], **_ignored):
        return torch_cpu_runner(torch_model=torch_model, torch_input=torch_input)


class TorchCudaBackendRunnerBuilder:
    def __call__(self, torch_model, torch_input, torch_cuda_runner: Type[TorchCudaRunner], **_ignored):
        return torch_cuda_runner(torch_model=torch_model, torch_input=torch_input)
