#!/usr/bin/python3
'''
Created on Jan 21, 2017

@author: arno
'''

import socket
import re
import sys


POST = "POST"
GET = "GET"
URL_REGEX = "((http[s]?|ftp):\/)?\/?((www\.)?([^:\/\s\?]+))(:(\d+))?(\/[\w\/]*)?(\.\w+)?(\?([\w=&]+))?"
# URL_REGEX = "((http[s]?|ftp):\/)?\/?((www\.)?([^:\/\s\?]+))(:(\d+))?(\/([\w\/]+)?(\.\w+)?)?(\?([\w=&]+))?"
CRLF = '\r\n'
DEFAULT_PATH = "/"
DEFAULT_PORT = 80
contentType = "Content-Type: {content_type}"
contentLength = "Content-length: {content_length}"
hostName = "Host: {host_name}"
CONNECTION_CLOSE = "Connection: Keep-Alive"

class HttpRequest:
    
    def __init__(self, url, verb, headers, host, port,
                  path, data, file, verbose, outputFile):
        self.verb = verb
        self.headers = headers
        self.host = host
        self.port = DEFAULT_PORT
        if port is not None :
            self.port = port
        self.path = DEFAULT_PATH
        if path is not None :
            self.path = path
        self.data = data
        self.file = file
        self.verbose = verbose
        self.outputFile = outputFile
        return
        
        
        
    # #######################
    # Build HTTP request
    # ####################### 
    def buildRequest(self):
    
        headersJson = {}
        
        if self.headers is not None:
            for header in self.headers:
                splittedHeader = header.split(':')
                headersJson[splittedHeader[0]]  = splittedHeader[1]

        request = ''.join([self.verb, ' ', self.path, ' HTTP/1.1', CRLF])
        
        request = ''.join([request,
                           hostName.format(host_name = str(self.host)), CRLF,
                           CONNECTION_CLOSE, CRLF
                           ])
        if headersJson:
            for key, value in headersJson.items():
                request = ''.join([request, key,  ':' , value , CRLF])


        if self.verb == POST:
            parameters = ''
            if self.file is None:
                parameters = self.data
            else:
                f = open(self.file, 'r')
                for line in f:
                    if line:
                        parameters += line.rstrip('\n') + '&'
        
            if parameters[-1] == '&':
                parameters = parameters.rstrip('&')
        
            data_bytes = parameters.encode()
            request = ''.join([request,
                               contentLength.format(content_length = len(data_bytes)), CRLF, CRLF,
                               parameters])
            
        request = ''.join([request, CRLF])



        
        self.request = request
        print(request)
        return
        
        
        
        
        
        
    # #######################
    # Process Http Request
    # ####################### 
    def processRequest(self):
        
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # SOCK_STREAM for TCP
            s.connect((self.host , self.port))
            s.send(self.request.encode())
            responseBytes = s.recv(4096)
            response = responseBytes.decode()
        except:
            print("An error occurred, please retry: ", sys.exc_info())
            sys.exit(0)
        
        
        responseArr = response.split(CRLF+CRLF)
        responseHeaders = responseArr[0]
        responseHeadersArr = responseHeaders.split(CRLF)
        responseStatus = parseResonseStatus(responseHeaders)
        
        if responseStatus >= 300 and responseStatus < 400 :
            
            newUrl = parseRedirectUrlFor300(response)
            matcher = re.search(URL_REGEX, newUrl)
            self.host = matcher.group(5)
            self.port = matcher.group(7)
            if self.port is None:
                self.port = DEFAULT_PORT
                
            self.path = matcher.group(8)
            if self.path is None :
                self.path = DEFAULT_PATH
            print(responseHeadersArr[0])
            print("Redirect url: ", newUrl)
            answer = input("Do you accept to follow the redirection link? [Y/n]: ")
            if answer != 'n' :
                self.buildRequest()
                self.processRequest()
            
        else :
            finalOutput = ''
            if self.verbose:
                finalOutput = responseArr[0]
                
            finalOutput = ''.join([finalOutput, CRLF, CRLF, responseArr[1]])
            
            if self.outputFile is None :
                print(finalOutput)
            else :
                f = open(self.outputFile, 'w')
                f.write(finalOutput)
                f.close()
        
        return

    


# #######################
# Extract response status
# ####################### 
def parseResonseStatus(responseHeaders):
    responseHeadersArr = responseHeaders.split(CRLF)
    responseStatus = int(responseHeadersArr[0].split(' ')[1])
    return responseStatus

# #######################
# Extract redirect url
# ####################### 
def parseRedirectUrlFor300(responseBody):
    pattern = re.search('(Location: )(.+)', responseBody)
    return pattern.group(2)
    return "http://httpbin.org/get"
    







