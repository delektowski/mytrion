from custom_exception import CustomException


class HostData:

    def __init__(self, host):

        self.host = host

    def get_credentials(self):
        credential = self.host.find("credentials")
        pkey_file_path = credential.find("pkey_file").text
        return pkey_file_path

    def get_ip(self):
        return self.host.attrib["ip"]

    def get_root(self):
        users = self.host.find("users")
        for user in users:
            if user.attrib["type"] == "root":
                return user.text
            else:
                raise CustomException("Provide a root to xml!")

    def handle_host_data(self):
        host_data = {"ip": self.get_ip(), "pkey": self.get_credentials(),
                     "user": self.get_root()}
        return host_data
