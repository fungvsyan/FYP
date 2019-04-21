import json
import boto3


def lambda_handler(event, context):
    cf_client = boto3.client('cloudformation')
    dynamodb_client = boto3.client('dynamodb')

    AssumedidList = []

    get_response = dynamodb_client.scan(
        TableName='AssumedAccount',
        AttributesToGet=[
            'account_id'
        ]
    )
    # print(get_response)
    # print(get_response['Items'][0]['account_id']['N'])
    i = get_response['Count']
    # print(i)

    for x in range(i):
        AssumedidList.append(get_response['Items'][x]['account_id']['N'])

    print(AssumedidList)

    stackSetName = 'TestUse'
    regionList = ['ap-southeast-1']

    response = cf_client.create_stack_set(
        StackSetName=stackSetName,
        Description='nothing',
        TemplateURL='https://s3.amazonaws.com/fyp-cloudformation-template/AWSCloud9Sample.yaml',

        Capabilities=[
            'CAPABILITY_IAM'
        ],
        AdministrationRoleARN='arn:aws:iam::267681339347:role/AWSCloudFormationStackSetAdministrationRole',
        ExecutionRoleName='AWSCloudFormationStackSetExecutionRole'
    )

    response = cf_client.create_stack_instances(
        StackSetName=stackSetName,
        Accounts=AssumedidList,
        Regions=regionList
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
