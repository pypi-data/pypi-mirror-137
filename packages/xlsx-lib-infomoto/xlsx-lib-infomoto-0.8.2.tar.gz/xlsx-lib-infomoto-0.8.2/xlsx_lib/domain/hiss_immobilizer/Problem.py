from typing import Optional

from camel_model.camel_model import CamelModel


class Problem(CamelModel):
    code: Optional[str]
    description: Optional[str]
    causes_and_solutions: Optional[str]
