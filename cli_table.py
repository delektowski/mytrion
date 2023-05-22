from rich.console import Console
from rich.table import Table


class CliTable:

    def __init__(self, columns, rows):
        self.columns = columns
        self.rows = rows

    def set_table(self):
        console = Console()
        table = Table(show_header=True, header_style="bold magenta")
        for column in self.columns:
            table.add_column(column, width=30)

        for row in self.rows:
            table.add_row(*row)

        console.print(table)
