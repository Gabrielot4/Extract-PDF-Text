## IMPORTAR TODOS DOS PDFS DO DIRETÓRIO

import PyPDF2, os

pdfFiles = []
for arquivo in os.listdir('.'):
    if arquivo.endswith('.pdf'):
        pdfFiles.append(arquivo)
print(f'Estes são os PDFs no diretório atual: {pdfFiles} \n')

textFile = open('most_frequent_words.txt', 'w')

for file in pdfFiles:
    pdfFileObj = open(file, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    pages = pdfReader.numPages
    print(f'\033[1;30;43m Este PDF possui {pages} páginas.\033[m \n ')

    listPages = []
    for page in range(1, pages):                                                                                        ### itera entre as páginas do PDF
        pageText = pdfReader.getPage(page)
        extractedPageText = pageText.extractText()                                                                      ### extrai texto da página
        listPages.append(extractedPageText)                                                                             ### adiciona o texto da página na lista
    print(listPages)

########## SUBSTITUIR AS SUBTRINGS '\n' DA LISTA ##########

    import re
    listPages = [re.sub("\n", '', string) for string in listPages]                                                      ### lista com as páginas do PDF
    print(listPages[:1], '\n')

    stringUnica = ' '.join(listPages)
    print('\033[1;33m - - TEXTO COMO UMA STRING SÓ: \033[m')
    print(stringUnica[:100], '\n')


#################### PRÉ-PROCESSAMENTO ####################

## LOWERCASE TEXT
    stringUnica = stringUnica.lower()
    print('\033[1;33m - - TEXTO COM MINÚSCULAS: \033[m')
    print(stringUnica[:100], '\n')

## TOKENIZATION
    from nltk.tokenize import word_tokenize, RegexpTokenizer

    space = RegexpTokenizer('\s+', gaps=True)
    tokenSpace = space.tokenize(stringUnica)
    print('\033[1;33m - - TOKENIZADO POR ESPAÇO: \033[m')
    print(tokenSpace, '\n')

## STOPWORDS
    from nltk.corpus import stopwords
    #print(stopwords.words('portuguese'))

    stopWords = stopwords.words('portuguese')
    stopLambda = lambda text: [word for word in text if word not in stopWords]                                          ### Retorna as palavras que não estão na lista de stopwords do português
    tokenSpaceSW = stopLambda(tokenSpace)                                                                               ### retira as stopwords
    print('\033[1;33m - - SEM STOPWORDS: \033[m')
    print(tokenSpaceSW, '\n')

## STEMMING
    from nltk.stem import SnowballStemmer                                                                               ### O LancasterStemmer é (mais agressivo)
    stemmer = SnowballStemmer('portuguese')                                                                             ### cria o stemmer com base na língua portuguesa

    stemLambda = lambda text: [stemmer.stem(text) for text in tokenSpaceSW]                                             ### retorna as palavras reduzidas ao seu radical
    tokenSpaceSWStem = stemLambda(tokenSpaceSW)
    print('\033[1;33m - - STEMMIZADO: \033[m')
    print(tokenSpaceSWStem, '\n')

## MOST FREQUENT WORDS
    from collections import Counter

    wordCounts = Counter(tokenSpaceSWStem)
    wordCounts = list(zip(wordCounts.values(), wordCounts.keys()))                     ### (frequência, palavra)
    wordCounts = sorted(wordCounts, reverse=True)                                      ### ordem decrescente de frequência
    print('\033[1;33m - - PALAVRAS MAIS FREQUENTES: \033[m')
    print(wordCounts[:10])

## CRIAR ARQUIVO TXT PARA COLOCAR AS PALAVRAS MAIS FREQUENTES

    textFile = open('most_frequent_words.txt', 'r')
    cont = textFile.readlines()
    cont.append(str(wordCounts))
    cont.append('\n\n')
    textFile = open('most_frequent_words.txt', 'w')
    textFile.writelines(cont)
    textFile.close()

    print('\n')

