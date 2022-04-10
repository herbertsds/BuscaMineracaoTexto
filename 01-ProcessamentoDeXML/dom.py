import os
from xml.etree import ElementTree

filename = 'cf79.xml'
file = os.path.abspath(os.path.join('data', filename))

dom = ElementTree.parse(file)

authors = dom.findall('RECORD/AUTHORS/AUTHOR')

outfile = open('autores', 'w')

for author in authors:
    authorName = author.text
    outfile.write(authorName + '\n')

outfile.close()
