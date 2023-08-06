import logging
from abc import ABC
from dataclasses import dataclass
from dataclasses import field
from inspect import signature
from typing import Callable
from typing import Generator
from typing import List
from typing import Optional

import numpy as np

from dkist_processing_common.models.tags import StemName
from dkist_processing_common.models.tags import Tag
from dkist_processing_common.parsers.quality import L0QualityFitsAccess
from dkist_processing_common.parsers.quality import L1QualityFitsAccess
from dkist_processing_common.tasks.base import WorkflowDataTaskBase
from dkist_processing_common.tasks.mixin.fits import FitsDataMixin
from dkist_processing_common.tasks.mixin.quality import QualityMixin


__all__ = ["QualityL1Metrics", "QualityL0Metrics"]


logger = logging.getLogger(__name__)


@dataclass
class _QualityTaskTypeData:
    quality_task_type: str
    average_values: List[float] = field(default_factory=list)
    rms_values_across_frame: List[float] = field(default_factory=list)
    datetimes: List[str] = field(default_factory=list)

    @property
    def has_values(self) -> bool:
        return bool(self.average_values)


class QualityL0Metrics(WorkflowDataTaskBase, FitsDataMixin, QualityMixin, ABC):
    def calculate_l0_metrics(
        self, frames: Generator[L0QualityFitsAccess, None, None], modstate: Optional[int] = None
    ):

        # determine quality metrics to calculate base upon task types defined in the quality mixin
        quality_task_type_data = [
            _QualityTaskTypeData(quality_task_type=t) for t in self.quality_task_types
        ]

        with self.apm_step("Calculating L0 quality metrics"):
            for frame in frames:

                # We grab the task name
                tags = self.tags(frame.name)
                task_type = [t.replace(f"{StemName.task.value}_", "") for t in tags if "TASK" in t][
                    0
                ]

                for quality_task_type_datum in quality_task_type_data:
                    if task_type.lower() == quality_task_type_datum.quality_task_type.lower():
                        # find the rms across frame
                        squared_mean = np.nanmean(frame.data.astype(np.float64) ** 2)
                        normalized_rms = np.sqrt(squared_mean) / frame.exposure_time
                        quality_task_type_datum.rms_values_across_frame.append(normalized_rms)
                        # find the average value across frame
                        quality_task_type_datum.average_values.append(
                            np.nanmean(frame.data) / frame.exposure_time
                        )
                        quality_task_type_datum.datetimes.append(frame.time_obs)

        with self.apm_step("Sending lists for storage"):
            for quality_task_type_datum in quality_task_type_data:
                if quality_task_type_datum.has_values:
                    self.quality_store_frame_average(
                        datetimes=quality_task_type_datum.datetimes,
                        values=quality_task_type_datum.average_values,
                        task_type=quality_task_type_datum.quality_task_type,
                        modstate=modstate,
                    )
                    self.quality_store_frame_rms(
                        datetimes=quality_task_type_datum.datetimes,
                        values=quality_task_type_datum.rms_values_across_frame,
                        task_type=quality_task_type_datum.quality_task_type,
                        modstate=modstate,
                    )
                    self.quality_store_dataset_average(
                        task_type=quality_task_type_datum.quality_task_type,
                        frame_averages=quality_task_type_datum.average_values,
                    )
                    self.quality_store_dataset_rms(
                        task_type=quality_task_type_datum.quality_task_type,
                        frame_rms=quality_task_type_datum.rms_values_across_frame,
                    )


class L1Metric:
    """
    Class for collecting L1 quality metric data while frames are being opened before storing on disk
    """

    def __init__(
        self,
        storage_method: Callable,
        value_source: str,
        value_function: Optional[Callable] = None,
    ):
        self.storage_method = storage_method
        self.value_source = value_source
        self.values = []
        self.datetimes = []
        self.value_function = value_function

    def append_value(self, frame: L1QualityFitsAccess):
        """
        Append datetime from the frame to the list of datetimes.
        If a value_function was provided, apply it to the given source attribute and append to
        self.values. Otherwise, append the attribute value itself to self.values.
        """
        self.datetimes.append(frame.time_obs)
        if self.value_function:
            self.values.append(self.value_function(getattr(frame, self.value_source)))
            return
        self.values.append(getattr(frame, self.value_source))

    @property
    def has_values(self):
        return any(self.values)

    def store_metric(self):
        """
        Remove None values from the values list (and also remove corresponding indices from
        datetimes) then send to the provided storage method.
        """
        # Get indices of non-None values and only use those
        indices = [i for i, val in enumerate(self.values) if val is not None]
        d = [self.datetimes[i] for i in indices]
        v = [self.values[i] for i in indices]
        # Get signature of storage method and call with applicable args
        storage_method_sig = signature(self.storage_method)
        if storage_method_sig.parameters.get("datetimes", False):
            self.storage_method(datetimes=d, values=v)
            return
        self.storage_method(values=v)


class QualityL1Metrics(WorkflowDataTaskBase, FitsDataMixin, QualityMixin):
    def run(self) -> None:
        metrics = [
            L1Metric(
                storage_method=self.quality_store_fried_parameter,
                value_source="fried_parameter",
            ),
            L1Metric(storage_method=self.quality_store_light_level, value_source="light_level"),
            L1Metric(storage_method=self.quality_store_health_status, value_source="health_status"),
            L1Metric(storage_method=self.quality_store_ao_status, value_source="ao_status"),
        ]

        frames: Generator[L1QualityFitsAccess, None, None] = self.fits_data_read_fits_access(
            tags=[Tag.output(), Tag.frame()], cls=L1QualityFitsAccess
        )

        with self.apm_step("Calculating L1 quality metrics"):
            for frame in frames:
                for metric in metrics:
                    metric.append_value(frame=frame)

        with self.apm_step("Sending lists for storage"):
            for metric in metrics:
                if metric.has_values:
                    metric.store_metric()
