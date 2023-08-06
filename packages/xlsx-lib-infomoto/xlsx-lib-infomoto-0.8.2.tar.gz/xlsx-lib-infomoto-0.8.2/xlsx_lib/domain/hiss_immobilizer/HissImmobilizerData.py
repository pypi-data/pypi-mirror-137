from typing import List

from camel_model.camel_model import CamelModel

from xlsx_lib.domain.shared.TextLine import TextLine
from xlsx_lib.domain.hiss_immobilizer.Problem import Problem


class HissImmobilizerData(CamelModel):
    key_cloning_steps: List[TextLine] = list()
    errors: List[TextLine] = list()
    problems: List[Problem] = list()
    key_coding_problems: List[Problem] = list()
