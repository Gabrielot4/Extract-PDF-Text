## IMPORTAR TODOS DOS PDFS DO DIRETÓRIO

import PyPDF2, os

pdfsList_corpus = []                                                                                                           ### lista que vai conter os pdfs pré-processados
pdfFiles = []                                                                                                           ### lista que vai onter os pdfs brutos, sem pré-processamento
for arquivo in os.listdir('.'):                                                                                         ### arquivos devem estar no diretorio onde está salvo esse código
    if arquivo.endswith('.pdf'):
        pdfFiles.append(arquivo)
print(f'Estes são os PDFs no diretório atual: {pdfFiles} \n')

textFile = open('most_frequent_words.txt', 'w')                                                                         ### criar um arquivo

for file in pdfFiles:
    pdfFileObj = open(file, 'rb')                                                                                       ### rb = read binary, para ler pdfs, que são arquivos binários
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    pages = pdfReader.numPages
    print(f'\033[1;30;43m Este PDF possui {pages} páginas.\033[m \n ')

    listPages = []                                                                                                      ### lista a conter os textos das páginas
    for page in range(1, pages):                                                                                        ### itera entre as páginas do PDF
        pageText = pdfReader.getPage(page)
        extractedPageText = pageText.extractText()                                                                      ### extrai texto da página
        listPages.append(extractedPageText)                                                                             ### adiciona o texto da página na lista
    print(listPages)

########## SUBSTITUIR AS SUBTRINGS '\n' DA LISTA ##########

    import re                                                                                                           ### re = regular expressions
    listPages = [re.sub("\n", '', string) for string in listPages]                                                      ### lista com as páginas do PDF sem \n
    print(listPages[:1], '\n')

    stringUnica = ' '.join(listPages)                                                                                   ### junta os itens da listPages em uma só string
    print('\033[1;33m - - TEXTO COMO UMA STRING SÓ: \033[m')
    print(stringUnica[:100], '\n')


#################### PRÉ-PROCESSAMENTO ####################

## LOWERCASE TEXT
    stringUnica = stringUnica.lower()
    print('\033[1;33m - - TEXTO COM MINÚSCULAS: \033[m')
    print(stringUnica[:100], '\n')

## TOKENIZATION
    from nltk.tokenize import word_tokenize, RegexpTokenizer

    space = RegexpTokenizer('\s+', gaps=True)                                                                           ### padrão é o \s+ para separar as palavras do texto
    tokenSpace = space.tokenize(stringUnica)                                                                            ### aplica o padrão na tokenização do texto
    print('\033[1;33m - - TOKENIZADO POR ESPAÇO: \033[m')
    print(tokenSpace, '\n')

## STOPWORDS
    from nltk.corpus import stopwords
    #print(stopwords.words('portuguese'))

    stopWords = stopwords.words('portuguese')
    stopLambda = lambda text: [word for word in text if word not in stopWords]                                          ### Retorna as palavras que não estão na lista de stopwords do português
    tokenSpaceSW = stopLambda(tokenSpace)                                                                               ### texto sem as stopwords
    print('\033[1;33m - - SEM STOPWORDS: \033[m')
    print(tokenSpaceSW, '\n')

## STEMMING
    from nltk.stem import SnowballStemmer                                                                               ### O LancasterStemmer é (mais agressivo)
    stemmer = SnowballStemmer('portuguese')                                                                             ### cria o stemmer com base na língua portuguesa

    stemLambda = lambda text: [stemmer.stem(text) for text in tokenSpaceSW]                                             ### retorna as palavras presentes em tokenSpaceSW reduzidas ao seu radical
    tokenSpaceSWStem = stemLambda(tokenSpaceSW)
    print('\033[1;33m - - STEMMIZADO: \033[m')
    print(tokenSpaceSWStem[:10], '\n')

## LISTA COM TEXTOS PRÉ-PROCESSADOS
    pdfsList_corpus.append(' '.join(tokenSpaceSWStem))

## MOST FREQUENT WORDS
    from collections import Counter

    wordCounts = Counter(tokenSpaceSWStem)
    wordCounts = list(zip(wordCounts.values(), wordCounts.keys()))                                                      ### coloca nesse padrão: (frequência, palavra)
    wordCounts = sorted(wordCounts, reverse=True)                                                                       ### ordem decrescente de frequência
    print('\033[1;33m - - PALAVRAS MAIS FREQUENTES: \033[m')
    print(wordCounts[:10], '\n')

## CRIAR ARQUIVO TXT PARA COLOCAR AS PALAVRAS MAIS FREQUENTES

    textFile = open('most_frequent_words.txt', 'r')
    cont = textFile.readlines()
    cont.append(str(wordCounts))
    cont.append('\n\n')
    textFile = open('most_frequent_words.txt', 'w')
    textFile.writelines(cont)
    textFile.close()

    print('\n')


print('\033[1;34m - - LISTA COM PDFS PRÉ-PROCESSADOS: \033[m')
#print(pdfsList, '\n')
print(f'Lista com {len(pdfsList_corpus)} textos pré-processados.', '\n')

## REALIZAR PROCEDIMENTO DE COSINE SIMILARITY COM TF-IDF (SIMILARIDADE DE TEXTOS)
import pandas as pd                                                                                                     ### para ser possível fazer a Document-term matrix
from sklearn.feature_extraction.text import TfidfVectorizer                                                             ### para fazer a matriz com base no TF-IDF

tfidf = TfidfVectorizer()
X_tfidf = tfidf.fit_transform(pdfsList_corpus).toarray()                                                                ### vetorizando cada texto em pdfsList, ou seja, cria a Document-term matrix
vectorsTFIDF = pd.DataFrame(X_tfidf, columns=tfidf.get_feature_names())
print('\033[1;33m - - DOCUMENT-TERM MATRIX \033[m')
print(vectorsTFIDF, '\n')




#### OBS: em vez de colocar as palavras mais frequentes em um txt, seria interessante colocar todos os documentos
# pré-processados, como string única em uma lista. Com isso, monta-se um corpus (vários documentos juntos), para
# depois fazer cálculos de similaridade entre documentos, TF-IDF, etc.