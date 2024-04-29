from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from time import sleep
from selenium.webdriver.common.keys import Keys
import pandas as pd



def baixar_xml():

    relatorio_excel = r'C:\Users\vlsilva\Documents\PYTHON PROJETOS\python_fiscal\Darj-Gnre_selenium\RelatorioPgtoSubsTrib.xls'
    df_excel = pd.read_excel(relatorio_excel)

    url = r'https://app.auditto.com.br/contas/login'
    url_monitor = r'https://app.auditto.com.br/fiscal/recebidas/monitor'

    options = Options()
    preferences = {'download.default_directory' : r'C:\Users\vlsilva\Documents\PYTHON PROJETOS\python_fiscal\Darj-Gnre_selenium\arquivo_xml'}
    options.add_experimental_option("prefs", preferences)
    options.add_argument("--headless")
    options.add_argument('--disable-notifications')
    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)
    print(f'Acessando: {url}')
    driver.get(url)
    sleep(5)
    login = '14186123756'
    senha = str('Zs2023!!!!')

    chaves = []
    for index, linha in df_excel.iterrows():
        if linha[0] == "G":
            chaves.append(linha['Chave'])
    print(f'Chaves lidas:{chaves}')


    try:
        print('Logando no sistema...')
        driver.find_element(By.NAME, 'login').send_keys(login)
        driver.find_element(By.NAME, 'senha').send_keys(senha)
        driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/div/div[2]/div[2]/form/fieldset/input').click()
        print('Logado com sucesso')
        sleep(2)
        print('Acessando:', format(url_monitor))
        for chave in chaves:
            driver.get(url_monitor)
            sleep(5)
            print('Acessando elementos...')
            sleep(2)

            driver.find_element(By.CSS_SELECTOR, "button[data-toggle='offcanvas']").click()
            print('Elemento acessado com sucesso!')
            sleep(2)
            print('Acessando Empresa Zona Sul S.A. (33.381.286/0001-51)')
            elemento_a = driver.find_element(By.XPATH,"//a[@class='btnConta' and @conta='33381286000151' and @url='https://app.auditto.com.br/fiscal/recebidas/monitor']")

            print('\nExecutando o javascript...\n')

            driver.execute_script("""
            var terceiroElemento = document.querySelectorAll('.menu li')[2];
            var link = terceiroElemento.querySelector('a.btnConta');
            link.click();
            """)
            print('Empresa Zona Sul acessada com sucesso!')
            #driver.get(url_monitor)

            sleep(15)
            driver.find_element(By.NAME, 'empresa-nome').click()
            sleep(5)
            driver.execute_script("""var elemento = document.querySelector('li[data-nodeid="0"][type="organizacao"]');
            elemento.click();""")
            
            print('Selecionando Todas as lojas...')
            sleep(2)
            driver.execute_script("""
    var botao = document.querySelector('button.btn.btn-primary.bt-selecionar');
    botao.click();

    """)
            
            seletor_chave = Select(driver.find_element(By.XPATH, '//*[@id="referente"]'))
            seletor_chave.select_by_value('chave')
            
            print('Inserindo Chave de Acesso...', chave)
            driver.find_element(By.XPATH, '//*[@id="busca"]').send_keys(chave)
            sleep(2)
            driver.find_element(By.XPATH, '//*[@id="busca"]').send_keys(Keys.ENTER)
            sleep(10)
            
            driver.find_element(By.CLASS_NAME, 'xml-detalhe').click()
            sleep(2)

            print('Acessando XML da chave para download...')

            sleep(5)
            
            driver.execute_script("""// Seletor CSS para encontrar todos os elementos <a> com href contendo "/fiscal/recebidas/xml?id="
        var links = document.querySelectorAll('a[href*="/fiscal/recebidas/xml?id="]');

        // Iterar sobre cada link encontrado
        links.forEach(function(link) {
            // Obter o valor do atributo href
            var href = link.getAttribute('href');
            console.log(href);
            link.click();
            
            // Abrir em uma nova aba
            // window.open(href, '_blank');
            // ou
            // Simular um clique no link
            
            });
            """)

            sleep(2)
            #driver.download_file(url_xml_download, 'XML')
            sleep(10)
            print('XML baixado com sucesso!')

    except Exception as e:
        print('Erro:', e)







