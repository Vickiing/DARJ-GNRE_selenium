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


arquivo = r'C:\Users\vlsilva\Documents\PYTHON PROJETOS\python_fiscal\Darj_selenium\RelatorioPgtoSubsTrib.xls'
df = pd.read_excel(arquivo)


def xml_leitor():
    xml_arquivo = r'C:\Users\vlsilva\Documents\PYTHON PROJETOS\python_fiscal\Darj_selenium\arquivo_xml\33230629020880000140550220003228301074967910-procNFe.xml'
    dom = xml.dom.minidom.parse(xml_arquivo)
    try:
        cnpj_destinatario = dom.getElementsByTagName('CNPJ')[0].firstChild.data
        uf_destinatario = dom.getElementsByTagName('UF')[0].firstChild.data
        mun = dom.getElementsByTagName('xMun')[0].firstChild.data
        razao_social = dom.getElementsByTagName('xNome')[0].firstChild.data
        endereco = dom.getElementsByTagName('xLgr')[0].firstChild.data
        chave = dom.getElementsByTagName('chNFe')[0].firstChild.data
        cep = dom.getElementsByTagName('CEP')[0].firstChild.data
        return chave, cnpj_destinatario, uf_destinatario, mun, razao_social, endereco, cep

    except Exception as e:
        print(e)



def gnre_automatico():
    xml_data = xml_leitor()
    url = r'https://www.gnre.pe.gov.br:444/gnre/v/guia/index'
    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    driver.get(url)
    sleep(5)
    for indice, linha in df.iterrows():
        uf_favorecida = driver.find_element(By.XPATH, '//*[@id="ufFavorecida"]/option[19]').click()
        tipo_gnre = driver.find_element(By.XPATH, '//*[@id="optGnreSimples"]').click()
        incr_uf = driver.find_element(By.XPATH, '//*[@id="optNaoInscrito"]').click()
        doc_identificacao = driver.find_element(By.XPATH, '//*[@id="tipoCNPJ"]').click()
        #campo_cnpj = driver.find_element(By.XPATH, '//*[@id="documentoEmitente"]').click()

        pg.typewrite(str(xml_data.cnpj_destinatario), interval=0.1)
        razao_social = driver.find_element(By.XPATH, '//*[@id="razaoSocialEmitente"]').click()
        pg.typewrite(str(xml_data.razao_social), interval=0.1)
        endereco = driver.find_element(By.XPATH, '//*[@id="enderecoEmitente"]').click()
        print(f'endereco {endereco}')
        pg.typewrite(endereco, interval=0.1)
        select_uf = driver.find_element(By.ID, 'ufEmitente')
        select = Select(select_uf)
        uf_element = select.select_by_value(xml_data.uf_destinatario)
        municipio_element = driver.find_element(By.ID, 'municipioEmitente').click()
        select = Select(municipio_element)
        select.select_by_value(xml_data.mun)
        cep_element = driver.find_element(By.XPATH, '//*[@id="cepEmitente"]').click()
        pg.typewrite(xml_data.cep, interval=0.1)
        receita_tipo = driver.find_element(By.XPATH, '//*[@id="receita"]').click()
        select = Select(receita_tipo)
        select.select_by_value('100099')

        sleep(3)
gnre_automatico()



