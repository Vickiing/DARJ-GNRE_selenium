import pandas as pd
from icms_darj import darj_automatico, darj_automatico_difal, darj_automatico_diario
from Xml_Gnre import gnre_automatico

def executar_programa():
    print('Escolha a opção desejada: \n1 - DARJ\n2 - DARJ DIFAL\n3 - GNRE\n4 - DARJ DIARIO')
    opcao = int(input('Opção: '))

    match opcao:
        case 1:
            darj()
        case 2:
            darj_difal()
        case 3:
            gnre_automatico()
        case 4:
            darj_diario()



def darj():
    excel = r'C:\Users\vlsilva\Documents\PYTHON PROJETOS\python_fiscal\Darj-Gnre_selenium\icms.xlsx'
    df = pd.read_excel(excel)
    df['INSCRICAO'] = df['INSCRICAO'].astype(str).str.replace('\.0', '', regex=True)
    #df = df.round(2)
    #df = '{:.2f}'.format(df)

    for loja in df['LOJAS'].values:
        filtro = df[df['LOJAS'] == loja]
        if not filtro.empty:  # Verifica se o filtro retornou algum resultado
            cnpj = filtro['INSCRICAO'].iloc[0]  # Assume que o CNPJ é único para cada loja
            loja = filtro['LOJAS'].iloc[0]  # Assume que o nome da loja é único
            icms = filtro['ICMS'].iloc[0]
            icms_formatado = '{:.2f}'.format(icms)
            fecp = filtro['FECP'].iloc[0]
            fecp_formatado = '{:.2f}'.format(fecp)
            total = icms + fecp
            print(f'Loja: {loja} - Total: {total}')
            #função pra darj
            darj_automatico(cnpj, loja, icms_formatado, fecp_formatado)
        else:
            print(f"Loja: {loja}  não encontrada.")


def darj_difal():
    excel = r'C:\Users\vlsilva\Documents\PYTHON PROJETOS\python_fiscal\Darj-Gnre_selenium\icms.xlsx'
    df = pd.read_excel(excel)
    df['INSCRICAO'] = df['INSCRICAO'].astype(str).str.replace('\.0', '', regex=True)
    #df = df.round(2)
    #df = '{:.2f}'.format(df)

    for loja in df['LOJAS'].values:
        filtro = df[df['LOJAS'] == loja]
        if not filtro.empty:  # Verifica se o filtro retornou algum resultado
            cnpj = filtro['INSCRICAO'].iloc[0]  # Assume que o CNPJ é único para cada loja
            loja = filtro['LOJAS'].iloc[0]  # Assume que o nome da loja é único
            icms = filtro['ICMS'].iloc[0]
            icms_formatado = '{:.2f}'.format(icms)
            fecp = filtro['FECP'].iloc[0]
            fecp_formatado = '{:.2f}'.format(fecp)
            total = icms + fecp
            print(f'Loja: {loja} - Total: {total}')
            #função pra darj
            darj_automatico_difal(cnpj, loja, icms_formatado, fecp_formatado)
        else:
            print(f"Loja: {loja}  não encontrada.")


def darj_diario():
    #data = input('Infome a data de emissaão do DARJ (formato dd/mm/aaaa): ')
    darj_automatico_diario()

executar_programa()