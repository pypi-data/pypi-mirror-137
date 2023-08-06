"""Contains classes for marking differential privacy on models."""
from dataclasses import dataclass, field
from typing import Any, List, Literal, Mapping, Optional, Tuple, Union

import desert
import marshmallow
from marshmallow import Schema as MarshmallowSchema
from marshmallow import fields
from marshmallow.validate import OneOf

from bitfount.federated.logging import _get_federated_logger

logger = _get_federated_logger(__name__)

_DEFAULT_ALPHAS: List[float] = [1 + x / 10.0 for x in range(1, 100)] + list(
    range(12, 64)
)
_DEFAULT_DELTA: float = 1e-6
_ALLOWED_LOSS_REDUCTIONS: Tuple[str, str] = ("mean", "sum")


@dataclass
class DPModellerConfig:
    """Modeller configuration options for Differential Privacy.

    Args:
        max_epsilon: The maximum epsilon value to use.
        max_grad_norm: The maximum gradient norm to use. Defaults to 1.0.
        noise_multiplier: The noise multiplier to use. Defaults to 0.4.
        alphas: The alphas to use. Defaults to floats from 1.1 to 63.0 (inclusive) with
            increments of 0.1 up to 11.0 followed by increments of 1.0 up to 63.0.
        target_delta: The target delta to use. Defaults to 1e-6.
        loss_reduction: The loss reduction to use. Available options are "mean" and
            "sum". Defaults to "mean".
        auto_fix: Whether to automatically fix the model if it is not DP-compliant.
            Currently, this just converts all `BatchNorm` layers to `GroupNorm`.
            Defaults to True.

    Raises:
        ValueError: If loss_reduction is not one of "mean" or "sum".

    :::info

    `max_epsilon` and `target_delta` are also set by the Pods involved in the task and
    take precedence over the values supplied here.

    :::
    """

    # DP directly related options
    max_epsilon: float
    max_grad_norm: Union[float, List[float]] = 1.0
    noise_multiplier: float = 0.4
    alphas: List[float] = field(default_factory=lambda: _DEFAULT_ALPHAS)
    target_delta: float = _DEFAULT_DELTA
    loss_reduction: Literal["mean", "sum"] = desert.field(  # type: ignore[assignment] # Reason: desert.field is intentional # noqa: B950
        marshmallow.fields.String(validate=OneOf(_ALLOWED_LOSS_REDUCTIONS)),
        default="mean",
    )

    # Other options
    auto_fix: bool = True

    def __post_init__(self) -> None:
        # Validate loss_reduction
        if self.loss_reduction not in _ALLOWED_LOSS_REDUCTIONS:
            raise ValueError(
                f"loss_reduction must be one of {_ALLOWED_LOSS_REDUCTIONS}, "
                f'not "{self.loss_reduction}".'
            )


@dataclass
class DPPodConfig:
    """Pod configuration options for Differential Privacy.

    Primarily used as caps and bounds for what options may be set by the modeller.

    Args:
        max_epsilon: The maximum epsilon value to use.
        max_target_delta: The maximum target delta to use. Defaults to 1e-6.
    """

    max_epsilon: float
    max_target_delta: float = _DEFAULT_DELTA


class _DifferentiallyPrivate:
    """Marks that the model supports differential privacy.

    This class itself does not handle the implementation details of DP (as that
    will differ on a per-model/per-library basis) but captures the configuration
    details for DP to enable implementing models to make use of it.
    """

    def __init__(
        self,
        dp_config: Optional[Union[DPModellerConfig, Mapping[str, Any]]] = None,
        **kwargs: Any,
    ):
        """Stores the Differential Privacy configuration for this model.

        Args:
            dp_config: The Differential Privacy configuration to use. Can be either
                a `DPModellerConfig` instance or a string-keyed mapping.
            **kwargs: Other keyword arguments to be passed up the inheritance
                hierarchy.
        """
        # Capture DP config options, converting if needed
        if not isinstance(dp_config, DPModellerConfig):
            dp_config = self._convert_to_dpconfig(dp_config)
        self._dp_config: Optional[DPModellerConfig] = dp_config

        if self._dp_config:
            logger.info(
                f"Model is differentially private with settings: {self._dp_config}"
            )
        else:
            logger.info("No differential privacy settings provided.")

        super().__init__(**kwargs)

    @staticmethod
    def _convert_to_dpconfig(
        dict_config: Optional[Mapping[str, Any]] = None
    ) -> Optional[DPModellerConfig]:
        """Converts a dict-based configuration into a DPModellerConfig.

        If the configuration is None, will be returned as-is.
        """
        if dict_config:
            return DPModellerConfig(**dict_config)
        else:
            return None

    def apply_pod_dp(self, pod_dp_config: Optional[DPPodConfig]) -> None:
        """Applies pod-based DP caps and bounds to configuration options.

        Args:
            pod_dp_config: Pod-based configuration related to DP.
        """
        if not self._dp_config:  # DP not being used
            return
        if not pod_dp_config:
            logger.info("No pod DP preferences, using modeller preferences.")
            return

        # Modify maximum epsilon budget based on pod cap
        if self._dp_config.max_epsilon > pod_dp_config.max_epsilon:
            logger.warning(
                f"Requested DP max epsilon ({self._dp_config.max_epsilon}) exceeds "
                f"maximum value allowed by pod. Using pod max of "
                f"{pod_dp_config.max_epsilon}."
            )
            self._dp_config.max_epsilon = pod_dp_config.max_epsilon

        # Modify maximum target delta based on pod cap
        if self._dp_config.target_delta > pod_dp_config.max_target_delta:
            logger.warning(
                f"Requested DP target delta ({self._dp_config.target_delta}) exceeds "
                f"maximum value allowed by pod. Using pod max of "
                f"{pod_dp_config.max_target_delta}."
            )
            self._dp_config.target_delta = pod_dp_config.max_target_delta

    class _Schema(MarshmallowSchema):
        # Two fields are needed to keep the config field private
        _dp_config = fields.Nested(
            desert.schema(DPModellerConfig),
            allow_none=True,
            data_key="dp_config",
            dump_only=True,
        )
        dp_config = fields.Nested(
            desert.schema(DPModellerConfig),
            allow_none=True,
            data_key="dp_config",
            load_only=True,
        )
