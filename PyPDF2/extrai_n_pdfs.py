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
    print(f'\033[1;30;43m Este PDF possui {pages} páginas.\033[m \n ')

    listPages = []
    for page in range(1, pages):                                                    ### itera entre as páginas do PDF
        pageText = pdfReader.getPage(page)
        extractedPageText = pageText.extractText()                                  ### extrai texto da página
        listPages.append(extractedPageText)                                        ### adiciona o texto da página na lista
    print(listPages)

########## SUBSTITUIR AS SUBTRINGS '\n' DA LISTA ##########

    import re
    listPages = [re.sub("\n", '', string) for string in listPages]                  ### lista com as páginas do PDF
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

