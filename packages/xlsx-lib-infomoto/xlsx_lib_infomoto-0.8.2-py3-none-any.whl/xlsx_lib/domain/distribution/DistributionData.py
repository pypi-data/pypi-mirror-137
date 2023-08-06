from typing import List, Optional

from camel_model.camel_model import CamelModel

from xlsx_lib.domain.distribution.DataBlock import DataBlock


class DistributionData(CamelModel):
    subtitle: Optional[str]
    blocks: List[DataBlock] = []
