#!/usr/bin/python3
'''
Created on Jan 21, 2017

@author: arno
'''

import socket
import re
import ArgumentParser
import sys

POST = "POST"
GET = "GET"
URL_REGEX = "^((http[s]?|ftp):\/)?\/?((www\.)?([^:\/\s\?]+))(:(\d+))?(\/([\w\/]+)(\.\w+)?)?(\?([\w=&]+))?$"
CRLF = '\r\n'
DEFAULT_PATH = "/"
DEFAULT_PORT = 80
contentType = "Content-Type: {content_type}"
contentLength = "Content-length: {content_length}"
hostName = "Host: {host_name}"
CONNECTION_CLOSE = "Connection: Keep-Alive"


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
    
# #######################
# Build HTTP request
# ####################### 
def buildRequest(url, verb, host, port, path, data, file):

    headersJson = {}
    
    if headers is not None:
        for header in headers:
            splittedHeader = header.split(':')
            headersJson[splittedHeader[0]]  = splittedHeader[1]
    
    if port is None:
        port = DEFAULT_PORT
     
    if path is None:
        path = DEFAULT_PATH
         
    request = ''.join([verb, ' ', path, ' HTTP/1.1', CRLF])
    
    request = ''.join([request,
                       hostName.format(host_name = str(host)), CRLF,
                       CONNECTION_CLOSE, CRLF, CRLF
                       ])
    
    if verb == POST:
        parameters = ''
        if file is None:
            parameters = data
        else:
            f = open(file, 'r')
            for line in f:
                if line:
                    parameters += line.rstrip('\n') + '&'
    
        if parameters[-1] == '&':
            parameters = parameters.rstrip('&')
    
        data_bytes = parameters.encode()
        request = ''.join([request,
                           contentLength.format(content_length = len(data_bytes)), CRLF,
                           parameters])
        
    request = ''.join([request, CRLF])
    
    if headersJson:
        for key, value in headersJson.items():
            request = ''.join([request, key,  ':' , value , CRLF])
            
    
    return request

# #######################
# Process Http Request
# ####################### 
def processRequest(request, verb, host, port, data, file, verbose, outputFile):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host , port))
        s.send(request.encode())
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
        host = matcher.group(5)
        port = matcher.group(7)
        if port is None:
            port = DEFAULT_PORT
            
        path = matcher.group(8)
        if path is None :
            path = DEFAULT_PATH
        print(responseHeadersArr[0])
        print("Redirect url: ", newUrl)
        answer = input("Do you accept to follow the redirection link? [Y/n]: ")
        if answer != 'n' :
            newRequest = buildRequest(newUrl, verb, host, port, path, data, file)
            processRequest(newRequest, verb, host, port, data, file, verbose, outputFile)
        
    else :
        finalOutput = ''
        if verbose:
            finalOutput = responseArr[0]
            
        finalOutput = ''.join([finalOutput, CRLF, CRLF, responseArr[1]])
        
        if outputFile is None :
            print(finalOutput)
        else :
            f = open(outputFile, 'w')
            f.write(finalOutput)
            f.close()
    
    return


# #######################
# Execution
# ####################### 

mainParser = ArgumentParser.generateArgParsers()
args = mainParser.parse_args()

url = args.URL
headers = args.headers
verb = args.subparser_name.upper()
verbose = args.isVerbose
outputFile = args.outputFile
if verb == POST:
    data = args.data
    file = args.file
else:
    data = file = None

matcher = re.search(URL_REGEX, url)
host = matcher.group(5)
port = matcher.group(7)
if port is None:
    port = DEFAULT_PORT
    
path = matcher.group(8)
if path is None :
    path = DEFAULT_PATH

request = buildRequest(url, verb, host, port, path, data, file)
processRequest(request, verb, host, port, data, file, verbose, outputFile)



