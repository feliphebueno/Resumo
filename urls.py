"""
Created on Feb 21, 2017
URL Router
@author: rinzler

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from .views import Router

router = Router()

urlpatterns = [
	#Pesquisa index
    url(r'^$', router.index),

	#relatorio padrão: resumo/{protocolo}/
    url(r'^error/(.*/?)/$', router.index),
	
    #raw data
    url(r'^relatorio/raw/protocolo/(.*/?)/$', router.raw),
    
	#relatorio padrão: resumo/relatorio/protocolo/{protocolo}/
    url(r'^relatorio/protocolo/(.*/?)/$', router.relatorio),
	
	#relatorio padrão: resumo/{protocolo}/
    url(r'^(.*/?)/$', router.redirProtocolo),
]