import xml.dom.minidom

class NFEXML:
    def __init__(self, xml_file_path):
        self.xml_file_path = xml_file_path
        self.chave = None
        self.cnpj_destinatario = None
        self.uf_destinatario = None
        self.mun = None
        self.razao_social = None
        self.endereco = None
        self.cep = None
        self.ler_xml()

    def ler_xml(self):
        try:
            dom = xml.dom.minidom.parse(self.xml_file_path)
            self.chave = dom.getElementsByTagName('chNFe')[0].firstChild.data
            self.cnpj_destinatario = dom.getElementsByTagName('CNPJ')[0].firstChild.data
            self.uf_destinatario = dom.getElementsByTagName('UF')[0].firstChild.data
            self.mun = dom.getElementsByTagName('xMun')[0].firstChild.data
            self.razao_social = dom.getElementsByTagName('xNome')[0].firstChild.data
            self.endereco = dom.getElementsByTagName('xLgr')[0].firstChild.data
            self.cep = dom.getElementsByTagName('CEP')[0].firstChild.data
        except Exception as e:
            print(e)

# Exemplo de uso:
caminho_xml = r'C:\Users\vlsilva\Documents\PYTHON PROJETOS\python_fiscal\Darj_selenium\arquivo_xml\33230629020880000140550220003228301074967910-procNFe.xml'
nf = NFEXML(caminho_xml)
print(nf.chave)
print(nf.cnpj_destinatario)
