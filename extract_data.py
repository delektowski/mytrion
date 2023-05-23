import re


class ExtractData:

    def __init__(self, data):
        self.data_list = re.findall(r'.*$', data, re.MULTILINE)

    def set_title_value_pairs(self):
        title_value_pairs = {}
        for item in self.data_list:
            if ':' in item:
                title = item.split(':', 1)[0].strip()
                value = item.split(':', 1)[1].strip()
                title_value_pairs[title] = value

        return title_value_pairs
