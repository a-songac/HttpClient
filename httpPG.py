'''
Created on Jan 21, 2017

@author: arno
'''

import socket
import argparse
import re
import ArgumentParser

URL_REGEX = "^((http[s]?|ftp):\/)?\/?([^:\/\s\?]+)(:(\d+))?(\/([\w\/]+)(\.\w+)?)?(\?([\w=&]+))?$"
CRLF = '\r\n'
DEFAULT_PATH = "/"
DEFAULT_PORT = 80

mainParser = ArgumentParser.generateArgParsers()
args = mainParser.parse_args()
print(args)

url = args.url
 
# Parse input 
matcher = re.search(URL_REGEX, args.url)
host = matcher.group(3)
port = matcher.group(5)
path = matcher.group(6)
# 
# if port is None:
#     port = DEFAULT_PORT
# 
# if path is None:
#     path = DEFAULT_PATH
#     
# 
# request = ''.join([verb, ' ', path, ' HTTP/1.1', CRLF, CRLF])
# 
# if data is not None and verb == "POST":
#     request = ''.join([request, data])
#     headers = ''.join(['Content-Type'])
# 
# # Send Request
# print("Request to be sent:\r\n\r\n" + request)
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                 
# s.connect((host , port))
# s.send(request.encode())
# print("\r\nRESPONSE:" + "\r\n")
# print(s.recv(4096))
# s.close    

