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
def accountverifier():
    result = boto3.client('sts').get_caller_identity().get('Account')
    if result == "713287746880":
        print(bcolors.FAIL + "You are running in a wrong account, please configure your account by running 'aws configure'"  + bcolors.ENDC)
        sys.exit(1)
