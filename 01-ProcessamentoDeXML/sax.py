import os
from pickle import FALSE, TRUE
import xml.sax

filename = 'cf79.xml'
file = os.path.abspath(os.path.join('data', filename))

outfile = open('titulo', 'w')

class XMLHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.CurrentData = ""
        self.isRunning = FALSE
        self.titleName = ""

    # Quando acha a abertura de um novo elemento
    def startElement(self, tag, attributes):
        self.CurrentData = tag

    # Quando acha o fechamento do elemento
    def endElement(self, tag):
        if self.CurrentData == 'TITLE':
            outfile.write(self.titleName+'\n')
            self.titleName = ""

    # O conteúdo daquele elemento. 
    # Quando tem quebra de linha, reconhece como um novo conteúdo
    def characters(self, content):
        if self.CurrentData == "TITLE":
            self.titleName += content.replace('\n', ' ')

parser = xml.sax.make_parser()
parser.setFeature(xml.sax.handler.feature_namespaces, 0)

Handler = XMLHandler()
parser.setContentHandler(Handler)

parser.parse(file)

outfile.close()