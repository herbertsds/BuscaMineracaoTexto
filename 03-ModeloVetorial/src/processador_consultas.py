from os import path
from utils.logging_format import config_log, log
from utils.process_xml import ProcessXML
from utils.format_text import format_text


class ProcessadorConsultas:

    def __init__(self, configfile, source_path, destination_path):
        self.process_xml = None
        self.destination_path = destination_path
        self.source_path = source_path
        self.configfile = configfile
        self.options = {}
        config_log(set_module='Processador de Consultas', file='../logs/processador_consulta.txt')

    def read_config_file(self):
        log(f'Lendo arquivo de configuração {self.configfile}')
        file = open(self.configfile, 'r')
        for line in file:
            split = line.rstrip("\n").split('=')
            if split[0] == 'LEIA':
                self.options[split[0]] = path.abspath(path.join(self.source_path, split[1]))
            else:
                self.options[split[0]] = path.abspath(path.join(self.destination_path, split[1]))
        log(f'Arquivo a ser lido: {self.options["LEIA"]}')
        log(f'Arquivo de consultas: {self.options["CONSULTAS"]}')
        log(f'Arquivo esperado: {self.options["ESPERADOS"]}')
        log(f'Leitura do arquivo de configuração concluída.')

    def processar_consultas(self):
        log('Iniciando o processamento das consultas')

        self.process_xml.open_output_file(file=self.options['CONSULTAS'], header='QueryNumber;QueryText')

        queries = self.process_xml.findall('QUERY')

        log('Escrevendo o corpo do arquivo')
        for query in queries:
            query_number = query.find('QueryNumber').text
            query_text = format_text(query.find('QueryText').text)
            self.process_xml.write_in_file(f'{query_number};{query_text}')

        self.process_xml.close_file()
        log('Processamento de consultas finalizado')

    def processar_esperados(self):
        log('Iniciando o processamento dos esperados')
        self.process_xml.open_output_file(file=self.options['ESPERADOS'], header='QueryNumber;DocNumber;DocVotes')

        queries = self.process_xml.findall('QUERY')

        log('Escrevendo o corpo do arquivo')
        for query in queries:
            query_number = query.find('QueryNumber').text
            records = query.findall('Records/Item')
            for item in records:
                doc_number = item.text
                doc_votes = 1
                self.process_xml.write_in_file(f'{query_number};{doc_number};{doc_votes}')

        self.process_xml.close_file()
        log('Processamento de esperados finalizado')

    def start(self):
        log('Iniciando execução do processador de consultas')

        log('Iniciando leitura de arquivos de configuração')
        self.read_config_file()
        log('Leitura de arquivos de configuração finalizada')

        log('Configurando o parser de XML')
        self.process_xml = ProcessXML()
        self.process_xml.config_file_to_parse(self.options['LEIA'])
        log('Parser de XML configurado')

        self.processar_consultas()
        self.processar_esperados()

        log('Execução do processador de consultas finalizado')


processador_consulta = ProcessadorConsultas(configfile='./configfiles/PC.CFG',
                                            source_path='./data',
                                            destination_path='../RESULT')

processador_consulta.start()
