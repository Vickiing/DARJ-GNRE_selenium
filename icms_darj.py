from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from time import sleep
import pyautogui as pg
import datetime
import pandas as pd
import datetime


"""
Data de Pagamento lojas = dia 05
Data de Pagamento MegaBox  = dia 10
"""

#Calculo da data para mes anterior
data_pagamento_lojas = datetime.date.today()
ano = data_pagamento_lojas.strftime('%Y')
mes = data_pagamento_lojas.strftime('%m')
mes_anterior = (data_pagamento_lojas.replace(day=1) - datetime.timedelta(days=1)).strftime('%m')
mes_ano_anterior = f"{mes_anterior}/{ano}"


def darj_automatico_difal(cnpj, loja, icms, fecp):

    print("Iniciando Darj DIFAL: ", cnpj, loja, icms, fecp)

    options = Options()
    preferences = {'download.default_directory' : r'C:\Users\vlsilva\Documents\PYTHON PROJETOS\python_fiscal\Darj-Gnre_selenium\download'}
    options.add_experimental_option("prefs", preferences)
    url = r'https://www1.fazenda.rj.gov.br/projetoGCTBradesco/br/gov/rj/sef/gct/web/emitirdocumentoarrecadacao/begin.do'
    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    sleep(10)

    c_tipo_pagamento = driver.find_element(By.XPATH, '//*[@id="tipoPagamentoLista"]').click()
    pg.press('down', presses=2)
    sleep(2)
    pg.press('enter')
    c_botao_alterar = driver.find_element(By.XPATH, '//*[@id="btnAlterarDataPagamento"]').click()
    sleep(5)
    c_data = driver.find_element(By.XPATH, '//*[@id="txtDataPagamento"]').click()
    pg.typewrite('05/04/2024', interval=0.2)
    c_botao_alterar = driver.find_element(By.XPATH, '//*[@id="btnAlterarDataPagamento"]').click()
    sleep(5)
    c_natureza = driver.find_element(By.XPATH, '//*[@id="slcNaturezaLista"]').click()
    pg.press('down') #presses=6)
    sleep(2)
    pg.press('enter')
    sleep(3)
    #c_qualificacao = driver.find_element(By.XPATH, '//*[@id="slcListaQualificacao"]').click()
    #pg.press('down', presses=3)
    #pg.press('enter')
    #sleep(2)

    c_cnpj = driver.find_element(By.XPATH, '//*[@id="txtCnpjCpf"]').click()
    pg.typewrite(str(cnpj), interval=0.2)
    c_botao_confirmar = driver.find_element(By.XPATH, '//*[@id="btnConfirmar"]').click()
    sleep(2)
    c_periodo_ref = driver.find_element(By.XPATH, '//*[@id="txtPeriodoReferencia"]').click()
    pg.typewrite(str(mes_ano_anterior), interval=0.2)
    pg.press('enter')
    sleep(2)
    #c_tipo_pagamento_2 = driver.find_element(By.XPATH, '//*[@id="rdgDiaVencimentoTotal"]').click()
    #sleep(2)
    c_botao_alterar_2 = driver.find_element(By.XPATH, '//*[@id="btnAlterarData"]').click()
    sleep(2)
    pg.typewrite('05/04/2024', interval=0.2)
    sleep(2)
    info_complementares = driver.find_element(By.XPATH, '//*[@id="txtJustificativa"]').click()
    pg.typewrite(f'LOJA:{loja} ATIVO', interval=0.2)
    sleep(2)

    #campo valores
    icms_informado = driver.find_element(By.XPATH, '//*[@id="txtIcmsInformado"]').click()
    pg.typewrite(str(icms), interval=0.2)
    botao_ok_1 = driver.find_element(By.XPATH, '//*[@id="okIcms"]').click()

    fecp_informado = driver.find_element(By.XPATH, '//*[@id="txtFecpInformado"]').click()
    pg.typewrite(str(fecp), interval=0.2)
    botao_ok_2 = driver.find_element(By.XPATH, '//*[@id="okFecp"]').click()
    #fim
    confirmar_item = driver.find_element(By.XPATH, '//*[@id="formulario"]/fieldset[2]/div[3]/input[1]').click()
    sleep(3)

    #****Faze experimental****
    botao_gerar_darj = driver.find_element(By.XPATH, '//*[@id="boxResumo_botoes2"]/input').click()
    sleep(6)
    #tela de download
    pg.hotkey('ctrl', 's')
    sleep(2)
    pg.typewrite(f'LOJA {loja}', interval=0.2)
    pg.press('enter')
    sleep(1.5)
    #sair = input('Pressione enter para sair')
    #if sair == None or sair == '':
    #    driver.quit()
    #    print('driver encerrado')
    #else:
    #    print('Encerrando em 5 segundos...')
    #    sleep(5)
    driver.quit()


def darj_automatico_icms(cnpj, loja, icms, fecp):

    print("Iniciando o processo de DARJ: ", cnpj, loja, icms, fecp)

    url = r'https://www1.fazenda.rj.gov.br/projetoGCTBradesco/br/gov/rj/sef/gct/web/emitirdocumentoarrecadacao/begin.do'
    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    driver.get(url)
    sleep(10)
    c_tipo_pagamento_select = Select(driver.find_element(By.XPATH, '//*[@id="tipoPagamentoLista"]'))
    c_tipo_pagamento_select.select_by_value('1')
    sleep(2)
    #pg.press('enter')
    c_botao_alterar = driver.find_element(By.XPATH, '//*[@id="btnAlterarDataPagamento"]').click()
    sleep(3)
    c_data = driver.find_element(By.XPATH, '//*[@id="txtDataPagamento"]').send_keys('06/05/2024')
    #pg.typewrite('06/05/2024', interval=0.2)
    c_botao_alterar = driver.find_element(By.XPATH, '//*[@id="btnAlterarDataPagamento"]').click()
    sleep(3)
    #c_natureza = driver.find_element(By.XPATH, '//*[@id="slcNaturezaLista"]').click()
    natureza_select = Select(driver.find_element(By.XPATH, '//*[@id="slcNaturezaLista"]'))
    natureza_select.select_by_value('1')
    sleep(2)
    c_qualificacao_select = Select(driver.find_element(By.XPATH, '//*[@id="slcListaQualificacao"]'))
    c_qualificacao_select.select_by_value('1')
    sleep(1.5)

    c_cnpj = driver.find_element(By.XPATH, '//*[@id="txtCnpjCpf"]').send_keys(cnpj)
    #pg.typewrite(str(cnpj), interval=0.2)
    c_botao_confirmar = driver.find_element(By.XPATH, '//*[@id="btnConfirmar"]').click()
    sleep(5)

    #tipo_apuracao = driver.find_element(By.XPATH, '//*[@id="rdgPorOperacao"]').click()
    #sleep(2)

    c_periodo_ref = driver.find_element(By.XPATH, '//*[@id="txtPeriodoReferencia"]').send_keys('04/2024')
    #pg.typewrite('04/2024', interval=0.2)
    pg.press('enter')
    sleep(2)
    c_tipo_pagamento_2 = driver.find_element(By.XPATH, '//*[@id="rdgDiaVencimentoTotal"]').click()
    sleep(2)
    c_botao_alterar_2 = driver.find_element(By.XPATH, '//*[@id="btnAlterarData"]').click()
    sleep(2)
    pg.typewrite('06/05/2024', interval=0.2)
    sleep(2)
    info_complementares = driver.find_element(By.XPATH, '//*[@id="txtJustificativa"]').click()
    pg.typewrite(f'LOJA:{loja}', interval=0.1)
    sleep(2)

    #campo valores
    icms_informado = driver.find_element(By.XPATH, '//*[@id="txtIcmsInformado"]').click()
    pg.typewrite(str(icms), interval=0.2)
    botao_ok_1 = driver.find_element(By.XPATH, '//*[@id="okIcms"]').click()

    fecp_informado = driver.find_element(By.XPATH, '//*[@id="txtFecpInformado"]').click()
    pg.typewrite(str(fecp), interval=0.2)
    botao_ok_2 = driver.find_element(By.XPATH, '//*[@id="okFecp"]').click()
    #fim
    confirmar_item = driver.find_element(By.XPATH, '//*[@id="formulario"]/fieldset[2]/div[3]/input[1]').click()
    sleep(5)

    #****Faze experimental****
    botao_gerar_darj = driver.find_element(By.XPATH, '//*[@id="boxResumo_botoes2"]/input').click()
    sleep(15)
    #tela de download
    pg.hotkey('ctrl', 's')
    sleep(2)
    pg.typewrite(f'LOJA {loja}', interval=0.2)
    pg.press('enter')
    sleep(1.5)
    #sair = input('Pressione enter para sair')
    #if sair == None or sair == '':
    #    driver.quit()
    #    print('driver encerrado')
    #else:
    #    print('Encerrando em 5 segundos...')
    #    sleep(5)
    driver.quit()


def darj_automatico_diario():
    data_atual = datetime.date.today()
    data_formatada = data_atual.strftime('%d/%m/%Y')
    

    arquivo = r'C:\Users\vlsilva\Documents\PYTHON PROJETOS\python_fiscal\Darj-Gnre_selenium\RelatorioPgtoSubsTrib.xls'
    df = pd.read_excel(arquivo)

    for index, row in df.iterrows():
        tipo = row['Tipo']
        nota_fiscal = row['Nota Fiscal']
        serie = row['Série']
        serie_formatada = '{:.0f}'.format(serie)
        cnpj_fornecedor = str(int(row['CNPJ Fornecedor'])).zfill(14)
        cnpj_destino = row['CNPJ Destino']
        loja = row['Cod. Destino']
        icms = row['Valor Principal']
        fecp = row['Valor Fecp']
        icms_format = '{:.2f}'.format(icms)
        fecp_format = '{:.2f}'.format(fecp)
        Classe = row['Classe']

        if tipo == 'D':

            print("Iniciando o processo de DARJ: ",nota_fiscal, cnpj_destino, str(cnpj_fornecedor), loja, icms_format, fecp_format, data_formatada)
            
            options = Options()
            preferences = {'download.default_directory' : r'C:\Users\vlsilva\Documents\PYTHON PROJETOS\python_fiscal\Darj-Gnre_selenium\download'}
            options.add_experimental_option("prefs", preferences)
            options.add_argument('--headless')
            url = r'https://www1.fazenda.rj.gov.br/projetoGCTBradesco/'
            service = Service(executable_path="chromedriver.exe")
            driver = webdriver.Chrome(service=service, options=options)
            print('Acessando: ', url)
            driver.get(url)
            sleep(5)

            c_tipo_pagamento = Select(driver.find_element(By.XPATH, '//*[@id="tipoPagamentoLista"]'))
            c_tipo_pagamento.select_by_value('1')
            sleep(2)
            c_botao_alterar = driver.find_element(By.XPATH, '//*[@id="btnAlterarDataPagamento"]').click()
            sleep(2)
            c_data = driver.find_element(By.XPATH, '//*[@id="txtDataPagamento"]').send_keys(data_formatada)
            c_botao_alterar = driver.find_element(By.XPATH, '//*[@id="btnAlterarDataPagamento"]').click()
            sleep(2)
            c_natureza = Select(driver.find_element(By.XPATH, '//*[@id="slcNaturezaLista"]'))
            c_natureza.select_by_value('4')
            sleep(3)

            select_produto = Select(driver.find_element(By.XPATH, '//*[@id="slcListaProduto"]'))
            if Classe == 'PRODUTOS ALIMENTICIOS':
                classe_selecionada =select_produto.select_by_value('469')#alimenticio
            else:
                classe_selecionada = select_produto.select_by_value('698')#outros

            print('Classe selecionada: ', Classe)

            c_cnpj = driver.find_element(By.XPATH, '//*[@id="txtCnpjCpf"]').send_keys(str(cnpj_destino))
            sleep(2)
            c_botao_confirmar = driver.find_element(By.XPATH, '//*[@id="btnConfirmar"]').click()
            sleep(2)
            tipo_apuracao = driver.find_element(By.XPATH, '//*[@id="rdgPorOperacao"]').click()
            sleep(2)
            numero_nota = driver.find_element(By.XPATH, '//*[@id="txtNotaFiscal"]')
            sleep(2)
            numero_nota.send_keys(nota_fiscal)
            serie_nf = driver.find_element(By.XPATH, '//*[@id="txtSerieNf"]').send_keys(serie_formatada)
            c_tipo = Select(driver.find_element(By.XPATH, '//*[@id="slcTipoNf"]'))
            c_tipo.select_by_value("NF-e")
            sleep(2)
            data_emissao = driver.find_element(By.XPATH, '//*[@id="txtDataNf"]').send_keys(data_formatada)
            sleep(1)
            cnpj_emitente = driver.find_element(By.XPATH, '//*[@id="txtCnpjCpfNf"]').send_keys(str(cnpj_fornecedor))

            botao_data = driver.find_element(By.XPATH, '//*[@id="btnAlterarData"]').click()
            sleep(2)
            driver.find_element(By.XPATH,'//*[@id="txtDataVencimento"]').send_keys(data_formatada)

            sleep(2)
            info_complementares = driver.find_element(By.XPATH, '//*[@id="txtJustificativa"]').send_keys(f'LOJA:{loja}')
            
            sleep(3)

            print('Iniciando o preenchimento dos campos valores...')
            #campo valores
            icms_informado = driver.find_element(By.XPATH, '//*[@id="txtIcmsInformado"]').send_keys(icms_format)
            botao_ok_1 = driver.find_element(By.XPATH, '//*[@id="okIcms"]').click()
            fecp_informado = driver.find_element(By.XPATH, '//*[@id="txtFecpInformado"]').send_keys(fecp_format)            
            botao_ok_2 = driver.find_element(By.XPATH, '//*[@id="okFecp"]').click()
            confirmar_item = driver.find_element(By.XPATH, '//*[@id="formulario"]/fieldset[2]/div[3]/input[1]').click()
            sleep(5)

            botao_gerar_darj = driver.find_element(By.XPATH, '//*[@id="boxResumo_botoes2"]/input').click()
            sleep(10)
            print('iniciando o download')
            driver.execute_script("""
                    var downloadLink = document.createElement('a');
                    downloadLink.setAttribute('id', 'downloadLink');
                    downloadLink.setAttribute('href', 'https://www1.fazenda.rj.gov.br/projetoGCTBradesco/br/gov/rj/sef/gct/web/emitirdocumentoarrecadacao/transfereDadosDebitos.do');
                    downloadLink.setAttribute('download', 'documento.pdf');
                    downloadLink.innerHTML = 'Download PDF';

                    // Adiciona o link à página
                    document.body.appendChild(downloadLink);

                    // Simula um clique no link de download
                    //Se o driver estiver no modo headless, precisa desativar o click no botao
                    //downloadLink.click();
                    """)
            print('Download concluído')
            sleep(2)
            driver.quit()