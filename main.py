from cli_table import CliTable
from execute_command import ExecuteCommand
from extract_data import ExtractData
from host_data import HostData
from parse_xml import ParseXml

xml_file = 'scanner.xml'
parse_xml = ParseXml(xml_file)
hosts = parse_xml.get_hosts()
commands = parse_xml.get_commands()

for host in hosts:
    host_data = HostData(host)
    execute_command = ExecuteCommand(host=host_data.handle_host_data()["ip"],
                                     special_account=host_data.handle_host_data()["user"],
                                     pkey_file=host_data.handle_host_data()["pkey"],
                                     commands=commands)
    resp = execute_command.exec_cmd()
    extract_data = ExtractData(resp)
    title_value_dict = extract_data.set_title_value_pairs()
    title_value_dict["user"] = "test"
    columns = list(title_value_dict.keys())
    rows = [list(title_value_dict.values())]
    table = CliTable(columns, rows)
    table.set_table()
