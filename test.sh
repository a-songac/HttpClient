#! /bin/bash

# Show usage
echo "EXECUTE: ./httpc.py -h"
./httpc.py -h

echo "EXECUTE: ./httpc.py get -h"
./httpc.py get -h

echo "EXECUTE: ./httpc.py post -h"
./httpc.py post -h


# Test GET methods
echo "EXECUTE: ./httpc.py get httpbin.org/get"
./httpc.py get httpbin.org/get

echo "EXECUTE: ./httpc.py get -v httpbin.org/get"
./httpc.py get -v httpbin.org/get

echo "EXECUTE: ./httpc.py get httpbin.org/get -o output.txt"
./httpc.py get httpbin.org/get -o output.txt
echo "EXECUTE cat output.txt"
cat output.txt

echo "EXECUTE: ./httpc.py get -v -H Connection:close httpbin.org/get"
./httpc.py get -v -H Connection:close httpbin.org/get


rm output.txt


# Test POST methods
echo "EXECUTE ./httpc.py post -H Content-type:application/json -d '{"Assignment": 1}' -v http://httpbin.org/post"
./httpc.py post -H Content-type:application/json -d '{"Assignment": 1}' -v http://httpbin.org/post

echo "EXECUTE ./httpc.py post -H Content-type:application/x-www-form-urlencoded -f input.txt httpbin.org/post"
./httpc.py post -H Content-type:application/x-www-form-urlencoded -f input.txt httpbin.org/post

echo "EXECUTE ./httpc.py post -H Content-type:application/x-www-form-urlencoded -d name=arno -v http://httpbin.org/post"
./httpc.py post -H Content-type:application/x-www-form-urlencoded -d "name=arno" -v http://httpbin.org/post

echo "EXECUTE ./httpc.py post -H Content-type:application/x-www-form-urlencoded -d 'some' -f 'some' -v http://httpbin.org/post" 
./httpc.py post -H Content-type:application/x-www-form-urlencoded -d 'some' -f 'some' -v http://httpbin.org/post







