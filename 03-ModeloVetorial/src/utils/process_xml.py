import os
from xml.etree import ElementTree


class ProcessXML:
    def __init__(self):
        self.dom = None
        self.outfile = None

    def config_file_to_parse(self, file):
        self.dom = ElementTree.parse(file)

    def open_output_file(self, file, header):
        self.outfile = open(file, 'w')
        if header != '':
            self.write_in_file(header)

    def write_in_file(self, line):
        self.outfile.write(line + '\n')

    def close_file(self):
        self.outfile.close()

    def findall(self, parameter):
        return self.dom.findall(parameter)
