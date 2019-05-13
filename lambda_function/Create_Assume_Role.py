import json
import boto3


def lambda_handler(event, context):
    s3_client = boto3.client('s3')
    dynamodb = boto3.resource('dynamodb')

    bucket = event['Records'][0]['s3']['bucket']['name']
    json_file_name = event['Records'][0]['s3']['object']['key']
    json_object = s3_client.get_object(Bucket=bucket, Key=json_file_name)
    jsonFileReader = json_object['Body'].read()
    jsonDict = json.loads(jsonFileReader)

    table = dynamodb.Table('fyp-demo-stack-StudentKeyTable/*')
    table.put_item(Item=jsonDict)

    dynamodb_client = boto3.client('dynamodb')

    dynamodb_response = dynamodb_client.scan(
        TableName='fyp-demo-stack-StudentKeyTable/*'
    )

    totalStundent = (dynamodb_response["Count"])

    i = 0

    while i < totalStundent:
        studentAccessKey = dynamodb_response['Items'][i]['Access_key']
        studentSecretKey = dynamodb_response['Items'][i]['Secret_key']
        studentId = dynamodb_response['Items'][i]['Student_id']

        student_id = str(studentId)

        student_id_1 = student_id.strip('{\'N\': \'')
        student_id_2 = student_id_1.strip('\'}')

        access_key = str(studentAccessKey)

        access_key_1 = access_key.strip('{\'S\': \'')
        access_key_2 = access_key_1.strip('\'}')
        print(access_key_2)

        secret_key = str(studentSecretKey)

        secret_key_1 = secret_key.strip('{\'S\': \'')
        secret_key_2 = secret_key_1.strip('\'}')
        print(secret_key_2)

        print(student_id_2)

        i += 1

        cf_client = boto3.client('cloudformation',
                                 aws_access_key_id=access_key_2,
                                 aws_secret_access_key=secret_key_2,
                                 # aws_session_token = '',
                                 region_name='ap-southeast-1')

        response = cf_client.create_stack(
            StackName='AWSCloudFormationStackSetExecutionRoleStack',
            TemplateURL='https://s3-ap-southeast-1.amazonaws.com/cf-test-170245996/AWSCloudFormationStackSetExecutionRole.yml',
            DisableRollback=False,
            TimeoutInMinutes=2,
            Capabilities=[
                'CAPABILITY_NAMED_IAM'
            ]
        )

        sts_client = boto3.client('sts',
                                  aws_access_key_id=access_key_2,
                                  aws_secret_access_key=secret_key_2)

        sts_response = sts_client.get_caller_identity()
        accountId = sts_response['Account']

        response = dynamodb_client.put_item(
            TableName='fyp-demo-stack-AssumedAccountTable/*',
            Item={
                'StudentID': {
                    'N': student_id_2
                },
                'account_id': {
                    'N': accountId
                }
            }
        )

        response = dynamodb_client.delete_item(
            TableName='fyp-demo-stack-StudentKeyTable/*',
            Key={
                'StudentID': {
                    'N': student_id_2
                }
            }
        )

        print('Delete completed')

        # i += 1

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
