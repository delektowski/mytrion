import paramiko


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
