from os import path

from src.utils.format_text import format_text
from utils.logging_format import config_log, log
from utils.process_xml import ProcessXML
from nltk.tokenize import word_tokenize


class GeradorListaInvertida:

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

    def read_config_file(self):
        log(f'Lendo arquivo de configuração {self.configfile}')
        file = open(self.configfile, 'r')
        for line in file:
            split = line.rstrip("\n").split('=')
            if split[0] == 'LEIA':
                self.options[split[0]].append(path.abspath(path.join(self.source_path, split[1])))
            else:
                self.options[split[0]] = path.abspath(path.join(self.destination_path, split[1]))
        log(f'Arquivos a serem lidos: {self.options["LEIA"]}')
        log(f'Arquivo de saída: {self.options["ESCREVA"]}')
        log(f'Leitura do arquivo de configuração concluída.')

    def gerar_lista_invertida(self):
        hash_words = {}
        for file in self.options['LEIA']:
            self.process_xml.config_file_to_parse(file)
            records = self.process_xml.findall('RECORD')

            for record in records:
                document_id = record.find('RECORDNUM').text
                document_abstract = record.find('ABSTRACT')
                if document_abstract is None:
                    document_abstract = record.find('EXTRACT')

                if document_abstract is not None:
                    for word in word_tokenize(document_abstract.text):
                        formatted_word = format_text(word)
                        if formatted_word not in hash_words:
                            hash_words[formatted_word] = []
                        hash_words[formatted_word].append(document_id.strip())

        for word in hash_words:
            self.process_xml.write_in_file(f'{word};{hash_words[word]}')

    def start(self):
        log('Iniciando execução do gerador de lista invertida')

        log('Iniciando leitura de arquivos de configuração')
        self.read_config_file()
        log('Leitura de arquivos de configuração finalizada')

        log('Configurando o parser de XML')
        self.process_xml = ProcessXML()
        self.process_xml.open_output_file(file=self.options['ESCREVA'], header='')
        log('Parser de XML configurado')

        self.gerar_lista_invertida()

        log('Execução do gerador de lista invertida finalizado')


processador_consulta = GeradorListaInvertida(configfile='./configfiles/GLI.CFG',
                                             source_path='./data',
                                             destination_path='../RESULT')

processador_consulta.start()
