import getpass
import json
import botocore
from botocore.vendored import requests
import sys
import urllib.parse

import boto3

def assume_role(account_id, role_name, duration):
    role_arn = "arn:aws:iam::" + str(account_id) + ":role/" + role_name
    role_session_name = "AssumeRoleSession"
    client = boto3.client('sts', 'ap-southeast-1')

    response = client.assume_role(RoleArn=role_arn,
            RoleSessionName=role_session_name,
            DurationSeconds=duration)

    tmp_credentials = {
            'sessionId': response['Credentials']['AccessKeyId'],
            'sessionKey': response['Credentials']['SecretAccessKey'],
            'sessionToken':response['Credentials']['SessionToken']
            }
    return json.dumps(tmp_credentials)

def generate_federation_request_parameters(credentials_json):
    request_parameters = "?Action=getSigninToken"
    request_parameters += "&SessionDuration=3600"
    request_parameters += "&Session=" + urllib.parse.quote_plus(credentials_json)
    return request_parameters

def generate_sign_in_token(credentials_json):
    request_parameters = generate_federation_request_parameters(credentials_json)
    request_url = "https://signin.aws.amazon.com/federation" + request_parameters
    r = requests.get(request_url)
    return json.loads(r.text)['SigninToken']

def generate_signin_request_parameters(signin_token):
    request_parameters = "?Action=login"
    #request_parameters += "&Issuer=" + issuer
    request_parameters += "&Destination=" + urllib.parse.quote_plus("https://console.aws.amazon.com/")
    request_parameters += "&SigninToken=" + signin_token
    return request_parameters

def generate_signed_url(signin_token):
    request_parameters = generate_signin_request_parameters(signin_token)
    return "https://signin.aws.amazon.com/federation" + request_parameters

def run(account_id, role_name, duration):
    tmp_credentials = assume_role(account_id, role_name, duration)
    signin_token = generate_sign_in_token(tmp_credentials)
    return generate_signed_url(signin_token)

account_id = 321170204940
role_name = "AWSCloudFormationStackSetExecutionRole"
#external_id = ""

duration = 3600 # Login link vaild time (sec)
#issuer = "Example.org" # issuer name for signin url
#external_id = getpass.getpass("External ID: ")

try:
    login_url = run(account_id, role_name, duration)
    sessionJson = assume_role(account_id, role_name, duration)
    
    print (login_url)
    #print (sessionJson)
    
except Exception as e:
    print("Received error:", e)
    sys.exit(1)
