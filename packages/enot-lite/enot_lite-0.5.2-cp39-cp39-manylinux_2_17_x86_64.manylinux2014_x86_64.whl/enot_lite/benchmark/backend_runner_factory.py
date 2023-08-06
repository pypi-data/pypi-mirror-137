from typing import Callable

from enot_lite import backend
from enot_lite.benchmark.backend_runner_builder import OrtCpuBackendRunnerBuilder
from enot_lite.benchmark.backend_runner_builder import OrtCudaBackendRunnerBuilder
from enot_lite.benchmark.backend_runner_builder import OrtOpenvinoFloatBackendRunnerBuilder
from enot_lite.benchmark.backend_runner_builder import OrtOpenvinoInt8BackendRunnerBuilder
from enot_lite.benchmark.backend_runner_builder import OrtTensorrtFloatBackendRunnerBuilder
from enot_lite.benchmark.backend_runner_builder import OrtTensorrtFloatOptimBackendRunnerBuilder
from enot_lite.benchmark.backend_runner_builder import OrtTensorrtInt8BackendRunnerBuilder
from enot_lite.benchmark.backend_runner_builder import OrtTensorrtInt8QDQBackendRunnerBuilder
from enot_lite.benchmark.backend_runner_builder import TorchCpuBackendRunnerBuilder
from enot_lite.benchmark.backend_runner_builder import TorchCudaBackendRunnerBuilder

__all__ = [
    'FACTORY',
]


class BackendRunnerFactory:
    """
    Produces :class:`~enot_lite.benchmark.backend_runner.BackendRunner` objects.

    To extend :class:`~enot_lite.benchmark.benchmark.Benchmark` for your own backend, create builder
    and register it with the help of :func:`register_builder`.
    Builder is a callable object that wraps your backend, model and input data into
    :class:`~enot_lite.benchmark.backend_runner.BackendRunner` object.
    You can see how we wrapped our and ``PyTorch`` backends in :mod:`enot_lite.benchmark.backend_runner_builder`
    module.

    Use ``FACTORY`` object exported by this module to get instance of :class:`BackendRunnerFactory`.
    """

    def __init__(self):
        self._builders = {}

    def register_builder(self, backend_name: str, builder: Callable):
        """
        Registers new :class:`~enot_lite.benchmark.backend_runner.BackendRunner` builder
        for backend with ``backend_name`` name.

        Parameters
        ----------
        backend_name : str
            The name of the backend for which new builder will be registered.
        builder : Callable
            Builder that wraps backend, model and input data into
            :class:`~enot_lite.benchmark.backend_runner.BackendRunner` object.

        """
        self._builders[backend_name] = builder

    def create(self, backend_name: str, **kwargs):
        """
        Creates new :class:`~enot_lite.benchmark.backend_runner.BackendRunner` object
        by using registred builder for ``backend_name``.

        Parameters
        ----------
        backend_name : str
            The name of the backend which factory should wrap and produce.
        **kwargs
            Arbitrary keyword arguments that will be passed to particular builder.
            This arguments should contain all information for successful object construction.
            :class:`~enot_lite.benchmark.benchmark.Benchmark` forms and passes
            these arguments to :class:`~enot_lite.benchmark.backend_runner_factory.BackendRunnerFactory`.

        """
        builder = self._builders.get(backend_name)
        if not builder:
            raise ValueError(f'Got unregistered backend_name {backend_name}')
        return builder()(**kwargs)


FACTORY = BackendRunnerFactory()

# Register CPU backend builders.
FACTORY.register_builder(backend.OrtCpuBackend.__name__, OrtCpuBackendRunnerBuilder)
FACTORY.register_builder(backend.OrtOpenvinoFloatBackend.__name__, OrtOpenvinoFloatBackendRunnerBuilder)
FACTORY.register_builder(backend.OrtOpenvinoInt8Backend.__name__, OrtOpenvinoInt8BackendRunnerBuilder)

# Register CUDA backend builders.
FACTORY.register_builder(backend.OrtCudaBackend.__name__, OrtCudaBackendRunnerBuilder)
FACTORY.register_builder(backend.OrtTensorrtFloatBackend.__name__, OrtTensorrtFloatBackendRunnerBuilder)
FACTORY.register_builder(backend.OrtTensorrtFloatOptimBackend.__name__, OrtTensorrtFloatOptimBackendRunnerBuilder)
FACTORY.register_builder(backend.OrtTensorrtInt8Backend.__name__, OrtTensorrtInt8BackendRunnerBuilder)
FACTORY.register_builder(backend.OrtTensorrtInt8QDQBackend.__name__, OrtTensorrtInt8QDQBackendRunnerBuilder)

# Register Torch backend builders.
FACTORY.register_builder('TorchCpu', TorchCpuBackendRunnerBuilder)
FACTORY.register_builder('TorchCuda', TorchCudaBackendRunnerBuilder)
