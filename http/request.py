'''
Created on 4 de jan de 2017

@author: rinzler
'''
import json, sys
import requests
from resumo.http.response import Response
from builtins import BaseException


class Request():
    '''
    Classe responsável pela abstração das requisições http
    @var str: method
    @var str: base_uri
    @var str: jwt
    @var dict: payload
    @var dict: headers
    '''

    method = str()
    base_uri = str()
    jwt = str()
    payload = dict()
    headers = dict()

    # classes auxiliares
    response = None

    def __init__(self, base_uri='http://localhost:8000/'):
        '''
        Constructor
        '''
        # setting some vales
        self.setBaseUri(base_uri)

    def get(self, end_point='/'):
        self.__setMethod("GET")
        return self.__request(end_point)

    def post(self, end_point='/', payload=dict()):
        self.__setMethod("POST")
        self.__setPayload(payload)
        return self.__request(end_point)

    def put(self, end_point='/', payload=dict()):
        self.__setMethod("PUT")
        self.__setPayload(payload)
        return self.__request(end_point)

    def delete(self, end_point='/', payload=dict()):
        self.__setMethod("DELETE")
        self.__setPayload(payload)
        return self.__request(end_point)

    def __request(self, end_point):
        """
        executa a requisição montada
        @return: Response
        """
        # final url
        url = self.getBaseUri() + end_point

        # configuration
        conf = self.config()

        try:
            method = self.getMethod()
            if (method == 'GET'):
                request = requests.get(url, headers=conf['headers'])
            elif (method == 'POST'):
                request = requests.post(url, headers=conf['headers'], data=conf['payload'])
            else:
                request = requests.put(url, data=conf['payload'], headers=conf['headers'])

            # Response object
            response = Response()

            # Set Response properies
            response.setContent(request.text)
            response.setStatusCode(request.status_code)
            response.setHeaders(request.headers)

            try:
                response.setDecoded(request.json())
            except(BaseException) as e:
                response.setDecoded(dict())

            # return Response() Object
            return response
        except(BaseException) as e:
            print("Falha na requisicao.")
            self.error.write(str(e) + "\n")
            sys.exit(1)

    def config(self):
        """
        monta a configuração da request
        @return: dict
        """
        conf = dict()
        headers = self.getHeaders()
        payload = self.getPayload()
        jwt = self.getJwt()

        # Inicializando...
        conf['headers'] = dict()
        conf['payload'] = dict()

        if (len(headers) > 0):
            conf['headers'] = headers

        if (jwt != ''):
            conf['headers']['Authorization'] = 'Bearer ' + jwt

        if (self.method != 'GET' and self.method != 'HEAD'):
            conf['payload'] = json.dumps(payload)

        return conf

    def getResponseDecode(self):
        if (self.response == None):
            raise BaseException("No request has been sent.")
        else:
            return self.response.json()

    def setBaseUri(self, base_uri):
        self.base_uri = base_uri
        return self

    def getBaseUri(self):
        return self.base_uri

    def setJwt(self, jwt):
        self.jwt = jwt
        return self

    def getJwt(self):
        return self.jwt

    def setResponse(self, response):
        self.response = response
        return self

    def getResponse(self):
        return self.response

    def __setPayload(self, payload):
        self.payload = payload
        return self

    def getPayload(self):
        return self.payload

    def setHeaders(self, headers):
        self.headers = headers
        return self

    def getHeaders(self):
        return self.headers

    def __setMethod(self, method):
        self.method = method
        return self

    def getMethod(self):
        return self.method
