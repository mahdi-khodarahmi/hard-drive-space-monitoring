#!/usr/bin/python
# -*- coding: utf-8 -*-

#Written By Mahdi Khodarahmi
#Release Date:1400/05/20

import subprocess as sp
import time
import requests
import json
import datetime
import sys
import shutil

Drive = "D:"
#set free driver (GB):
FreeDrive=17
serverName="سرور ديتابيس"


now = datetime.datetime.now()
hour = now.hour
if hour < 12:
    greeting = "صبح بخير"
elif hour < 19:
    greeting = "عصر بخير"
else:
    greeting = "شب بخير"

timeNow=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
global i
i =0

def prettyJSON(response):
    b=json.loads(response.text)
    print(json.dumps(b, indent = 1, ensure_ascii=False))

def getToken():
        
    tokenUrl = "https://Restful.......com/api/Token"
    tokenPayload ={
            "UserApiKey":"5db8b......636b94c",
            "SecretKey":"key........"
    }
    tokenHeaders = {
      'Content-Type': 'application/json'
    }
    
    try:
        tokenResponse = requests.request("POST", tokenUrl, headers=tokenHeaders, data = json.dumps(tokenPayload))
        return tokenResponse
    except:
        print("Maybe the internet is disconnect!. can't get Token")
        i=0
        
newToken=getToken()
def getSMS():
    time.sleep(2)
    tokenResponse=newToken
    token=tokenResponse.json()['TokenKey']
    #print(token)
    try :   
        if tokenResponse.json()['IsSuccessful'] == True:
            url = "https://restful......com/api/ReceiveMessage?Shamsi_FromDate=1400/04/31&Shamsi_ToDate=1410/04/31&RowsPerPage=5&RequestedPageNumber=1"
            headers = {
              'x-sms-ir-secure-token': token,
              'Content-Type': 'application/json'
            }
            response = requests.request("GET", url, headers=headers)
            if response.json()['IsSuccessful'] == True:
                return response
            else:
                print("get sms problem!")            
    except:
        print("Maybe the internet is disconnect!. can't get send SMS")           



def sendSMS(myMessages):
    
    tokenUrl = "https://Restful.........com/api/Token"
    tokenPayload ={
            "UserApiKey":"5db.........b94c",
            "SecretKey":"key .........."
    }
    tokenHeaders = {
      'Content-Type': 'application/json'
    }
    try :
        tokenResponse = requests.request("POST", tokenUrl, headers=tokenHeaders, data = json.dumps(tokenPayload))
        token=tokenResponse.json()['TokenKey']
    except:
        print("Maybe the internet is disconnect!. can't get Token(sendSMS)")
    try :
        if tokenResponse.json()['IsSuccessful'] == True:
            url = "https://Restful..........com/api/MessageSend"
            payload = {
                    "Messages":[myMessages],
                    "MobileNumbers": ["09....."],
                    "LineNumber": "3000......",
                    "SendDateTime": "",
                    "CanContinueInCaseOfError": "false",     
            }
            headers = {
              'x-sms-ir-secure-token': token,
              'Content-Type': 'application/json'
            }
            
            response = requests.request("POST", url, headers=headers, data = json.dumps(payload))                        
            if response.json()['IsSuccessful'] == True:
                return response           
            else:
                print("send sms problem!")
    except:
        print("Maybe the internet is disconnect!. can't send SMS")



print ("++++ HDD Space Monitor Application Started ++++")
getSMSresponse=getSMS()        
msgID=getSMSresponse.json()['Messages'][0]["ID"]


def listenComingNewCode():
        getSMSresponse=getSMS()
        time.sleep(2)
        msgBody=getSMSresponse.json()['Messages'][0]["SMSMessageBody"]
        time.sleep(2)
        msgIDNew=getSMSresponse.json()['Messages'][0]["ID"]
        global msgID
        if msgID != msgIDNew:
            print("++++++++++New Code Detected from SMS... +++++++++++")
            statusNumber=getSMSresponse.json()['Messages'][0]["SMSMessageBody"]
            msgID=msgIDNew
            if statusNumber == 'hdd-off':
                print ("SMS received --> hdd-off code.")
                sendSMS("کد خاموش کردن برنامه مانیتور فضای هارد دريافت شد.")
                time.sleep(3)
                sys.exit()
            

total, used, free = shutil.disk_usage(Drive)
free=free // (2**30)

while free > FreeDrive:
    
    total, used, free = shutil.disk_usage(Drive)
    free=free // (2**30)
    used=used // (2**30)
    #print("Total: %d GiB" % (total // (2**30)))
    #print("Used: %d GiB" % (used // (2**30)))
    print("Drive-"+Drive+"--->Free: %d GiB" % free +"   (Time:"+timeNow+")")
    listenComingNewCode()
    
    time.sleep(5)
    i+= 3
    if i>7:
        newToken=getToken()
        i=0
        
    if free <= FreeDrive :
        myMessages=(greeting+"\nظرفيت درايو پر شده است - "+serverName+"\nمقدار فضاي آزاد کنوني:"+str(free)+"گيگابايت"+"\nمقدار فضاي استفاده شده:"+str(used)+"گيگابايت"+"\ntime:"+timeNow)
        sendSMS(myMessages)
        print ("■■■■■■ Drive is full ! ■■■■■■")
        print ("SMS sent.")
        break;


    
