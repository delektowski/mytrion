from display_responses import DisplayResponses
from parse_xml import ParseXml

xml_file = 'scanner.xml'
parsed_xml = ParseXml(xml_file)
hosts = parsed_xml.get_hosts()
commands = parsed_xml.get_commands()

display_responses = DisplayResponses(hosts, commands)
display_responses.execute_commands()

