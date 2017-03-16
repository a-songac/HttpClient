#!/usr/bin/python3
'''
Created on Jan 21, 2017

@author: arno
'''

import re
import ArgumentParser
import HttpcHelper
from HttpcHelper import HttpRequest


mainParser = ArgumentParser.generateArgParsers()
args = mainParser.parse_args()


url = args.URL
headers = args.headers
verb = args.subparser_name.upper()
verbose = args.isVerbose
outputFile = args.outputFile
if verb == HttpcHelper.POST:
    data = args.data
    file = args.file
    if args.data is not None and args.file is not None:
        print("Cannot have both data and file for POST input")
        exit()
else:
    data = file = None

matcher = re.search(HttpcHelper.URL_REGEX, url)
host = matcher.group(5)
port = matcher.group(7)
path = matcher.group(8)

httpRequest = HttpRequest(url, verb, headers, host, port, path, data, file, verbose, outputFile)
httpRequest.buildRequest()
httpRequest.processRequest()



