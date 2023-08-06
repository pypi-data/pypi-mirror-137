from typing import Generator

from dkist_processing_common.models.tags import Tag
from dkist_processing_common.parsers.quality import L0QualityFitsAccess
from dkist_processing_common.tasks import QualityL0Metrics


class TestQualityL0Metrics(QualityL0Metrics):
    def run(self) -> None:
        frames: Generator[L0QualityFitsAccess, None, None] = self.fits_data_read_fits_access(
            tags=[Tag.input()],
            cls=L0QualityFitsAccess,
        )
        self.calculate_l0_metrics(frames=frames)
