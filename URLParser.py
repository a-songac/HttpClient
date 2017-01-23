import re

URL_REGEX = "^((http[s]?|ftp):\/)?\/?([^:\/\s\?]+)(:(\d+))?(\/([\w\/]+)(\.\w+)?)?(\?([\w=&]+))?$"
CRLF = '\r\n'


# Parse input 
matcher = re.search(URL_REGEX, args.url)
host = matcher.group(3)
port = matcher.group(5)
path = matcher.group(6)