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
print(listaPages[:1], '\n')

### SUBSTITUIR SUBSTRINGS \n DA LISTA

import re                                                               ### re = regular expressions
listPages = [re.sub("\n", '', string) for string in listaPages]         ### para string em listaPages, substituo a substring '\n' por '' em cada item da lista
print(listPages[:1], '\n')

stringUnica = ' '.join(listPages)                                        ### junto todos os itens da lista em uma string só
print(' - - TEXTO COMO UMA STRING SÓ: ')
print(stringUnica[:100], '\n')                                           ### printa os 100 primeiros caracteres, apenas (só para melhor visualização

### PRÉ-PROCESSAMENTO DO TEXTO

## LOWERCASE TEXT, ONLY
stringUnica = stringUnica.lower()
print(' - - TEXTO EM MINÚSCULAS: ')
print(stringUnica[:100], '\n')

## TOKENIZATION
from nltk.tokenize import word_tokenize, RegexpTokenizer                 ### tokenizar a stringUnica, tokenizar por meio de Regular Expression
from nltk.util import ngrams                                             ### tokenizar em 3 grams

"""tokens = word_tokenize(stringUnica)
print(' - - TOKENS: ')
print(tokens[:10], '\n')

threegrams = list(ngrams(tokens, 3))
print(' - - 3 GRAMS:')
print(threegrams[:10], '\n')
threegramsUnicas = [' '.join(i) for i in threegrams]                    ### junta os 3 grams para ser possível extrair o valor das indenizações, ex: R$10.000,00
print(threegramsUnicas, '\n')"""

tokenSpace = RegexpTokenizer('\s+', gaps=True)                          ### outra forma de extrair os valores das indenizações mais facilmente
print(' - - TOKENIZAÇÃO POR ESPAÇO:')
print(tokenSpace.tokenize((stringUnica)[:100]), '\n')
#tokenSpaceUnica = ' '.join(tokenSpace.tokenize(stringUnica))            ### estou juntando tudo em uma string só para usar o CountVectorizer com tudo minúsculo, poderia fazer isso com as tokenizações threegrams e tokens também
#print(tokenSpaceUnica)

## REMOVE STOPWORDS
from nltk.corpus import stopwords
#print(stopwords.words('portuguese'))

stopWords = stopwords.words('portuguese')
stopLambda = lambda text: [word for word in text if word not in stopWords]         ### Retorna as palavras que não estão na lista de stopwords do português
tokenSpaceSW = stopLambda(tokenSpace.tokenize(stringUnica))                        ### retiro as stopwords do texto com tokenização por espaço, usado na tokenização com regular expressions
print(' - - TEXTO SEM STOPWORDS:')
print(tokenSpaceSW, '\n')

## STEMMING
from nltk.stem import SnowballStemmer                                              ### Tem o LancasterStemmer (mais agressivo) também, mas é recomendado esse SnowballStemmer
stemmer = SnowballStemmer('portuguese')                                            ### cria o stemmer com base na língua portuguesa
stemLambda = lambda text: [stemmer.stem(text) for text in tokenSpaceSW]            ### percorre o texto tokenizado por espaço, removido as stopwords para reduzi-lo ao radical das palavras
tokenSpaceSWStem = stemLambda(tokenSpaceSW)
print(' - - TEXTO STEMMIZADO:')
print(tokenSpaceSWStem, '\n')

## MOST FREQUENT WORDS
from collections import Counter
wordCounts = Counter(tokenSpaceSWStem)
wordCounts = list(zip(wordCounts.values(), wordCounts.keys()))                     ### (frequência, palavra)
wordCounts = sorted(wordCounts, reverse=True)                                      ### ordem decrescente de frequência
print(' - - PALAVRAS MAIS FREQUENTES:')
print(wordCounts[:30])

wordCounts = [wordCounts]
textFile = open('pdf1.txt', 'w')
textFile.writelines(str(wordCounts))
