'''
Generate Argument Parsers for the client tool

@author: arno
'''

import argparse

def generateArgParsers():
    parentParser = argparse.ArgumentParser(add_help=False, conflict_handler='resolve')
    parentParser.add_argument('-v',
                              dest="isVerbose",
                              action="store_const", const=True, default=False,
                              help="Prints the detail of the response such as protocol, status, and headers.")
    parentParser.add_argument('-H',
                              dest="headers",
                              action="append",
                              metavar="key:value",
                              help="Associates headers to HTTP Request with the format 'key:value'")
    
    parentParser.add_argument('URL', action="store", help="URL for the Http request")
    
    # Main Parse: httpc client
    mainParser = argparse.ArgumentParser(prog="httpc", description="httpc is a curl-like application but supports HTTP protocol only")
    
    subParsers = mainParser.add_subparsers(help='[command] help', dest="subparser_name")
    
    # GET command
    getParser = subParsers.add_parser('get',
                                      parents=[parentParser],
                                      help='Get executes a HTTP GET request for a given URL.')
    
    # POST command
    postParser = subParsers.add_parser('post', 
                                        parents=[parentParser],
                                        epilog="Either [-d] or [-f] can be used but not both.",
                                        help='Post executes a HTTP POST request for a given URL with inline data or from file.')
    postParser.add_argument('-d', dest="data", action="store",
                            metavar="inline-data",
                            help="Associates an inline data to the body HTTP POST")
    postParser.add_argument('-f', dest="file", action="store",
                            metavar="file",
                            help="Associates an inline data to the body HTTP POST")
    return mainParser

