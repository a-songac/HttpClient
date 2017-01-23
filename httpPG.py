'''
Created on Jan 21, 2017

@author: arno
'''

import socket
import argparse
import re

URL_REGEX = "^((http[s]?|ftp):\/)?\/?([^:\/\s\?]+)(:(\d+))?(\/([\w\/]+)(\.\w+)?)?(\?([\w=&]+))?$"
CRLF = '\r\n'
DEFAULT_PATH = "/"
DEFAULT_PORT = 80

# Usage: 
parser = argparse.ArgumentParser()
parser.add_argument('url', action="store")
parser.add_argument('--post', '-P', dest="verb", action="store_const",
                     const="POST", default="GET", help="HTTP Verb POST, or GET if not provided")
args = parser.parse_args()
url = args.url
verb = args.verb

# Parse input 
matcher = re.search(URL_REGEX, args.url)
host = matcher.group(3)
port = matcher.group(5)
path = matcher.group(6)

if port is None:
    port = DEFAULT_PORT

if path is None:
    path = DEFAULT_PATH

requestHeaders = ''
request = ''.join([verb, ' ', path, ' HTTP/1.1', CRLF, CRLF])

# Send Request
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                 
s.connect((host , port))
print(request)
s.send(request.encode())
print(s.recv(4096))
s.close    