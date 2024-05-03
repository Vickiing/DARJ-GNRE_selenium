import sys
import os

# Adiciona o diretório raiz do projeto ao Python PATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import xml.etree.ElementTree as ET
import pandas as pd
from Xml_Gnre import xml_leitor, XML



# Modulo para gerar GNRE de um unico arquivo xml com uma ou mais guias.
# Usando o arquivo 'RelatorioPgtoSubsTrib.xls'
# Usando os padrões estipulados pela própria Sefaz.


def Gnre_Xml_Generator_Lote():
    
    arquivo = r'C:\Users\vlsilva\Documents\PYTHON PROJETOS\python_fiscal\Darj-Gnre_selenium\RelatorioPgtoSubsTrib.xls'
    df = pd.read_excel(arquivo)
    print('\nArquivo Excel lido...\n')
    
    # Criando o elemento raiz do XML
    # Padrão de cabeçalho
    root = ET.Element("TLote_GNRE")
    root.set("xmlns", "http://www.gnre.pe.gov.br")
    root.set("versao", "2.00")

    # Adicionando o elemento 'guias' como filho do elemento raiz
    guias = ET.SubElement(root, "guias")


    for index, row in df.iterrows():

        if row['Tipo'] == 'G':
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
            valor_total = row['ICMS R.F.']
            print('Montando Xml GNRE com as seguintes informações: \n')
            print('\nTipo: {}\nNota Fiscal: {}\nSerie: {}\nCNPJ Fornecedor: {}\nCNPJ Destino: {}\nChave: {}\nCod. Destino: {}\nValor Principal: {}\nValor Fecp: {}\n'.format(tipo, nota_fiscal, serie_formatada, cnpj_fornecedor, cnpj_destino, chave_de_acesso, loja, icms_format, fecp_format))
    
            validar_local = False
            while validar_local is False:

                try:
                    pasta_caminho = 'arquivo_xml'
                    xml_arquivo = f'{pasta_caminho}\{chave_de_acesso}-procNFe.xml'
                    if os.path.exists(xml_arquivo):
                        print(xml_arquivo)
                        xml_data = xml_leitor(xml_arquivo)
                        validar_local = True
                    else:
                        print(f'{xml_arquivo} NÃO ENCONTRADO!')
                        print(f'Por favor, verifique o caminho do arquivo e tente novamente.')
                        input('Pressione ENTER para continuar...')

                except Exception as e:
                    print(f'Erro:{e}')
                

            

            # Adicionando o elemento 'TDadosGNRE' como filho do elemento 'guias'
            t_dados_gnre = ET.SubElement(guias, "TDadosGNRE")
            t_dados_gnre.set("versao", "2.00")

            # Adicionando os elementos dentro de 'TDadosGNRE'
            uf_favorecida = ET.SubElement(t_dados_gnre, "ufFavorecida")
            uf_favorecida.text = "RJ" #Cidade Onde o CNPJ do Zona Sul está localizado
            tipoGnre = ET.SubElement(t_dados_gnre, "tipoGnre")
            tipoGnre.text = "0"# GNRE Simples

            t_contribuinteEmitente = ET.SubElement(t_dados_gnre, "contribuinteEmitente")
            t_identificacao = ET.SubElement(t_contribuinteEmitente, "identificacao")
            cnpj = ET.SubElement(t_identificacao, "CNPJ")
            cnpj.text = cnpj_fornecedor # Documento de identificação do emitente
            razaoSocial = ET.SubElement(t_contribuinteEmitente, "razaoSocial")
            razaoSocial.text = xml_data.razao_social 
            endereco = ET.SubElement(t_contribuinteEmitente, "endereco")
            endereco.text = xml_data.endereco
            municipio = ET.SubElement(t_contribuinteEmitente, "municipio")
            municipio.text = xml_data.cod_municipio[2:] # Código do municipio
            uf = ET.SubElement(t_contribuinteEmitente, "uf")
            uf.text = xml_data.uf_destinatario # Sigla do estado
            cep = ET.SubElement(t_contribuinteEmitente, "cep")
            cep.text = xml_data.cep # Cep

            t_itensGNRE = ET.SubElement(t_dados_gnre, "itensGNRE")
            item = ET.SubElement(t_itensGNRE, "item")
            receita = ET.SubElement(item, "receita")
            receita.text = "100099" # 100099 - ICMS Substituição Tributária por Operação
            documentoOrigem = ET.SubElement(item, "documentoOrigem")
            documentoOrigem.set("tipo", "24") # 24 - Chave de acesso da nota
            documentoOrigem.text = xml_data.chave
            produto = ET.SubElement(item, "produto")
            produto.text = "89" #Tipo de produto = Outros
            dataVencimento = ET.SubElement(item, "dataVencimento")
            dataVencimento.text = "2024-05-03" # Data vencimento
            valor_principal = ET.SubElement(item, "valor")
            valor_principal.set("tipo", "11") # 11 - Valor Principal
            valor_principal.text = str(icms_format) # Valor Principal
            valor_fecp = ET.SubElement(item, "valor")
            valor_fecp.set("tipo", "12") # 12 - Valor Fecp
            valor_fecp.text = str(fecp_format) # Valor Fecp

            t_contribuinteDestinatario = ET.SubElement(item, "contribuinteDestinatario")
            t_identificacao = ET.SubElement(t_contribuinteDestinatario, "identificacao")
            ie = ET.SubElement(t_identificacao, "IE")
            ins_estadual = df[df['Chave'] == xml_data.chave]['Insc. Estadual Dest.'].iloc[0]
            ie.text = str(ins_estadual) # Inscrição estadual do contribuinte destinatário

            t_camposExtras = ET.SubElement(item, "camposExtras")
            campoExtra1 = ET.SubElement(t_camposExtras, "campoExtra")
            codigo = ET.SubElement(campoExtra1, "codigo")
            codigo.text = "117"
            valor_dt = ET.SubElement(campoExtra1, "valor")
            valor_dt.text = "2024-05-03" # Data de emissão da GNRE
            campoExtra2 = ET.SubElement(t_camposExtras, "campoExtra")
            codigo = ET.SubElement(campoExtra2, "codigo")
            codigo.text = "118" 
            valor_dt = ET.SubElement(campoExtra2, "valor")
            valor_dt.text = f'Loja {str(loja)}' # Informações complementares

            t_valorGNRE = ET.SubElement(t_dados_gnre, "valorGNRE")
            t_valorGNRE.text = str(valor_total) # Valor Total da GNRE
            dataPagamento = ET.SubElement(t_dados_gnre, "dataPagamento")
            dataPagamento.text = "2024-05-03" # Data de pagamento

        # Criando a árvore XML
        tree = ET.ElementTree(root)

        # Salvando a árvore XML em um arquivo
        tree.write(f"xml-gnre-construidos/GNRE_UNICO.xml", encoding="utf-8", xml_declaration=True)
