from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.cell import Cell
from typing import List, Optional

from xlsx_lib.domain.shared.TextLine import TextLine
from xlsx_lib.domain.hiss_immobilizer.HissImmobilizerData import HissImmobilizerData
from xlsx_lib.domain.hiss_immobilizer.Problem import Problem
from xlsx_lib.domain.hiss_immobilizer.HissImmobilizerCellValueKind import HissImmobilizerCellValueKind
from xlsx_lib.domain.xlsx_elements.sheet import Sheet

from xlsx_lib.domain.xlsx_elements.exceptions.continue_exception import ContinueException
from xlsx_lib.domain.xlsx_elements.exceptions.sheet_end_exception import SheetEndException


def get_hiss_immobilizer_cell_value_kind(cell: Cell) -> HissImmobilizerCellValueKind:
    if cell.font.b and cell.alignment.horizontal == "center":
        try:
            return {
                "CLONADO NUEVAS LLAVES": HissImmobilizerCellValueKind.KEY_CLONING_TITLE,
                "ERRORES SISTEMA INMOVILIZADOR HISS": HissImmobilizerCellValueKind.ERRORS_COLUMN_TITLE,
                "PROBLEMA": HissImmobilizerCellValueKind.PROBLEMS_COLUMN_TITLE,
                "PROBLEMAS CON EL CODIFICADO DE LLAVES": HissImmobilizerCellValueKind.KEY_CODING_PROBLEMS_COLUMN_TITLE,
            }[cell.value]
        except KeyError:
            raise ContinueException
    else:
        return HissImmobilizerCellValueKind.CONTENT


class HissImmobilizerSheet(Sheet):
    def __init__(
            self,
            worksheet: Worksheet,
    ):
        self.hiss_immobilizer_data: HissImmobilizerData = HissImmobilizerData()

        self.content_found: bool = False
        self.key_cloning_steps_found: bool = False
        self.errors_found: bool = False
        self.problems_found: bool = False
        self.key_coding_problems_found: bool = False

        super().__init__(
            worksheet=worksheet,
            end_of_sheet_rows_limit=20,
            start_col=1,
            start_row=0,
        )

        self.process_data()

    def process_data(self) -> None:
        col_index: int = self.start_col
        row_index: int = self.start_row

        while True:
            cell: Cell = self.sheet_reader.read_cell(col_index, row_index)

            try:
                self.process_cell(cell, col_index, row_index)
            except ContinueException:
                row_index += 1
                continue
            except SheetEndException:
                break

            row_index += 1

    def process_cell(self, cell: Cell, col_index: int, row_index: int):
        first_cell_value = self.sheet_reader.read_cell(
            col=0,
            row=row_index,
        ).value

        if cell.value is None and first_cell_value is None:
            self.check_next_values(row=row_index)
            raise ContinueException

        cell_value_type = get_hiss_immobilizer_cell_value_kind(cell)

        if self.content_found and cell_value_type is HissImmobilizerCellValueKind.CONTENT:
            self.process_row(0, row_index)

        elif cell_value_type is HissImmobilizerCellValueKind.KEY_CLONING_TITLE:
            self.key_cloning_steps_found = True
            self.content_found = True

        elif cell_value_type is HissImmobilizerCellValueKind.ERRORS_COLUMN_TITLE:
            self.errors_found = True
            self.content_found = True

        elif cell_value_type is HissImmobilizerCellValueKind.PROBLEMS_COLUMN_TITLE:
            self.problems_found = True
            self.content_found = True

        elif cell_value_type is HissImmobilizerCellValueKind.KEY_CODING_PROBLEMS_COLUMN_TITLE:
            self.key_coding_problems_found = True
            self.content_found = True

    def process_row(
            self,
            col: int,
            row: int,
    ) -> None:
        values: List[str] = self.sheet_reader.read_cells_values(
            col,
            col + 2,
            row,
            row
        )

        if self.key_coding_problems_found:
            self.hiss_immobilizer_data.key_coding_problems.append(
                Problem(
                    code=values[0],
                    description=values[1],
                    causes_and_solutions=values[2]
                )
            )
        elif self.problems_found:
            self.hiss_immobilizer_data.problems.append(
                Problem(
                    code=values[0],
                    description=values[1],
                    causes_and_solutions=values[2]
                )
            )
        elif self.errors_found:
            self.hiss_immobilizer_data.errors.append(
                TextLine(text=values[0])
            )
        elif self.key_cloning_steps_found:
            self.hiss_immobilizer_data.key_cloning_steps.append(
                TextLine(text=values[0])
            )

    def check_next_values(
            self,
            row: int,
            rows_checked: Optional[int] = None,
            continue_mode: bool = False,
    ) -> None:
        if rows_checked is None:
            rows_checked = self.end_of_sheet_rows_limit

        content_cells: List[Cell] = self.sheet_reader.read_cells(
            start_row=row + 1,
            end_row=row + rows_checked,
            start_col=0,
        )

        content_cells_matches: int = len(
            [cell for cell in content_cells
             if cell.value is not None
             and get_hiss_immobilizer_cell_value_kind(cell) is HissImmobilizerCellValueKind.CONTENT])

        if content_cells_matches == 0:
            if continue_mode:
                raise ContinueException

            raise SheetEndException

