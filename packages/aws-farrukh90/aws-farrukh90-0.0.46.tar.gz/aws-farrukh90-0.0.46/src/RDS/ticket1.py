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
def taskchecker():
    REGION="us-east-1"
    DBNAME="django"
    try:
        client = boto3.client('rds', region_name=REGION)
        response = client.describe_db_instances(
            DBInstanceIdentifier=DBNAME
            )
        time.sleep(0.5)
        print(bcolors.OKGREEN + "RDS is created %s " % REGION + bcolors.ENDC)
    except Exception as e:
        print(bcolors.FAIL + "RDS is not created %s " % REGION + bcolors.ENDC)
        sys.exit(1)
        time.sleep(0.5)