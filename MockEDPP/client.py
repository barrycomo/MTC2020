#!/usr/bin/python
import requests
import sys
import uuid
import base64

usercred = "username:password"
basicURL = "http://localhost:5000/api/v1/institutions/999999999/environments/TEST/products/EDPP/EDPP/collection?personid=AAA0001"
headers = {
  "Authorization": "Basic %s" % base64.b64encode(usercred.encode()).decode(),
  'Content-Type': 'application/json',
  'X-Request-ID': str(uuid.uuid4()),
  'X-Correlation-ID': str(uuid.uuid4()),
  'X-BusinessCorrelationId': str(uuid.uuid4()),
  'X-WorkflowCorrelationId': str(uuid.uuid4())
}

def verification():
  URL="http://localhost:5000/api/v1/institutions/999999999/environments/TEST/products/EDPP/EDPP/verification"
  Data = {
    "FirstName": "",
    "LastName": "andries",
    "TaxId": "",
    "DriverLicenseId": "",
    "DriverLicenseIssueState": "",
    "AccountId": "",
    "AccountType": ""
  }
  r = requests.post(url = URL, json = Data, headers = headers)
  resp = r.json()
  print("Response code:%s" % r.status_code)
  print("Response:%s"%resp)

def printCurl():
  print("curl -i ", end='')
  for key, value in headers.items():
    print("-H \"" + key + ": " + value + "\" ", end='')
  print(basicURL)

def getCollection(personid):
  URL="http://localhost:5000/api/v1/institutions/999999999/environments/TEST/products/EDPP/EDPP/collection?personid="+personid
  print("Request ID sent:%s"%headers['X-Request-ID'])
  r = requests.get(url = URL, headers=headers)
  resp = r.json()
  print("Response code:%s" % r.status_code)
  print("Request ID received:%s"%r.headers['X-Request-ID'])
  print("Response:%s"%resp)

def deleteCollection(personid):
  URL="http://localhost:5000/api/v1/institutions/999999999/environments/TEST/products/EDPP/EDPP/collection?personid="+personid
  r = requests.delete(url = URL, headers=headers)
  resp = r.json()
  print("Response:%s"%resp)

def status():
  URL="http://localhost:5000/api/v1/institutions/999999999/environments/TEST/products/EDPP/status"
  print("Request ID sent:%s"%headers['X-Request-ID'])
  r = requests.get(url = URL, headers=headers)
  resp = r.json()
  print("Response code:%s" % r.status_code)
  print("Request ID received:%s"%r.headers['X-Request-ID'])
  print("Response:%s"%resp)

def version():
  URL="http://localhost:5000/api/v1/institutions/999999999/environments/TEST/products/EDPP/status/version"
  print("Request ID sent:%s"%headers['X-Request-ID'])
  r = requests.get(url = URL, headers=headers)
  resp = r.json()
  print("Response code:%s" % r.status_code)
  print("Request ID received:%s"%r.headers['X-Request-ID'])
  print("Response:%s"%resp)


if len(sys.argv) >= 2:
  if sys.argv[1] == "1":
    verification()
  elif sys.argv[1] == "2":
    getCollection(sys.argv[2])
  elif sys.argv[1] == "3":
    deleteCollection(sys.argv[2])
  elif sys.argv[1] == "4":
    status()
  elif sys.argv[1] == "5":
    version()
  elif sys.argv[1] == "curl":
    printCurl()
else:
    print("Usage: client arg1 arg2 ")
    print("  Arg1:  1=verification, 2=get collection, 3=delete collection, 4=status, 5=version, curl=print curl cmd")
    

