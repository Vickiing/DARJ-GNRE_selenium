import xml.etree.ElementTree as ET

# Criando o elemento raiz
root = ET.Element("TLote_GNRE")
root.set("xmlns", "http://www.gnre.pe.gov.br")
root.set("versao", "2.00")

# Adicionando o elemento 'guias' como filho do elemento raiz
guias = ET.SubElement(root, "guias")

# Adicionando o elemento 'TDadosGNRE' como filho do elemento 'guias'
t_dados_gnre = ET.SubElement(guias, "TDadosGNRE")
t_dados_gnre.set("versao", "2.00")

# Adicionando os elementos dentro de 'TDadosGNRE' conforme o exemplo fornecido
uf_favorecida = ET.SubElement(t_dados_gnre, "ufFavorecida")
uf_favorecida.text = "RJ"
tipoGnre = ET.SubElement(t_dados_gnre, "tipoGnre")
tipoGnre.text = "0"

t_contribuinteEmitente = ET.SubElement(t_dados_gnre, "contribuinteEmitente")
t_identificacao = ET.SubElement(t_contribuinteEmitente, "identificacao")
cnpj = ET.SubElement(t_identificacao, "CNPJ")
cnpj.text = "02106825000463"
razaoSocial = ET.SubElement(t_contribuinteEmitente, "razaoSocial")
razaoSocial.text = "GRANO ALIMENTOS S A - SP - 418331" 
endereco = ET.SubElement(t_contribuinteEmitente, "endereco")
endereco.text = "AV DR GASTAO VIDIGAL 1946 - VILA LEOPOLDINA"
municipio = ET.SubElement(t_contribuinteEmitente, "municipio")
municipio.text = "50308"
uf = ET.SubElement(t_contribuinteEmitente, "uf")
uf.text = "SP"
cep = ET.SubElement(t_contribuinteEmitente, "cep")
cep.text = "05316900"


t_itensGNRE = ET.SubElement(t_dados_gnre, "itensGNRE")
item = ET.SubElement(t_itensGNRE, "item")
receita = ET.SubElement(item, "receita")
receita.text = "100099"
documentoOrigem = ET.SubElement(item, "documentoOrigem")
documentoOrigem.set("tipo", "24")
documentoOrigem.text = "35240402106825000463550400005300461793586078"
produto = ET.SubElement(item, "produto")
produto.text = "89"
dataVencimento = ET.SubElement(item, "dataVencimento")
dataVencimento.text = "2024-05-03"
valor_principal = ET.SubElement(item, "valor")
valor_principal.set("tipo", "11")
valor_principal.text = "6232.98"
valor_fecp = ET.SubElement(item, "valor")
valor_fecp.set("tipo", "12")
valor_fecp.text = "623.30"

t_contribuinteDestinatario = ET.SubElement(item, "contribuinteDestinatario")
t_identificacao = ET.SubElement(t_contribuinteDestinatario, "identificacao")
ie = ET.SubElement(t_identificacao, "IE")
ie.text = "81916527"


t_camposExtras = ET.SubElement(item, "camposExtras")
campoExtra1 = ET.SubElement(t_camposExtras, "campoExtra")
codigo = ET.SubElement(campoExtra1, "codigo")
codigo.text = "117"
valor_dt = ET.SubElement(campoExtra1, "valor")
valor_dt.text = "2024-05-03"
campoExtra2 = ET.SubElement(t_camposExtras, "campoExtra")
codigo = ET.SubElement(campoExtra2, "codigo")
codigo.text = "118"
valor_dt = ET.SubElement(campoExtra2, "valor")
valor_dt.text = "loja 3085"

t_valorGNRE = ET.SubElement(t_dados_gnre, "valorGNRE")
t_valorGNRE.text = "6856.28"
dataPagamento = ET.SubElement(t_dados_gnre, "dataPagamento")
dataPagamento.text = "2024-05-03"


# Criando a árvore XML
tree = ET.ElementTree(root)

# Salvando a árvore XML em um arquivo
tree.write("arquivo.xml", encoding="utf-8", xml_declaration=True)
