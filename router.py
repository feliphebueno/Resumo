'''
Created on Feb 21, 2017
@author: rinzler
'''
from django.shortcuts import render, redirect
from resumo.services.relatorio import Relatorio
from resumo.config import URL_APP, URL_STATIC

# Create your views here.

class Router(object):

	#metodos das actions
	def index(self, request, error=None):
		return render(request, 'home/index.html', {
			'urlLibrary': URL_STATIC +"/LibraryJS",
			'URL_STATIC': URL_STATIC,
			'URL_APP': URL_APP,
			'error': '' if error == None else self.getErrorByCod(error)
		})

	def relatorio(self, request, protocolo):
		
		dados = Relatorio().getDadosProtocolo(protocolo)
		if(dados == False):
			return self.redirErro(request, '005')
		else:
			return render(request, 'relatorio/lista.html', {
				'dados': dados,
				'URL_STATIC': URL_STATIC,
				'URL_APP': URL_APP,
			})

	def raw(self, request, protocolo):

		dados = Relatorio().getDadosRaw(protocolo)
		if(dados == False):
			return self.redirErro(request, '001')
		else:
			return render(request, 'relatorio/raw.html', {
				'dados': dados[35:(len(dados) - 1)]
			}, content_type="application/json; charset=utf-8")

	#Redirects
	def redirProtocolo(self, request, protocolo):
		return redirect('/resumo/relatorio/protocolo/{0}/'.format(protocolo))

	def redirErro(self, request, error):
		return redirect('/resumo/error/{0}/'.format(error))

	#Métodos axiliares
	def getErrorByCod(self, code=None):
		errors = {
			'000': "Não foi possível processar sua solicitação. Tente novamente.",
			'001': "Protocolo inválido",
			'002': "Informe um protocolo válido",
		}

		if(code in errors):
			return errors[code]
		else:
			return errors['000']

