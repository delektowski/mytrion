from server_classes import ExecuteCommand
from data_extraction import DataExtraction
from server_classes import HostData
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

class TableResponseCreator:

    def __init__(self, hosts, commands):
        self.hosts = hosts
        self.commands = commands
        self.columns = []
        self.rows = []

    @staticmethod
    def handle_bind_command_to_user(cmds, user):
        updated_commands = []
        for command in cmds:
            if command.attrib["type"] == "bind-user":
                updated_commands.append(f"{command.text} {user.text}")
            else:
                updated_commands.append(command.text)
        return updated_commands

    @staticmethod
    def add_row_divider(columns_number):
        divider = []
        for column in range(columns_number):
            divider.append(" ")
        return divider

    def __handle_table_data(self, responses, host_user):
        for resp in responses:
            extract_data = DataExtraction(resp)
            title_value_dict = extract_data.set_title_value_pairs()
            title_value_dict["User"] = host_user.text
            if len(self.columns) == 0:
                self.columns = list(title_value_dict.keys())
            self.rows.extend([TableResponseCreator.add_row_divider(len(self.columns)), list(title_value_dict.values()),
                              TableResponseCreator.add_row_divider(len(self.columns))])

    def __execute_commands(self):
        for host in self.hosts:
            host_data = HostData(host)
            host_users = host_data.get_regular_users()
            for host_user in host_users:
                execute_commands = ExecuteCommand(host=host_data.handle_host_data()["ip"],
                                                  special_account=host_data.handle_host_data()["user"],
                                                  pkey_file=host_data.handle_host_data()["pkey"],
                                                  commands=TableResponseCreator.handle_bind_command_to_user(self.commands,
                                                                                                        host_user))
                responses = execute_commands.exec_cmd()
                self.__handle_table_data(responses, host_user)

    def display_table(self):
        self.__execute_commands()
        table = CliTable(self.columns, self.rows)
        table.set_table()
