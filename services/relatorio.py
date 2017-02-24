'''
Created on Feb 21, 2017
Relatório service - responsável pela recuperação dos dados a serem exibidos.
@author: rinzler
'''

from resumo.http.request import Request
from resumo.config import URL_IPRESB_API
from builtins import list
import sys
from datetime import datetime

class Relatorio(object):
    '''
    classdocs
    '''

    __api = Request(base_uri=URL_IPRESB_API)
    #__api = Request(base_uri='http://localhost/')

    def __init__(self):
        '''
        Constructor
        '''
        
    def getDadosProtocolo(self, protocolo):
        if(protocolo.strip()):
            try:
                request = self.__api.get('resumo/{0}/'.format(protocolo))
                #request = self.__api.get('resumo.json')
                
                dados = request.getDecoded()

                if('data' in dados):
                    return self.preparaDadosRelatorio(dados['data'])
                else:
                    return False
            except(BaseException) as e:
                print(e)
                sys.exit()
                return False
        else:
            return False

    def getDadosRaw(self, protocolo):
        if(protocolo.strip()):
            try:
                request = self.__api.get('resumo/{0}/'.format(protocolo))
                #request = self.__api.get('resumo.json')
                
                dados = request.getContent()

                if(len(dados) > 0):
                    return dados
                else:
                    return False
            except(BaseException) as e:
                print(e)
                sys.exit()
                return False
        else:
            return False

    def preparaDadosRelatorio(self, dados):

        pessoa = {
            'foto'          : dados['pessoa']['foto'],
            'nome'          : dados['pessoa']['nome'],
            'cpf'           : "{0}.{1}.{2}-{3}".format(dados['pessoa']['cpf'][0:3], dados['pessoa']['cpf'][3:6], dados['pessoa']['cpf'][6:9], dados['pessoa']['cpf'][9:12]),
            'nascimento'    : datetime.strptime(dados['pessoa']['nascimento'], '%Y-%m-%d'),
            'sexo'          : dados['pessoa']['sexo'],
            'estado_civil'  : dados['pessoa']['estado_civil']['est_civil_nome'],
            'escolaridade'  : dados['pessoa']['escolaridade']['escol_nome']
        }

        documentos = {
            'identidade': dados['pessoa']['identidade'],
            'ctps': dados['pessoa']['ctps'],
            'titulo_eleitoral': dados['pessoa']['titulo_eleitoral']
        }

        documentos['ctps']['ctps_data_emissao']             = datetime.strptime(dados['pessoa']['ctps']['ctps_data_emissao'], '%Y-%m-%d') if 'ctps_data_emissao' in dados['pessoa']['ctps'] else None
        documentos['identidade']['identidade_data_emissao'] = datetime.strptime(dados['pessoa']['identidade']['identidade_data_emissao'], '%Y-%m-%d')

        contatos = {
            'telefones': self.organizaTelefones(dados['pessoa']['telefones']),
            'emails': dados['pessoa']['emails']
        }

        servidor = {
            'previdencia': dados['previdencia'],
            'matriculas': self.organizaMatriculas(dados['matriculas']),
        }

        confirmacao                 = dados['confirmacao']
        confirmacao['data_hora']    = datetime.strptime(dados['confirmacao']['data_hora'], '%Y-%m-%d %H:%M:%S')

        avaliacao                 = dados['avaliacao'] if 'avaliacao' in dados else dict()
        avaliacao['data_hora']    = datetime.strptime(avaliacao['data_hora'], '%Y-%m-%d %H:%M:%S') if 'data_hora' in avaliacao else None

        confirmacao['protocolo_limpo'] = dados['confirmacao']['protocolo']
        confirmacao['protocolo'] = "{0}-{1}-{2}".format(dados['confirmacao']['protocolo'][0:4], dados['confirmacao']['protocolo'][4:8], dados['confirmacao']['protocolo'][8:12])

        return {
            'pessoa': pessoa,
            'documentos': documentos,
            'contatos': contatos,
            'enderecos': dados['pessoa']['enderecos'],
            'dependentes': dados['pessoa']['dependente'],
            'servidor': servidor,
            'digitalizacao': self.organizaDigitalizacoes(dados['digitalizacoes']),
            'biometria': self.organizaBios(dados['biometria']),
            'confirmacao': confirmacao,
            'avaliacao': avaliacao
        }

    def organizaMatriculas(self, matriculas):

        retorno = list()

        for linhas in matriculas:
            for mat in linhas.keys():
                linha = linhas[mat]
                linha['matricula'] = mat
                retorno.append(linha)
        
        return retorno

    def organizaDigitalizacoes(self, digitalizacoes):

        retorno = {
            'docs': list(),
            'tipos': list(),
        }

        for tipo in digitalizacoes['drive_files']:

            tipo_desc = digitalizacoes['upload_tipo_lista'][tipo]
            retorno['tipos'].append(tipo_desc)

            for doc in digitalizacoes['drive_files'][tipo]:
                doc['tipo'] = tipo_desc
                linha = doc
                retorno['docs'].append(linha)

        return retorno

    def organizaTelefones(self, telefones):
        
        fixo   = list()
        movel  = list()
        
        for telefone in telefones:
            if(telefone['tipo'] == 'F'):
                fixo.append(telefone)
            else:
                movel.append(telefone)
        
        return {
            'fixo': fixo,
            'movel': movel,
        }
        
    def organizaBios(self, bios):
        
        direita    = list()
        esquerda   = list()

        for bio in bios: 
            if(bio['bio_id'] <= 5):
                direita.append(bio)
            else:
                esquerda.append(bio)

        return {
            'direita': direita,
            'esquerda': esquerda
        }



