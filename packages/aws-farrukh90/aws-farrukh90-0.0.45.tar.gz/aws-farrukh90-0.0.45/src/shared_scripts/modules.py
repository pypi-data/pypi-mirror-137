import boto3
def zone_id_finder():
    client = boto3.client('route53')
    fulllist = client.list_hosted_zones()
    HZONELIST = (fulllist["HostedZones"])

    # Creates a variable for Hosted Zone ID
    for i in HZONELIST:
        RAWHZONEID = i["Id"]
        HZONEID = RAWHZONEID.split("/")[2]
        return HZONEID
