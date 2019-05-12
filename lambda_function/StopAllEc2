import boto3

def lambda_handler(even, context):
    
    client=boto3.client('ec2')

    regionName = client.describe_regions()
    
    for region in regionName["Regions"]:
        
        client=boto3.client('ec2', region_name = region["RegionName"])
        
        response = client.describe_instances()
        
        for reservation in response["Reservations"]:
        
            for instance in reservation["Instances"]:
            
                print(region)

                print(instance["InstanceId"] + "stoping")

                id=[instance["InstanceId"]]
            
                client.stop_instances(InstanceIds=id)
            
            
    return("Completed")
