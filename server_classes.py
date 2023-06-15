import paramiko
from custom_exception import CustomException


class ConnectServer:

    def __init__(self, host, special_account, pkey_file):
        self.host = host
        self.special_account = special_account
        self.pkey_file = pkey_file

    def __key_based_connect(self):
        pkey = paramiko.RSAKey.from_private_key_file(self.pkey_file)
        client = paramiko.SSHClient()
        policy = paramiko.AutoAddPolicy()
        client.set_missing_host_key_policy(policy)
        client.connect(self.host, username=self.special_account, pkey=pkey)
        return client

    def connection(self):
        connection = self.__key_based_connect()
        return connection


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

class HostData:

    def __init__(self, host):
        self.host = host

    def get_credentials(self):
        credential = self.host.find("credentials")
        pkey_file_path = credential.find("pkey_file").text
        return pkey_file_path

    def get_ip(self):
        return self.host.attrib["ip"]

    def get_root_user(self):
        users = self.host.find("users")
        for user in users:
            if user.attrib["type"] == "root":
                return user.text
            else:
                raise CustomException("Provide a root to xml!")

    def get_regular_users(self):
        users = self.host.find("users")
        regular_users = [regular_user for regular_user in users if regular_user.attrib["type"] == "regular"]
        return regular_users

    def handle_host_data(self):
        host_data = {"ip": self.get_ip(), "pkey": self.get_credentials(),
                     "user": self.get_root_user(), "users": self.get_regular_users()}
        return host_data