import xml.dom.minidom
from selenium import webdriver
import selenium.common.exceptions as se
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import xml.dom.minidom
from time import sleep
from datetime import date
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


def gnre_automatico():
    
    #Calculo da data de emissaão
    data_pagamento_lojas = date.today()
    day = data_pagamento_lojas.strftime('%d/%m/%Y')
    #data = input("Data de Pagamento: ")
    
    arquivo = r'C:\Users\vlsilva\Documents\PYTHON PROJETOS\python_fiscal\Darj-Gnre_selenium\RelatorioPgtoSubsTrib.xls'
    df = pd.read_excel(arquivo)
    print('\nArquivo Excel lido...\n')
    
    for index, row in df.iterrows():
        tipo = row['Tipo']
        nota_fiscal = row['Nota Fiscal']
        serie = row['Série']
        serie_formatada = '{:.0f}'.format(serie)
        cnpj_fornecedor = str(row['CNPJ Fornecedor']).zfill(14)
        cnpj_destino = row['CNPJ Destino']
        chave_de_acesso = row['Chave']
        loja = row['Cod. Destino']
        icms = row['Valor Principal']
        fecp = row['Valor Fecp']
        icms_format = '{:.2f}'.format(icms)
        fecp_format = '{:.2f}'.format(fecp)

        if tipo == 'G':
            elemento = False
            while elemento is False:
                try:
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
                    xml_arquivo = f'{pasta_caminho}\{chave_de_acesso}-procNFe.xml'
                    print(xml_arquivo)
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
                    campo_cnpj = driver.find_element(By.XPATH, '//*[@id="documentoEmitente"]').send_keys(str(xml_data.cnpj_destinatario))
                    razao_social = driver.find_element(By.XPATH, '//*[@id="razaoSocialEmitente"]').send_keys(str(xml_data.razao_social))

                    endereco = driver.find_element(By.XPATH, '//*[@id="enderecoEmitente"]').send_keys(str(xml_data.endereco))

                    select_uf = driver.find_element(By.ID, 'ufEmitente')
                    select = Select(select_uf)
                    uf_element = select.select_by_value(xml_data.uf_destinatario)

                    sleep(3)

                    municipio_element = driver.find_element(By.ID, 'municipioEmitente')
                    select = Select(municipio_element)
                    select.select_by_visible_text(xml_data.mun.upper())
                    cep_element = driver.find_element(By.XPATH, '//*[@id="cepEmitente"]').click()
                    pg.press('backspace', presses=8)
                    #cep_element = driver.find_element(By.XPATH, '//*[@id="cepEmitente"]').clear()
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
                    data_vencimento = driver.find_element(By.XPATH, '//*[@id="dataVencimento"]').send_keys(str(day))

                    valor_principal = driver.find_element(By.XPATH, '//*[@id="valor"]').click()
                    valor_principal_digitado = df[df['Chave'] == xml_data.chave]['Valor Principal'].iloc[0]
                    pg.typewrite(str('{:.2f}'.format(valor_principal_digitado)), interval=0.1)

                    valor_fecp = driver.find_element(By.XPATH, '//*[@id="valorFecp"]').click()
                    valor_fecp_digitado = df[df['Chave'] == xml_data.chave]['Valor Fecp'].iloc[0]
                    pg.typewrite(str('{:.2f}'.format(valor_fecp_digitado)), interval=0.1)

                    insc_uf_favorecida = driver.find_element(By.XPATH, '//*[@id="optInscritoDest"]').click()
                    inscricao_estadual = driver.find_element(By.XPATH, '//*[@id="inscricaoEstadualDestinatario"]').click()
                    ins_estadual = df[df['Chave'] == xml_data.chave]['Insc. Estadual Dest.'].iloc[0]
                    ins_estadual_formatada = '{:.0f}'.format(ins_estadual)
                    pg.typewrite(str(ins_estadual_formatada), interval=0.1)

                    data_emissao = driver.find_element(By.XPATH, '//*[@id="campoAdicional00"]').click()
                    pg.press('backspace', presses=8)
                    data_emissao = driver.find_element(By.XPATH, '//*[@id="campoAdicional00"]').send_keys(str(day))

                    loja = df[df['Chave'] == xml_data.chave]['Cod. Destino'].iloc[0]
                    info_complementares = driver.find_element(By.XPATH, '//*[@id="campoAdicional01"]').click()
                    pg.typewrite(f'Loja: {str(loja)}', interval=0.1)

                    elemento = True

                except se.NoSuchElementException as e:
                    print("Elemento não encontrado:", e)
                    continue
                    
            botao_validar = driver.find_element(By.XPATH, '//*[@id="validar"]').click()
            sleep(15)

            print('\nBaixando documento...\n')
            baixar = driver.find_element(By.XPATH, '//*[@id="baixar"]').click()
            sleep(10)
            print('Docmento GNRE baixado com sucesso!')
            driver.quit()
