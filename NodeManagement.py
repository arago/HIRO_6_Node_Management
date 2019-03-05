import requests
import json
import glob
import re
import urllib3
import urllib
import logging

# You must initialize logging, otherwise you'll not see debug output.
#logging.basicConfig()
#logging.getLogger().setLevel(logging.DEBUG)
#requests_log = logging.getLogger("requests.packages.urllib3")
#requests_log.setLevel(logging.DEBUG)
#requests_log.propagate = True


print("Loading Data to Graph Node.")
print("---------------------------------------------------------------------")


##Get pip: curl https://bootstrap.pypa.io/get-pip.py | python3


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def findEnv():
   findToken = input("Do you have a token? (y) (n) ")
   type(findToken)
   findToken = findToken.lower()
   if findToken == "y":
        parsedToken = input("Please enter the token. ")
        findGraph = input("What is the IP of your Graph node? ")
        type(findGraph)
        findStyle(findGraph,parsedToken)
        return
   findWS02 = input("What is the IP of your WSO2 node? ")
   type(findWS02)
   findGraph = input("What is the IP of your Graph node? ")
   type(findGraph)
   findKey = input("What is the client_key for the account you will be using to upload? ")
   type(findKey)
   findSecret = input("What is the client_secret for the account you will be using to upload? ")
   type(findSecret)
   iamurl = "https://{0}:9443/oauth2/token".format(findWS02)
   data = {}
   data["grant_type"] = "client_credentials"
   data["scope"] = "batchjob"
   data["client_id"] = findKey
   data["client_secret"] = findSecret
   headers = {'Content-Type':'application/x-www-form-urlencoded;charset=UTF-8'}
   token = requests.post(iamurl, params=data, headers=headers, verify=False)
   parsedToken = json.loads(token.text)
   parsedToken = parsedToken['access_token']
   print("Your token is: " + parsedToken)
   findStyle(findGraph,parsedToken)
   return


def createNodes(graph,parsedToken):
   print("You chose to create new nodes.")
   findJSON = input("Where is the JSON stored? ie. /tmp/Nodes.json ")
   type(findJSON)
   findnType = input("What is the node type? ie. ogit/Place/Region ")
   type(findnType)
   nType = urllib.parse.quote_plus(findnType)
   headers = {'Content-Type': 'application/json', '_TOKEN':parsedToken}
   graphurl = "https://{0}/new/".format(graph)
   myCounter = 0
   with open(findJSON) as fp:
       line = fp.readline()
       cnt = 1
       while line:
          # print("Line {}: {}".format(cnt, line.strip()))
           upload = requests.post(graphurl + nType, data=line.encode('utf-8'), headers=headers, verify=False)
           print(upload.url)
           line = fp.readline()
           cnt += 1
           myCounter += 1
           print(upload.text)
           if "literal" in upload.text:
              myCounter -= 1
   print("Creation finished! " + str(myCounter) + " nodes created.")
   continueWork(graph,parsedToken)
   return

def createEdges(graph,parsedToken):
   print("You chose to create new edges. Only a single edge type can be created at once. ")
   findeType = input("What is the edge type? ie. ogit/contains ")
   type(findeType)
   eType = urllib.parse.quote_plus(findeType)
   findOut = input("What is the ID of the out node? ie. cfjdddkkssjddfhdd ")
   type(findOut)
   findJSON = input("Where are the IDs of the in nodes stored? ie. /tmp/Nodes.json ")
   type(findJSON)
   headers = {'Content-Type': 'application/json', '_TOKEN':parsedToken}
   graphurl = "https://{0}/connect/".format(graph)
   myCounter = 0
   with open(findJSON) as fp:
       line = fp.readline()
       cnt = 1
       while line:
           line = line.rstrip()
           data = {"out": findOut, "in": line}
          # print("Line {}: {}".format(cnt, line.strip()))
           upload = requests.post(graphurl + eType, json=data, headers=headers, verify=False)
           print(upload.url)
           line = fp.readline()
           cnt += 1
           myCounter += 1
           print(upload.text)
           if "literal" in upload.text:
              myCounter -= 1
   print("Creation finished! " + str(myCounter) + " edges created.")
   continueWork(graph, parsedToken)
   return


def deleteNodes(graph,parsedToken):
   print("You chose to delete nodes.")
   findJSON = input("Where are the NodeIDs stored? ie. /tmp/nodeIDs.json ")
   type(findJSON)
   headers = {'Content-Type': 'application/json', '_TOKEN':parsedToken}
   graphurl = "https://{0}/".format(graph)
   myCounter = 0
   #filepath = 'Iliad.txt'
   with open(findJSON) as fp:
       line = fp.readline()
       cnt = 1
       while line:
          # print("Line {}: {}".format(cnt, line.strip()))
           upload = requests.delete(graphurl + line.rstrip(), headers=headers, verify=False)
           line = fp.readline()
           cnt += 1
           myCounter += 1
           print(upload.text)
           if "literal" in upload.text:
            myCounter -= 1
   print("Delete finished! " + str(myCounter) + " nodes deleted.")
   continueWork(graph, parsedToken)
   return

def updateNodes(graph,parsedToken):
   print("You chose to update existing MARS nodes.")
   findJSON = input("What directory are the JSONs stored in? ie. /tmp/MARSBackup")
   type(findJSON)
   getJSONS = glob.glob(findJSON+'/*')
   headers = {'Content-Type': 'application/json', '_TOKEN':parsedToken}
   graphurl = "https://{0}:8443/".format(graph)
   myCounter = 0
   for x in getJSONS:
       myCounter += 1
       contents = open(x).read()
       marsID = json.loads(contents)
       marsID = marsID['ogit/_id']
       upload = requests.post(graphurl + marsID, data=contents, headers=headers, verify=False)
       print(upload.text)
   print("Upload finished! " + str(myCounter) + " MARS nodes updated.")
   continueWork(graph, parsedToken)
   return

def checkInput(str,graph,parsedToken):
     if str == "c" or str == "create":
         createNodes(graph,parsedToken)
     elif str == "createEdges":
         createEdges(graph,parsedToken)
     elif str == "u" or str == "update":
         updateNodes(graph,parsedToken)
     elif str == "d" or str == "delete":
         deleteNodes(graph,parsedToken)
     return

def findStyle(graph,parsedToken):
    style = input("Will you be creating new nodes, updating existing nodes or deleting nodes or none of the above? (c)reate (u)pdate (d)elete (n)one ")
    type(style)
    style = style.lower()
    print(style)
    if style == "c" or style == "create" or style == "u" or style == "update" or style == "d" or style == "delete":
        checkInput(style,graph,parsedToken)
    elif style =="n":
        style = input("Will you be creating new edges? (y) (n) ")
        type(style)
        style = style.lower()
        if style == "y":
            style = "createEdges"
            checkInput(style, graph, parsedToken)
        elif style =="n":
            continueWork(graph, parsedToken)
    else:
        print(r'You must enter "create" or "update" or "delete".')
        findStyle()
    return

def continueWork(graph,parsedToken):
    choice = input(
        "Would you like to perform another operation? (y) (n) ")
    type(choice)
    if choice == "y":
        findStyle(graph,parsedToken)
    else:
        print("Exiting...")
    return

findEnv()
