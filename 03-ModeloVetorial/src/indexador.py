from os import path

from src.utils.format_text import format_text
from utils.logging_format import config_log, log

class Indexador:

    def __init__(self, configfile, source_path, destination_path):
        self.process_xml = None
        self.destination_path = destination_path
        self.source_path = source_path
        self.configfile = configfile
        self.options = {
            'LEIA': [],
            'ESCREVA': None
        }
        config_log(set_module='Gerador de Lista Invertida', file='../logs/gerador_lista_invertida.txt')