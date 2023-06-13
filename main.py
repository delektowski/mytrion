from display_responses import DisplayResponses
from parse_xml import ParseXml

if __name__ == "__main__":
    xml_file = 'scanner.xml'
    parsed_xml = ParseXml(xml_file)
    hosts = parsed_xml.get_hosts()
    commands = parsed_xml.get_commands()

    responses = DisplayResponses(hosts, commands)
    responses.display_table()

