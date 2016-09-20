#!/usr/bin/python
import httplib
import hashlib
def LoadDictionaryFromLines(lines):
  d = {}
  for line in lines:
    line = line.strip()
    if not line or line.startswith("#"):
      continue
    if "=" in line:
      name, value = line.split("=", 1)
      d[name] = value
  return d

def DumpInfoDict(d):
  for k, v in sorted(d.items()):
    print "%-25s = (%s) %s" % (k, type(v).__name__, v)

def main():
  conn = httplib.HTTPConnection("172.21.29.243", 80)
  conn.request("GET", "/test.php?version=TVOS.04.15.010.03.17")
  response = conn.getresponse()
  if response.status != httplib.OK:
    print response.status, response.reason
  data = response.read()
  #print data
  #conn.close()
  d = LoadDictionaryFromLines(data.split("\n"))
  DumpInfoDict(d)
  package_name = d["package_name"]
  md5_value = d["md5_value"]
  conn.request("GET", "/" + package_name)
  #conn.request("GET", "/aosp_mangosteen-ota-TVOS.04.15.010.03.17.zip")
  response_down = conn.getresponse()
  if response.status != httplib.OK:
    print response_down.status, response_down.reason
  data_down = response_down.read()
  md5_cal_value = hashlib.md5(data_down).hexdigest()
  if md5_value == md5_cal_value:
    print "OTA upgrade pacakge download finished\n"
    output_file = open(package_name, "w")
    output_file.write(data_down)
    output_file.close()
  conn.close()

if __name__ == '__main__':
  main()