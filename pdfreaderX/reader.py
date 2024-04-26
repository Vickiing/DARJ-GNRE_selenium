from PyPDF2 import PdfReader
import os


def pdf_leitor_gnre():
    caminho = r'C:\Users\vlsilva\Documents\PYTHON PROJETOS\python_fiscal\Darj-Gnre_selenium\download'

    for file in os.listdir(caminho):
        
        arquivo = os.path.join(caminho, file)
        
        reader = PdfReader(arquivo)
        page = reader.pages[0]
        page_text = page.extract_text()

        for linha in page_text.split('\n'):

            if linha.__contains__('Chave DF-e:'):
                valores = linha.split(' ')
                chave = valores[2]
                numero = int(chave[25:34])
                print(numero)
                #RENOMEAR ARQUIVO PARA GNRE_ OU DARJ_
                os.rename(arquivo, f'C:\\Users\\vlsilva\\Documents\\PYTHON PROJETOS\\python_fiscal\\Darj-Gnre_selenium\\download\\GNRE_{numero}.pdf')
                break
pdf_leitor_gnre()

def pdf_leitor_darj():
    

    #for file in os.listdir(caminho):
        
        #arquivo = os.path.join(caminho, file)
        caminho = r'C:\Users\vlsilva\Downloads\itenspagamento_1714049660465.pdf'
        reader = PdfReader(caminho)
        page = reader.pages[0]
        page_text = page.extract_text()
        for linha in page_text.split('\n'):

            #if linha.__contains__('Chave DF-e:'):
                valores = linha.split(' ')
                print(valores[0])
                #os.rename(caminho, f'C:\\Users\\vlsilva\\Documents\\PYTHON PROJETOS\\python_fiscal\\Darj-Gnre_selenium\\download\\DARJ_{valores[0]}.pdf')

#pdf_leitor_darj()