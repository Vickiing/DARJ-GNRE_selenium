import xml.dom.minidom
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import xml.dom.minidom
from time import sleep
import pyautogui as pg
import pandas as pd
import os
from fake_useragent import UserAgent

class XML:
    def __init__(self):
        self.chave = None
        self.cnpj_destinatario = None
        self.uf_destinatario = None
        self.mun = None
        self.razao_social = None
        self.endereco = None
        self.cep = None

def xml_leitor(xml_arquivo):
    
    dom = xml.dom.minidom.parse(xml_arquivo)
    
    xml_obj = XML()  
    
    try:
        xml_obj.cnpj_destinatario = dom.getElementsByTagName('CNPJ')[0].firstChild.data
        xml_obj.uf_destinatario = dom.getElementsByTagName('UF')[0].firstChild.data
        xml_obj.mun = dom.getElementsByTagName('xMun')[0].firstChild.data
        xml_obj.razao_social = dom.getElementsByTagName('xNome')[0].firstChild.data
        xml_obj.endereco = dom.getElementsByTagName('xLgr')[0].firstChild.data
        xml_obj.chave = dom.getElementsByTagName('chNFe')[0].firstChild.data
        xml_obj.cep = dom.getElementsByTagName('CEP')[0].firstChild.data
        
        return xml_obj
    
    except Exception as e:
        print("Erro ao processar XML:", e)
        return None  # Retorna None em caso de erro

# Exemplo de utilização da função e da classe:
def gnre_automatico():

    data = input("Data de Pagamento: ")
    
    arquivo = r'C:\Users\vlsilva\Documents\PYTHON PROJETOS\python_fiscal\Darj-Gnre_selenium\RelatorioPgtoSubsTrib.xls'
    df = pd.read_excel(arquivo)
    print('\nArquivo Excel lido...\n')
    
    for i in os.listdir('arquivo_xml'):
        ua = UserAgent()
        user_agent = ua.random
        print(user_agent)

        options = Options()
        preferences = {'download.default_directory' : r'C:\Users\vlsilva\Documents\PYTHON PROJETOS\python_fiscal\Darj-Gnre_selenium\download'}
        options.add_experimental_option("prefs", preferences)
        options.add_argument(f'--user-agent={user_agent}')
        #options.add_argument("--headless")

        url = r'https://www.gnre.pe.gov.br:444/gnre/v/guia/index'
        service = Service(executable_path="chromedriver.exe")
        driver = webdriver.Chrome(service=service, 
        options=options)

        driver.get(url)
        sleep(5)

        pasta_caminho = 'arquivo_xml'
        xml_arquivo = f'{pasta_caminho}\{i}'
        xml_data = xml_leitor(xml_arquivo)

        loja = df[df['Chave'] == xml_data.chave]['Cod. Destino'].iloc[0]
        chave = df[df['Chave'] == xml_data.chave]['Chave'].iloc[0]
        fornecedor = df[df['Chave'] == xml_data.chave]['Fornecedor'].iloc[0]
        valor_fecp = df[df['Chave'] == xml_data.chave]['Valor Fecp'].iloc[0]
        valor_principal = df[df['Chave'] == xml_data.chave]['Valor Principal'].iloc[0]
       
        print(f'Emitindo GNRE para: \nLoja: {loja}\nChave: {chave}\nFornecedor: {fornecedor}\nValor Principal: {valor_principal}\nValor Fecp: {valor_fecp}')


        uf_favorecida = driver.find_element(By.XPATH, '//*[@id="ufFavorecida"]/option[19]').click()
        tipo_gnre = driver.find_element(By.XPATH, '//*[@id="optGnreSimples"]').click()
        incr_uf = driver.find_element(By.XPATH, '//*[@id="optNaoInscrito"]').click()
        doc_identificacao = driver.find_element(By.XPATH, '//*[@id="tipoCNPJ"]').click()
        pg.typewrite(str(xml_data.cnpj_destinatario), interval=0.1)

        razao_social = driver.find_element(By.XPATH, '//*[@id="razaoSocialEmitente"]').click()
        pg.typewrite(str(xml_data.razao_social), interval=0.1)

        endereco = driver.find_element(By.XPATH, '//*[@id="enderecoEmitente"]').click()
        pg.typewrite(str(xml_data.endereco), interval=0.1)

        select_uf = driver.find_element(By.ID, 'ufEmitente')
        select = Select(select_uf)
        uf_element = select.select_by_value(xml_data.uf_destinatario)

        sleep(3)

        municipio_element = driver.find_element(By.ID, 'municipioEmitente')
        select = Select(municipio_element)
        select.select_by_visible_text(xml_data.mun.upper())
        cep_element = driver.find_element(By.XPATH, '//*[@id="cepEmitente"]').click()
        pg.press('backspace', presses=8)
        sleep(3)
        cep_element = driver.find_element(By.XPATH, '//*[@id="cepEmitente"]').send_keys(str(xml_data.cep))
        receita_tipo = driver.find_element(By.XPATH, '//*[@id="receita"]')
        select = Select(receita_tipo)
        select.select_by_value('100099')

        documento_origem = driver.find_element(By.XPATH, '//*[@id="tipoDocOrigem"]')
        select = Select(documento_origem)
        select.select_by_value('24')
        
        numero_doc_origem = driver.find_element(By.XPATH, '//*[@id="numeroDocumentoOrigem"]').send_keys(str(xml_data.chave))
        data_vencimento = driver.find_element(By.XPATH, '//*[@id="dataVencimento"]').click()
        pg.press('backspace', presses=8)
        #pg.typewrite(data, interval=0.2)
        data_vencimento = driver.find_element(By.XPATH, '//*[@id="dataVencimento"]').send_keys(str(data))

        valor_principal = driver.find_element(By.XPATH, '//*[@id="valor"]').click()
        valor_principal_digitado = df[df['Chave'] == xml_data.chave]['Valor Principal'].iloc[0]
        pg.typewrite(str(valor_principal_digitado), interval=0.1)

        #print(f'Valor Principal: {valor_principal_digitado} - xml_data.chave: {xml_data.chave}')

        valor_fecp = driver.find_element(By.XPATH, '//*[@id="valorFecp"]').click()
        valor_fecp_digitado = df[df['Chave'] == xml_data.chave]['Valor Fecp'].iloc[0]
        pg.typewrite(str(valor_fecp_digitado), interval=0.1)

        insc_uf_favorecida = driver.find_element(By.XPATH, '//*[@id="optInscritoDest"]').click()
        inscricao_estadual = driver.find_element(By.XPATH, '//*[@id="inscricaoEstadualDestinatario"]').click()
        ins_estadual = df[df['Chave'] == xml_data.chave]['Insc. Estadual Dest.'].iloc[0]
        ins_estadual_formatada = '{:.0f}'.format(ins_estadual)
        pg.typewrite(str(ins_estadual_formatada), interval=0.1)

        data_emissao = driver.find_element(By.XPATH, '//*[@id="campoAdicional00"]').click()
        pg.press('backspace', presses=8)
        #pg.typewrite(data, interval=0.2)
        data_emissao = driver.find_element(By.XPATH, '//*[@id="campoAdicional00"]').send_keys(str(data))

        loja = df[df['Chave'] == xml_data.chave]['Cod. Destino'].iloc[0]
        info_complementares = driver.find_element(By.XPATH, '//*[@id="campoAdicional01"]').click()
        pg.typewrite(f'Loja: {str(loja)}', interval=0.1)
        
        botao_validar = driver.find_element(By.XPATH, '//*[@id="validar"]').click()
        sleep(15)
        print('\nBaixando documento...\n')
        baixar = driver.find_element(By.XPATH, '//*[@id="baixar"]').click()
        sleep(10)
        print('Docmento GNRE baixado com sucesso!')
        driver.quit()


#gnre_automatico()
# xml_ob = xml_leitor()
# arquivo = r'C:\Users\vlsilva\Documents\PYTHON PROJETOS\python_fiscal\Darj_selenium\RelatorioPgtoSubsTrib.xls'
# df = pd.read_excel(arquivo)
# print(df)
# valor_digitado = df[df['Chave'] == xml_ob.chave]['Valor Principal'].iloc[0]
# valor_fecp = df[df['Chave'] == xml_ob.chave]['Valor Fecp']
# print(f'Valor Principal: {valor_digitado}\nValor Fecp: {valor_fecp}')