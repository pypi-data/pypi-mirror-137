"""Results Only protocol."""
from __future__ import annotations

import os
import time
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    List,
    Optional,
    Protocol,
    Type,
    Union,
    cast,
    overload,
    runtime_checkable,
)

from marshmallow import Schema as MarshmallowSchema
from marshmallow import fields, post_load

from bitfount.data.datasource import DataSource
from bitfount.federated.logging import _get_federated_logger
from bitfount.federated.pod_vitals import _PodVitals
from bitfount.federated.privacy.differential import DPPodConfig
from bitfount.federated.protocols.base import (
    _BaseCompatibleAlgoFactory,
    _BaseModellerProtocol,
    _BaseProtocolFactory,
    _BaseWorkerProtocol,
)
from bitfount.federated.transport.modeller_transport import _ModellerMailbox
from bitfount.federated.transport.worker_transport import _WorkerMailbox
from bitfount.types import _JSONDict

if TYPE_CHECKING:
    from bitfount.hub.api import BitfountHub

logger = _get_federated_logger(__name__)


@runtime_checkable
class _ResultsOnlyCompatibleModeller(Protocol):
    """Defines modeller-side algorithm compatibility."""

    @overload
    def initialise(
        self,
        **kwargs: Any,
    ) -> None:
        ...

    @overload
    def initialise(
        self,
        pretrained_file: Optional[Union[str, os.PathLike]] = None,
        **kwargs: Any,
    ) -> None:
        ...

    def initialise(
        self,
        pretrained_file: Optional[Union[str, os.PathLike]] = None,
        **kwargs: Any,
    ) -> None:
        """Initialise the modeller-side algorithm."""
        ...

    def run(self, results: List[Dict[str, float]]) -> List[Dict[str, float]]:
        """Run the modeller-side algorithm."""
        ...


@runtime_checkable
class _ResultsOnlyCompatibleWorker(Protocol):
    @overload
    def initialise(
        self,
        datasource: DataSource,
        **kwargs: Any,
    ) -> None:
        ...

    @overload
    def initialise(
        self,
        datasource: DataSource,
        pod_dp: Optional[DPPodConfig] = None,
        **kwargs: Any,
    ) -> None:
        ...

    def initialise(
        self,
        datasource: DataSource,
        pod_dp: Optional[DPPodConfig] = None,
        **kwargs: Any,
    ) -> None:
        """Initialise the worker-side algorithm."""
        ...


@runtime_checkable
class _ResultsOnlyDataIncompatibleWorker(_ResultsOnlyCompatibleWorker, Protocol):
    """Defines modeller-side algorithm compatibility without datasource.."""

    def run(self) -> Dict[str, float]:
        """Run the worker-side algorithm."""
        ...


@runtime_checkable
class _ResultsOnlyDataCompatibleWorker(_ResultsOnlyCompatibleWorker, Protocol):
    """Defines modeller-side algorithm compatibility with datasource needed."""

    def run(self, data: DataSource) -> Dict[str, float]:
        """Run the worker-side algorithm."""
        ...


class _ModellerSide(_BaseModellerProtocol):
    """Modeller side of the ResultsOnly protocol."""

    algorithm: _ResultsOnlyCompatibleModeller

    def __init__(
        self,
        *,
        algorithm: _ResultsOnlyCompatibleModeller,
        mailbox: _ModellerMailbox,
        **kwargs: Any,
    ):
        super().__init__(algorithm=algorithm, mailbox=mailbox, **kwargs)

    async def run(
        self,
        pretrained_file: Optional[Union[str, os.PathLike]] = None,
        **kwargs: Any,
    ) -> List[Any]:
        """Runs Modeller side of the protocol."""
        self.algorithm.initialise(pretrained_file=pretrained_file)

        eval_results = await self.mailbox.get_evaluation_results_from_workers()
        modeller_results = self.algorithm.run(eval_results)
        await self.mailbox.send_task_complete_message()
        return modeller_results


class _WorkerSide(_BaseWorkerProtocol):
    """Worker side of the ResultsOnly protocol."""

    algorithm: Union[
        _ResultsOnlyDataIncompatibleWorker, _ResultsOnlyDataCompatibleWorker
    ]

    def __init__(
        self,
        *,
        algorithm: Union[
            _ResultsOnlyDataIncompatibleWorker, _ResultsOnlyDataCompatibleWorker
        ],
        mailbox: _WorkerMailbox,
        **kwargs: Any,
    ):
        super().__init__(algorithm=algorithm, mailbox=mailbox, **kwargs)

    async def run(
        self,
        datasource: DataSource,
        pod_dp: Optional[DPPodConfig] = None,
        pod_vitals: Optional[_PodVitals] = None,
        **kwargs: Any,
    ) -> None:
        """Runs Worker side of the protocol."""
        self.algorithm.initialise(datasource=datasource, pod_dp=pod_dp)
        if pod_vitals:
            pod_vitals.last_task_execution_time = time.time()
        try:
            self.algorithm = cast(_ResultsOnlyDataCompatibleWorker, self.algorithm)
            results = self.algorithm.run(data=datasource)
        except TypeError:
            self.algorithm = cast(_ResultsOnlyDataIncompatibleWorker, self.algorithm)
            results = self.algorithm.run()
        await self.mailbox.send_evaluation_results(results)
        await self.mailbox.get_task_complete_update()


@runtime_checkable
class _ResultsOnlyCompatibleAlgoFactory(_BaseCompatibleAlgoFactory, Protocol):
    """Defines algo factory compatibility."""

    def modeller(self, **kwargs: Any) -> _ResultsOnlyCompatibleModeller:
        """Create a modeller-side algorithm."""
        ...


@runtime_checkable
class _ResultsOnlyCompatibleAlgoFactory_(_ResultsOnlyCompatibleAlgoFactory, Protocol):
    """Defines algo factory compatibility."""

    def worker(
        self, **kwargs: Any
    ) -> Union[_ResultsOnlyDataIncompatibleWorker, _ResultsOnlyDataCompatibleWorker]:
        """Create a worker-side algorithm."""
        ...

    @staticmethod
    def get_schema(**kwargs: Any) -> Type[MarshmallowSchema]:
        """Get schema."""
        ...


@runtime_checkable
class _ResultsOnlyCompatibleModelAlgoFactory(
    _ResultsOnlyCompatibleAlgoFactory, Protocol
):
    """Defines algo factory compatibility."""

    def worker(
        self, hub: BitfountHub, **kwargs: Any
    ) -> Union[_ResultsOnlyDataIncompatibleWorker, _ResultsOnlyDataCompatibleWorker]:
        """Create a worker-side algorithm."""
        ...

    @property
    def model_schema(self) -> Type[MarshmallowSchema]:
        """Model schema."""
        ...

    @staticmethod
    def get_schema(
        model_schema: Type[MarshmallowSchema], **kwargs: Any
    ) -> Type[MarshmallowSchema]:
        """Get schema."""
        ...


class ResultsOnly(_BaseProtocolFactory):
    """Simply returns the results from the provided algorithm.

    This protocol is the most permissive protocol and only involves one round of
    communication. It simply runs the algorithm on the `Pod`(s) and returns the
    results as a list (one element for every pod).

    Args:
        algorithm: The algorithm to run.

    Attributes:
        name: The name of the protocol.
        algorithm: The algorithm to run. This must be compatible with the `ResultsOnly`
            protocol.

    Raises:
        TypeError: If the `algorithm` is not compatible with the protocol.
    """

    # TODO: [BIT-1047] Consider separating this protocol into two separate protocols
    #       for each algorithm. The algorithms may not be similar enough to benefit
    #       from sharing one protocol.

    algorithm: Union[
        _ResultsOnlyCompatibleAlgoFactory_, _ResultsOnlyCompatibleModelAlgoFactory
    ]

    def __init__(
        self,
        *,
        algorithm: Union[
            _ResultsOnlyCompatibleAlgoFactory_, _ResultsOnlyCompatibleModelAlgoFactory
        ],
        **kwargs: Any,
    ) -> None:
        super().__init__(algorithm=algorithm, **kwargs)

    @classmethod
    def _validate_algorithm(
        cls,
        algorithm: _BaseCompatibleAlgoFactory,
    ) -> None:
        """Checks that `algorithm` is compatible with the protocol."""
        if not isinstance(
            algorithm,
            (
                _ResultsOnlyCompatibleAlgoFactory_,
                _ResultsOnlyCompatibleModelAlgoFactory,
            ),
        ):
            raise TypeError(
                f"The {cls.__name__} protocol does not support "
                + f"the {type(algorithm).__name__} algorithm.",
            )

    @staticmethod
    def get_schema(
        algorithm_schema: Type[MarshmallowSchema],
        **kwargs: Any,
    ) -> MarshmallowSchema:
        """Returns the schema for ResultsOnly."""

        class Schema(_BaseProtocolFactory._Schema):
            algorithm = fields.Nested(algorithm_schema)

            @post_load
            def recreate_factory(self, data: dict, **_kwargs: Any) -> ResultsOnly:
                return ResultsOnly(**data)

        return Schema()

    def dump(self) -> _JSONDict:
        """Returns the JSON-serializable representation of the protocol."""
        if isinstance(self.algorithm, _ResultsOnlyCompatibleModelAlgoFactory):
            model_schema = self.algorithm.model_schema
            algorithm_schema = self.algorithm.get_schema(model_schema=model_schema)
        else:
            algorithm_schema = self.algorithm.get_schema()

        schema = self.get_schema(algorithm_schema)
        return cast(_JSONDict, schema.dump(self))

    def modeller(self, mailbox: _ModellerMailbox, **kwargs: Any) -> _ModellerSide:
        """Returns the modeller side of the ResultsOnly protocol."""
        return _ModellerSide(
            algorithm=self.algorithm.modeller(),
            mailbox=mailbox,
            **kwargs,
        )

    def worker(
        self, mailbox: _WorkerMailbox, hub: BitfountHub, **kwargs: Any
    ) -> _WorkerSide:
        """Returns the worker side of the ResultsOnly protocol."""
        return _WorkerSide(
            algorithm=self.algorithm.worker(hub=hub),
            mailbox=mailbox,
            **kwargs,
        )
