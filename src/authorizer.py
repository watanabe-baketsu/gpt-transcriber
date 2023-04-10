import base64
import json
import os

import boto3


client = boto3.client(region_name="ap-northeast-1", service_name="secretsmanager")
# Basic Authentication Secretの取得
auth_secret = client.get_secret_value(SecretId=os.environ['AUTHORIZER'])
auth_config = json.loads(auth_secret["SecretString"])

def lambda_handler(event, context):
    auth_str = 'Basic ' + base64.b64encode(f"{auth_config['user']}:{auth_config['pass']}".encode("utf-8")).decode("ascii")
    auth_header = event['headers']['Authorization']

    if auth_str != auth_header:
        raise Exception('Unauthorized')

    return {
        'principalId': auth_config['user'],
        'policyDocument': {
            'Version': '2012-10-17',
            'Statement': [
                {
                    'Action': 'execute-api:Invoke',
                    'Effect': 'Allow',
                    'Resource': 'arn:aws:execute-api:ap-northeast-1:053566855280:76z6mcx4jh/*'
                }
            ]
        }
    }
