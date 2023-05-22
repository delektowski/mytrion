from cli_table import CliTable
from execute_command import ExecuteCommand
from host_data import HostData
from parse_xml import ParseXml

xml_file = 'scanner.xml'
parse_xml = ParseXml(xml_file)
hosts = parse_xml.get_hosts()
commands = parse_xml.get_commands()
columns = ["User", "Last password change", "Password expires", "Password inactive", "Account expires"]
rows = [["koza", "koza", "koza", "koza", "koza", ], ["koza", "koza", "koza", "koza", "koza", ] ]
table = CliTable(columns, rows)
# table.set_table()
for host in hosts:
    host_data = HostData(host)

    execute_command = ExecuteCommand(host=host_data.handle_host_data()["ip"],
                                     special_account=host_data.handle_host_data()["user"],
                                     pkey_file=host_data.handle_host_data()["pkey"],
                                     commands=commands)
    execute_command.exec_cmd()
