from dataclasses import dataclass
from dataclasses import field
from typing import Generator
from typing import List
from typing import Optional

import numpy as np
from astropy.time import Time
from dkist_processing_common.models.tags import StemName
from dkist_processing_common.parsers.quality import L0QualityFitsAccess
from dkist_processing_common.parsers.quality import L1QualityFitsAccess
from dkist_processing_common.tasks import QualityL0Metrics
from dkist_processing_common.tasks.mixin.quality import QualityMixin

from dkist_processing_visp.models.tags import VispTag
from dkist_processing_visp.parsers.visp_quality_fits_access import VispL1QualityFitsAccess
from dkist_processing_visp.tasks.visp_base import VispScienceTask


@dataclass
class _QualityData:
    datetimes: List[str] = field(default_factory=list)
    Q_RMS_noise: List[float] = field(default_factory=list)
    U_RMS_noise: List[float] = field(default_factory=list)
    V_RMS_noise: List[float] = field(default_factory=list)
    intensity_values: List[float] = field(default_factory=list)


@dataclass
class _QualityTaskTypeData:
    quality_task_type: str
    average_values: List[float] = field(default_factory=list)
    rms_values_across_frame: List[float] = field(default_factory=list)
    datetimes: List[str] = field(default_factory=list)

    @property
    def has_values(self) -> bool:
        return bool(self.average_values)


class VispL0QualityMetrics(VispScienceTask, QualityL0Metrics):
    def run(self) -> None:
        if not self.constants.correct_for_polarization:
            frames: Generator[L0QualityFitsAccess, None, None] = self.fits_data_read_fits_access(
                tags=[VispTag.input()],
                cls=L0QualityFitsAccess,
            )
            self.calculate_l0_metrics(frames=frames)
        else:
            for m in range(1, self.constants.num_modstates + 1):
                frames: Generator[
                    L0QualityFitsAccess, None, None
                ] = self.fits_data_read_fits_access(
                    tags=[VispTag.input(), VispTag.modstate(m)],
                    cls=L0QualityFitsAccess,
                )
                self.calculate_l0_metrics(frames=frames, modstate=m)


class VispL1QualityMetrics(VispScienceTask, QualityMixin):
    def run(self) -> None:
        with self.apm_step("Calculating L1 ViSP quality metrics"):
            if self.constants.correct_for_polarization:
                self.compute_polarimetric_metrics()
        self.compute_noise()

    def compute_polarimetric_metrics(self) -> None:
        with self.apm_step("Calculating polarization metrics"):
            all_datetimes = []
            all_Q_RMS_noise = []
            all_U_RMS_noise = []
            all_V_RMS_noise = []
            all_pol_sens_values = []
            for drep in range(1, self.constants.num_dsps_repeats + 1):
                polarization_data = _QualityData()
                for step in range(1, self.constants.num_raster_steps + 1):

                    # grab stokes I data
                    stokesI_frame = next(
                        self.fits_data_read_fits_access(
                            tags=[
                                VispTag.output(),
                                VispTag.frame(),
                                VispTag.raster_step(step),
                                VispTag.dsps_repeat(drep),
                                VispTag.stokes("I"),
                            ],
                            cls=VispL1QualityFitsAccess,
                        )
                    )
                    stokesI_data = stokesI_frame.data
                    polarization_data.datetimes.append(Time(stokesI_frame.time_obs).mjd)
                    polarization_data.intensity_values.append(np.max(stokesI_data))

                    # grab other stokes data and find and store RMS noise
                    for stokes_param, data_list in zip(
                        ("Q", "U", "V"),
                        (
                            polarization_data.Q_RMS_noise,
                            polarization_data.U_RMS_noise,
                            polarization_data.V_RMS_noise,
                        ),
                    ):
                        stokes_frame = next(
                            self.fits_data_read_fits_access(
                                tags=[
                                    VispTag.output(),
                                    VispTag.frame(),
                                    VispTag.raster_step(step),
                                    VispTag.dsps_repeat(drep),
                                    VispTag.stokes(stokes_param),
                                ],
                                cls=VispL1QualityFitsAccess,
                            )
                        )
                        # find Stokes RMS noise
                        data_list.append(np.std(stokes_frame.data / stokesI_data))

                all_datetimes.append(Time(np.mean(polarization_data.datetimes), format="mjd").isot)
                all_Q_RMS_noise.append(np.average(polarization_data.Q_RMS_noise))
                all_U_RMS_noise.append(np.average(polarization_data.U_RMS_noise))
                all_V_RMS_noise.append(np.average(polarization_data.V_RMS_noise))
                # find the polarimetric sensitivity of this drep (smallest intensity signal measured)
                polarimetric_sensitivity = 1 / np.max(polarization_data.intensity_values)
                all_pol_sens_values.append(polarimetric_sensitivity)

        with self.apm_step("Sending lists for storage"):
            for stokes_index, stokes_noise in zip(
                ("Q", "U", "V"), (all_Q_RMS_noise, all_U_RMS_noise, all_V_RMS_noise)
            ):
                self.quality_store_polarimetric_noise(
                    stokes=stokes_index, datetimes=all_datetimes, values=stokes_noise
                )
            self.quality_store_polarimetric_sensitivity(
                datetimes=all_datetimes, values=all_pol_sens_values
            )

    def compute_noise(self):
        for stokes in ["I", "Q", "U", "V"]:
            tags = [VispTag.output(), VispTag.frame(), VispTag.stokes(stokes)]
            if self.scratch.count_all(tags=tags) > 0:
                frames = self.fits_data_read_fits_access(
                    tags=tags,
                    cls=L1QualityFitsAccess,
                )
                noise_values = []
                datetimes = []
                for frame in frames:
                    noise_values.append(self.avg_noise(frame.data))
                    datetimes.append(frame.time_obs)
                self.quality_store_noise(datetimes=datetimes, values=noise_values, stokes=stokes)
