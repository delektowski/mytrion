from datetime import datetime, date

from rich.console import Console
from rich.table import Table


class CliTable:

    def __init__(self, columns, rows):
        self.columns = columns
        self.rows = rows

    @staticmethod
    def is_valid_date(value):
        try:
            datetime.strptime(value, "%B %d, %Y")
            return True
        except ValueError:
            return False

    @staticmethod
    def is_date_past(date_string):
        date_object = datetime.strptime(date_string, "%B %d, %Y").date()
        current_date = date.today()
        if date_object > current_date:
            return False
        elif date_object < current_date:
            return True
        else:
            return True

    @staticmethod
    def style_cell(cells):
        styled_cells = []
        for index, cell in enumerate(cells):
            if index != 0 and CliTable.is_valid_date(cell) and CliTable.is_date_past(cell):
                cell = f"[red]{cell}"
            else:
                cell = f"[green]{cell}"
            styled_cells.append(cell)
        return styled_cells

    def set_table(self):
        console = Console()
        table = Table(show_header=True, header_style="bold magenta")
        for column in self.columns:
            table.add_column(column, width=30)

        for row in self.rows:
            CliTable.style_cell(row)
            table.add_row(*CliTable.style_cell(row))

        console.print(table)
