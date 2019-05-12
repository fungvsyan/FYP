import boto3
import json

def lambda_handler(event, context):
    
    ec2_client = boto3.client('ec2')
    
    regionName = ec2_client.describe_regions()
    
    notInUseIPsList = []
    
    for region in regionName["Regions"]:
        
        ec2_client=boto3.client('ec2', region_name = region["RegionName"])
        addresses_dict = ec2_client.describe_addresses()
        
        #print(regionName['Regions'][i]['RegionName'])
        
        for eip_dict in addresses_dict['Addresses']:
            if "NetworkInterfaceId" not in eip_dict:
                # print(eip_dict['PublicIp'])
                ec2_client.release_address(AllocationId=eip_dict['AllocationId'])
    
    return {
        'statusCode': 200,
        'body': json.dumps('Released!')
    }
