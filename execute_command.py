from connect_server import ConnectServer


class ExecuteCommand(ConnectServer):

    def __init__(self, host, special_account, pkey_file, commands):
        super().__init__(host=host, special_account=special_account, pkey_file=pkey_file)
        self.commands = commands

    def exec_cmd(self):
        responses = []
        for command in self.commands:
            _stdin, _stdout, _stderr = self.connection().exec_command(command)
            response = _stdout.read().decode()
            responses.append(response)
        return responses