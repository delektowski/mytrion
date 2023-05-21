import xml.etree.ElementTree as ET


class ParseXml:

    def __init__(self, xml_file):
        self.root = ET.parse(xml_file).getroot()

    def get_commands(self):
        commands_root = self.root.find('commands')
        command_elements = [commands for commands in commands_root]
        return command_elements

    def get_hosts(self):
        hosts_root = self.root.find('hosts')
        host_elements = [hosts for hosts in hosts_root]
        return host_elements
