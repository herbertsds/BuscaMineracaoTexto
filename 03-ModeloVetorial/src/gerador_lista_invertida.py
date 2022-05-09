from os import path
from utils.logging_format import config_log, log
from utils.process_xml import ProcessXML


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
        config_log(set_module='Gerador de Lista Invertida', file='logs/gerador_lista_invertida.txt')

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
        for file in self.options['LEIA']:
            self.process_xml.config_file_to_parse(file)
            records = self.process_xml.findall('RECORD')

            abstract = records.find('ABSTRACT')
            print(abstract)

    def start(self):
        log('Iniciando execução do gerador de lista invertida')

        log('Iniciando leitura de arquivos de configuração')
        self.read_config_file()
        log('Leitura de arquivos de configuração finalizada')

        log('Configurando o parser de XML')
        self.process_xml = ProcessXML()
        self.process_xml.open_output_file(file=self.options['ESCREVA'], header='')
        log('Parser de XML configurado')

        self.processar_consultas()
        self.processar_esperados()

        log('Execução do processador de consultas finalizado')


processador_consulta = GeradorListaInvertida(configfile='./configfiles/GLI.CFG',
                                             source_path='./data',
                                             destination_path='../RESULT')

processador_consulta.start()
