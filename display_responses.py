from cli_table import CliTable
from execute_command import ExecuteCommand
from extract_data import ExtractData
from host_data import HostData


class DisplayResponses:

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

    def __handle_table_data(self, responses, host_user):
        for resp in responses:
            extract_data = ExtractData(resp)
            title_value_dict = extract_data.set_title_value_pairs()
            title_value_dict["User"] = host_user.text
            if len(self.columns) == 0:
                self.columns = list(title_value_dict.keys())
            self.rows.append(list(title_value_dict.values()))

    def __execute_commands(self):
        for host in self.hosts:
            host_data = HostData(host)
            host_users = host_data.get_regular_users()
            for host_user in host_users:
                execute_commands = ExecuteCommand(host=host_data.handle_host_data()["ip"],
                                                  special_account=host_data.handle_host_data()["user"],
                                                  pkey_file=host_data.handle_host_data()["pkey"],
                                                  commands=DisplayResponses.handle_bind_command_to_user(self.commands,
                                                                                                        host_user))
                responses = execute_commands.exec_cmd()
                self.__handle_table_data(responses, host_user)

    def display_table(self):
        self.__execute_commands()
        table = CliTable(self.columns, self.rows)
        table.set_table()
