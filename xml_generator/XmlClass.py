import xml.dom.minidom


class NFEXML:
    def __init__(self):
        self.chave = None
        self.cnpj_destinatario = None
        self.uf_destinatario = None
        self.mun = None
        self.razao_social = None
        self.endereco = None
        self.cep = None

    @staticmethod
    def xml_leitor(xml_arquivo):
        
        dom = xml.dom.minidom.parse(xml_arquivo)
        
        xml_obj = NFEXML()  
        
        try:
            xml_obj.cnpj_destinatario = dom.getElementsByTagName('CNPJ')[0].firstChild.data
            xml_obj.uf_destinatario = dom.getElementsByTagName('uf')[0].firstChild.data
            xml_obj.mun = dom.getElementsByTagName('municipio')[0].firstChild.data
            xml_obj.razao_social = dom.getElementsByTagName('razaoSocial')[0].firstChild.data
            xml_obj.endereco = dom.getElementsByTagName('endereco')[0].firstChild.data
            xml_obj.chave = dom.getElementsByTagName('documentoOrigem')[0].firstChild.data
            xml_obj.cep = dom.getElementsByTagName('cep')[0].firstChild.data
            
            return xml_obj
        
        except Exception as e:
            print("Erro ao processar XML:", e)
            return None  # Retorna None em caso de erro

leitor = NFEXML.xml_leitor(r'C:\Users\vlsilva\Documents\PYTHON PROJETOS\python_fiscal\Darj-Gnre_selenium\arquivo.xml')

print(f'Chave do XML: {leitor.chave}')