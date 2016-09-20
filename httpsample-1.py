#!/usr/bin/python
import httplib
conn = httplib.HTTPConnection("172.21.29.243", 80)
conn.request("GET", "/test.php?version=TVOS.04.15.010.03.17")
response = conn.getresponse()
print response.status, response.reason
data = response.read()
print data
conn.close()
