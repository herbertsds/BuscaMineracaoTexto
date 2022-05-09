import json
import math
from os import path
import csv
from src.utils.format_text import format_text
from src.utils.process_xml import ProcessXML
from utils.logging_format import config_log, log
import numpy as np

class Indexador:

    def __init__(self, configfile, source_path, destination_path, normalize):
        self.model = {}
        self.total_number_of_documents = 0
        self.inverted_list = {}
        self.process_xml = None
        self.destination_path = destination_path
        self.source_path = source_path
        self.configfile = configfile
        self.options = {}
        self.normalize = normalize
        config_log(set_module='Indexador', file='../logs/indexador.txt')

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
        log(f'Arquivo com modelo: {self.options["ESCREVA"]}')
        log(f'Leitura do arquivo de configuração concluída.')

    def csv_to_dictionary(self):
        log('Convertendo csv para um dicionário em python')
        with open(self.options['LEIA'], mode='r') as infile:
            reader = csv.reader(infile, delimiter=';')
            for row in reader:
                documents = np.array(np.matrix(row[1])).ravel()
                if row[0].isalpha() and len(row[0]) > 2:
                    self.inverted_list[row[0]] = documents
        log('Arquivo convertido')

    def calculate_number_of_documents(self):
        log('Calculando o número total de documentos do modelo')
        document_list = {}
        for term in self.inverted_list:
            for document in self.inverted_list[term]:
                if document not in document_list:
                    document_list[document] = 'a'
        self.total_number_of_documents = len(document_list)
        log(f'O número total de documentos é {self.total_number_of_documents}')

    def build_frequency_matrix(self):
        for term in self.inverted_list:
            if term not in self.model:
                self.model[term] = {}
            for document in self.inverted_list[term]:
                if document not in self.model[term]:
                    self.model[term][document] = 1
                else:
                    self.model[term][document] += 1

    def build_tf_idf_matrix(self):
        if self.normalize:
            def calculate_tf(tf_frequency):
                return 1 + math.log2(tf_frequency)
        else:
            def calculate_tf(tf_frequency):
                return tf_frequency

        def calculate_idf(idf_number_of_documents):
            return math.log2(self.total_number_of_documents / idf_number_of_documents)

        for term in self.model:
            number_of_documents = len(self.model[term])
            idf = calculate_idf(number_of_documents)
            for document in self.model[term]:
                frequency = self.model[term][document]
                tf = calculate_tf(frequency)
                self.model[term][document] = tf * idf

    def build_matrix_simplified(self):
        self.calculate_number_of_documents()
        self.build_frequency_matrix()
        self.build_tf_idf_matrix()

    def start(self):
        log('Iniciando execução do indexador')

        log('Iniciando leitura de arquivos de configuração')
        self.read_config_file()
        log('Leitura de arquivos de configuração finalizada')

        self.csv_to_dictionary()
        self.build_matrix_simplified()

        with open(self.options['ESCREVA'], "w") as write_file:
            json.dump(self.model, write_file, indent=4)

        log('Execução do indexador finalizado')


indexador = Indexador(configfile='./configfiles/INDEX.CFG', source_path='../RESULT', destination_path='../RESULT',
                      normalize=True)

indexador.start()
