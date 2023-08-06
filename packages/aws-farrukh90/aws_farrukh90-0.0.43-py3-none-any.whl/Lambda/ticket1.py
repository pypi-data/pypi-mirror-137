import os
import re 
import sys 
import time 
import boto3
import json 
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
def taskchecker():
    try:
        REGION="us-east-2"
        FUNCTIONNAME="HelloWorld"
        FUNCTIONPYTHON="python3.7"
        TOTALMEMORY=256
        FUNCTIONTIMEOUT=120
        client = boto3.client('lambda', region_name=REGION)
        response = client.list_functions()        

        RESULT = response["Functions"][0]
        FOUNDFUNCTIONNAME = RESULT["FunctionName"]
        FOUNDFUNCTIONPYTHON = RESULT["Runtime"]
        FOUNDFUNCTIONMEMORY = RESULT["MemorySize"]
        FOUNDFUNCTIONTIMEOUT = RESULT["Timeout"]

        if FOUNDFUNCTIONNAME in FUNCTIONNAME:
            print(bcolors.OKGREEN + "Function is created in %s " % REGION + bcolors.ENDC)
            time.sleep(0.5)
        else:
            print(bcolors.FAIL + "Function is not created %s " % REGION + bcolors.ENDC)
            sys.exit(1)
            time.sleep(0.5)


        if FOUNDFUNCTIONPYTHON == FUNCTIONPYTHON:
            print(bcolors.OKGREEN + "Function python is correct" + bcolors.ENDC)
            time.sleep(0.5)
        else:
            print(bcolors.FAIL + "Function python is not correct, it should be %s" % FUNCTIONPYTHON + bcolors.ENDC)
            sys.exit(1)
            time.sleep(0.5)

        if FOUNDFUNCTIONMEMORY == TOTALMEMORY:
            print(bcolors.OKGREEN + "Function memory is correct" + bcolors.ENDC)
            time.sleep(0.5)
        else:
            print(bcolors.FAIL + "Function memory is not correct, it should be %s, please update by Function >> Configuration >> >> General Configuration" % TOTALMEMORY + bcolors.ENDC)
            sys.exit(1)
            time.sleep(0.5)
        
        if FOUNDFUNCTIONTIMEOUT == FUNCTIONTIMEOUT:
            print(bcolors.OKGREEN + "Function timeout is correct" + bcolors.ENDC)
            time.sleep(0.5)
        else:
            print(bcolors.FAIL + "Function timeout is not correct, it should be %s, please update by Function >> Configuration >> >> General Configuration" % FUNCTIONTIMEOUT + bcolors.ENDC)
            time.sleep(0.5)
            sys.exit(1)


    except:
        print(bcolors.FAIL + "Something went wrong or you did the task in wrong region should be in %s, please redo the task" % REGION +  bcolors.ENDC)
        time.sleep(0.5)
        sys.exit(1)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
