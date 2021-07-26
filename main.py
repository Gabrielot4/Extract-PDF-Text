## IMPORTAR E EXTRAIR TEXTO DE APENAS 1 PDF

import PyPDF2

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

### SUBSTITUIR SUBSTRINGS \n DA LISTA

import re                                                               ### re = regular expressions
listPages = [re.sub("\n", '', string) for string in listaPages]         ### para string em listaPages, substituo a substring '\n' por '' em cada item da lista
print(listPages)

stringUnica = ' '.join(listPages)                                        ### junto todos os itens da lista em uma string só
print(stringUnica, '\n')

### PRÉ-PROCESSAMENTO DO TEXTO

## LOWERCASE TEXT, ONLY
stringUnica = stringUnica.lower()
print(stringUnica, '\n')

## TOKENIZATION
from nltk.tokenize import word_tokenize, RegexpTokenizer                 ### tokenizar a stringUnica, tokenizar por meio de Regular Expression
from nltk.util import ngrams                                             ### tokenizar em 3 grams


tokens = word_tokenize(stringUnica)
print(' - - TOKENS: ')
print(tokens, '\n')

threegrams = list(ngrams(tokens, 3))
print(' - - 3 GRAMS:')
print(threegrams, '\n')
threegramsUnicas = [' '.join(i) for i in threegrams]                    ### junta os 3 grams para ser possível extrair o valor das indenizações
print(threegramsUnicas, '\n')

tokenSpace = RegexpTokenizer('\s+', gaps=True)                          ### outra forma de extrair os valores das indenizações mais facilmente
print(tokenSpace.tokenize((stringUnica)), '\n')
#tokenSpaceUnica = ' '.join(tokenSpace.tokenize(stringUnica))            ### estou juntando tudo em uma string só para usar o CountVectorizer com tudo minúsculo, poderia fazer isso com as tokenizações threegrams e tokens também
#print(tokenSpaceUnica)

## REMOVE STOPWORDS
from nltk.corpus import stopwords
print(stopwords.words('portuguese'))

stopWords = stopwords.words('portuguese')
stopLambda = lambda text: [word for word in text if word not in stopWords]         ### Retorna as palavras que não estão na lista de stopwords do português
tokenSpaceSW = stopLambda(tokenSpace.tokenize(stringUnica))                        ### retiro as stopwords do texto com tokenização por espaço, usado na tokenização com regular expressions
print(tokenSpaceSW)












"""## IMPORTAR TODOS DOS PDFS DO DIRETÓRIO

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
    print(listPages)"""