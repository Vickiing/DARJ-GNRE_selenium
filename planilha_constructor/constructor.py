import pandas as pd


arquivo = r'planilha_constructor\Requisições DARJ e GNRE - 2024.xlsx'

def ler_tab_ZONA_SUL_DARJ():
    # TAB ZONA SUL DARJ
    tab_ZONA_SUL_DARJ = pd.read_excel(arquivo, sheet_name='ZONA_SUL_DARJ',)
    inicio_coluna_favorecido_zsdarj = tab_ZONA_SUL_DARJ.apply(lambda col: col.str.contains('FAVORECIDO', na=False)).idxmax()
    indice_inicio_coluna_zsdarj = inicio_coluna_favorecido_zsdarj.max()
    tab_ZONA_SUL_DARJ = pd.read_excel(arquivo, sheet_name='ZONA_SUL_DARJ', skiprows= indice_inicio_coluna_zsdarj)
    print(tab_ZONA_SUL_DARJ)


def ler_tab_ZONA_SUL_GNRE():
    #TAB ZONA SUL GNRE
    tab_ZONA_SUL_GNRE = pd.read_excel(arquivo,sheet_name='ZONA_SUL_GNRE')
    inicio_coluna_favorecido_zsgnre = tab_ZONA_SUL_GNRE.apply(lambda col: col.str.contains('FAVORECIDO', na=False)).idxmax()
    indice_inicio_coluna_zsgnre = inicio_coluna_favorecido_zsgnre.max()
    tab_ZONA_SUL_GNRE = pd.read_excel(arquivo,sheet_name='ZONA_SUL_GNRE', skiprows=indice_inicio_coluna_zsgnre)
    print(tab_ZONA_SUL_GNRE)

