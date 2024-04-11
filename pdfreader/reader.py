from PyPDF2 import PdfReader
import os


def pdf_leitor():
    caminho = r'C:\Users\vlsilva\Documents\PYTHON PROJETOS\python_fiscal\Darj_selenium\download'

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
                os.rename(arquivo, f'C:\\Users\\vlsilva\\Documents\\PYTHON PROJETOS\\python_fiscal\\Darj_selenium\\download\\GNRE_{numero}.pdf')
                break
pdf_leitor()