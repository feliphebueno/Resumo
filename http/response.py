'''
Created on 10 de jan de 2017
Abstract Response Object
@author: rinzler
'''
class Response():

    __statusCode    = 200
    __decoded       = {}
    __content       = {}
    __headers       = {}
    
    def __init__(self):
        return None

    def setStatusCode(self, statusCode):
        self.__statusCode = statusCode
        return self
    
    def getStatusCode(self):
        return self.__statusCode

    def setDecoded(self, data):
        self.__decoded = data
        return self

    def getDecoded(self):
        return self.__decoded

    def setContent(self, content):
        self.__content = content
        return self

    def getContent(self):
        return self.__content

    def setHeaders(self, headers):
        self.__headers = headers
        return self

    def getHeaders(self):
        return self.__headers
