'''
Created on Jan 21, 2017

@author: arno
'''

import socket
import re
import ArgumentParser

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

mainParser = ArgumentParser.generateArgParsers()
args = mainParser.parse_args()

url = args.URL
headers = args.headers
verb = args.subparser_name.upper()
verbose = args.isVerbose
outputFile = args.outputFile

data = file = None

matcher = re.search(URL_REGEX, url)
host = matcher.group(5)
port = matcher.group(7)
path = matcher.group(8)
params = matcher.group(12)

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
                   hostName.format(host_name = str(host) + ":" + str(port)), CRLF,
                   CONNECTION_CLOSE, CRLF, CRLF
                   ])

if verb == POST:
    parameters = ''
    data = args.data
    file = args.file
    if file is None:
        parameters = args.data
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

# Send Request
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host , port))
s.send(request.encode())
responseBytes = s.recv(4096)
response = responseBytes.decode()

finalOutput = ''
responseHeaders = response.split(CRLF+CRLF)
if verbose:
    finalOutput = responseHeaders[0]
    
finalOutput = ''.join([finalOutput, CRLF, CRLF, responseHeaders[1]])

if outputFile is None :
    print(finalOutput)
else :
    f = open(outputFile, 'w')
    f.write(finalOutput)
    f.close()


