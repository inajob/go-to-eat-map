import json
import urllib.request
import urllib.parse
import time
import sys
import os
from xml.dom.minidom import parseString

appid = os.environ["YAHOO_APPID"]

def geocode(address):
  query = urllib.parse.quote(address)
  url = "https://map.yahooapis.jp/geocode/V1/geoCoder?appid=%s&query=%s&output=json" % (appid, query)
  coord = ""
  with urllib.request.urlopen(url) as response:
     sjson = response.read()
     obj = json.loads(sjson)
     coord = (obj["Feature"][0]["Geometry"]["Coordinates"])
  parts = coord.split(",")
  lon = float(parts[0])
  lat = float(parts[1])
  return [lat, lon]


def geocode2(address):
  query = urllib.parse.quote(address)
  url = "https://www.geocoding.jp/api/?q=%s" % (query)
  lat = 0
  lon = 0
  with urllib.request.urlopen(url) as response:
     sxml = response.read()
     obj = parseString(sxml)
     lat = obj.getElementsByTagName("lat")[0].childNodes[0].data
     lon = obj.getElementsByTagName("lng")[0].childNodes[0].data
  time.sleep(10)
  return [lat, lon]

pref = sys.argv[1]

output = []
with open("../data/raw-%s.txt" % (pref),'r', encoding="utf8") as f:
  while True:
    name = f.readline()
    if not(name):
      break;
    name = name.rstrip()
    dummy1 = f.readline()
    zipcode = f.readline().rstrip()
    address = f.readline().rstrip()
    tel = f.readline().rstrip()
    dummy2 = f.readline()
    dummy3 = f.readline()
    latlon = [0,0]
    try:
      latlon = geocode(address)
    except:
      print("error")
    if latlon[0] == 0:
      try:
        latlon = geocode2(address)
      except:
        print("2nd error")
    print(name,zipcode,address,tel)
    output.append({'name': name, "zipcode": zipcode, "address": address, "tel": tel, "lat": latlon[0], "lon": latlon[1]})

print("parse OK.")
with open('../data/%s.js' % (pref), 'w') as f:
  sjson = json.dumps(output, indent=4)
  f.write(("var data_%s = " % (pref)) + sjson);
print("../data/%s.js dumped." % pref)
