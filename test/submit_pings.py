#!/usr/bin/env python
#
# Usage: submit_pings.py <directory containing *.json pings>
#
# Port number is 8080
#

import sys
import gzip
import requests
import os
import hashlib
import json


HOST_NAME = "127.0.0.1"
PORT_NUMBER = 8080

baseUrl = "http://" + HOST_NAME + ":" + str(PORT_NUMBER) + "/submit/telemetry"
#/submit/telemetry/00753794-0704-4534-9364-a64a88061777/saved-session/Firefox/38.0a1/nightly/20150219153629"

def Send(filename):
  data = open(filename, "r").read()
  ping = json.loads(data)

  hash = hashlib.md5(filename.encode()).hexdigest()
  guid = hash[:8] + "-" + hash[8:12] + "-" + hash[12:16] + "-" + hash[16:20] + "-" + hash[20:]

  url = baseUrl + "/" + guid + "/"
  if "ver" in ping:
    info = ping["info"]
    url += info["reason"] + "/"
    url += info["appName"] + "/"
    url += info["appVersion"] + "/"
    url += info["appUpdateChannel"] + "/"
    url += info["appBuildID"]
  elif "version" in ping:
    info = ping["payload"]["info"]
    app = ping["application"]
    url += ping["type"] + "/"
    url += app["name"] + "/"
    url += app["version"] + "/"
    url += app["channel"] + "/"
    url += app["buildId"]
  else:
    raise ValueError("Can't find ver or version in " + filename)

  gzipFile = gzip.open("temp.gz", "wb")
  gzipFile.write(data)
  gzipFile.close()
  compressed = open("temp.gz", "rb").read()

  res = requests.post(url=url, data=compressed, headers={"Content-Type": "gzip"})

  print "Submitted " + url
  print "\tfile:", filename
  print "\tguid:", guid, "\n"

pingFiles = []
for (dirpath, dirnames,filenames) in os.walk(sys.argv[1]):
  pingFiles.extend(os.path.join(dirpath, path) for path in filenames)
  break

for filename in pingFiles:
  if filename[-5:] == ".json":
    Send(filename)

