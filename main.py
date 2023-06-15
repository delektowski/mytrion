if __name__ == "__main__":
    from table_classes import TableResponseCreator
    from parser_xml import ParserXml
    
    xml_file = 'scanner.xml'
    parsed_xml = ParserXml(xml_file)
    hosts = parsed_xml.get_hosts()
    commands = parsed_xml.get_commands()

    responses = TableResponseCreator(hosts, commands)
    responses.display_table()

