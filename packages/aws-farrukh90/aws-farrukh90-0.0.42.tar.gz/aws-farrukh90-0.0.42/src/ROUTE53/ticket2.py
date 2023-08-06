import os 
import sys 
import time 
import boto3

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
    client = boto3.client('route53')
    fulllist = client.list_hosted_zones()
    HZONELIST = (fulllist["HostedZones"])

    # Creates a variable for Hosted Zone ID
    for i in HZONELIST:
        RAWHZONEID = i["Id"]
        HZONEID = RAWHZONEID.split("/")[2]

    for i in HZONELIST:
        HNAME = i["Name"]



    response = client.list_resource_record_sets(
        HostedZoneId=HZONEID
    )


    RR = response["ResourceRecordSets"]
    for i in RR:
        NAMETUPLE    = i["Name"], 
        TYPELIST    = i["Type"]
        NAMELIST    = ''.join(NAMETUPLE)
    if "1sdf" in NAMELIST:
        print(HNAME)
        print(bcolors.OKGREEN + "CNAME is created"+ bcolors.ENDC)
    else:
        print(bcolors.OKGREEN + "CNAME is created"+ bcolors.ENDC)

taskchecker()
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
