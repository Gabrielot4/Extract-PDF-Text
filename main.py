## IMPORTAR E EXTRAIR TEXTO DE APENAS 1 PDF

"""import PyPDF2

pdfFileObj = open("pdf1.pdf", 'rb')                     ### rb = read binary mode
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)            ### ler o pdf
pages = pdfReader.numPages                              ### pega n0 de pág do pdf
print(f'Este PDF possui {pages} páginas.')

listaPages = []
for i in range(1,pages):
    pagesPDF = pdfReader.getPage(i)                     ### armazena cada página do pdf na variável
    extractedText = pagesPDF.extractText()              ### extrai o texto em formato de string e armazena na variável
    listaPages.append(extractedText)                    ### coloca em uma lista os textos das páginas
print(listaPages)
"""


## IMPORTAR TODOS DOS PDFS DO DIRETÓRIO

import PyPDF2, os

pdfFiles = []
for arquivo in os.listdir('.'):
    if arquivo.endswith('.pdf'):
        pdfFiles.append(arquivo)
print(f'Estes são os PDFs no diretório atual: {pdfFiles} \n')

for file in pdfFiles:
    pdfFileObj = open(file, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    pages = pdfReader.numPages
    print(f'Este PDF possui {pages} páginas. \n')

    listPages = []
    for page in range(1, pages):
        pageText = pdfReader.getPage(page)
        extractedPageText = pageText.extractText()
        listPages.append(extractedPageText)
    print(listPages)