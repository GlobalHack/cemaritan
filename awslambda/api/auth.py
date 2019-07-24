import os
import json

import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth


def init_app():
    cred_json = json.loads(os.environ['AUTH_CRED'])
    cred_json['private_key'] = cred_json['private_key'].replace('\\n', '\n')
    try:
        cred = credentials.Certificate(cred_json)
        firebase_admin.initialize_app(cred)
    except Exception as e:
        print('init err')
        print(e)


def generatePolicy(principalId, effect, methodArn):
    authResponse = {}
    authResponse['principalId'] = principalId
 
    if effect and methodArn:
        policyDocument = {
            'Version': '2012-10-17',
            'Statement': [
                {
                    'Sid': 'FirstStatement',
                    'Action': 'execute-api:Invoke',
                    'Effect': effect,
                    'Resource': methodArn
                }
            ]
        }
 
        authResponse['policyDocument'] = policyDocument
 
    return authResponse


def authorizer_user(event, context):
    """event:
    {
        "authorizationToken": <token>,
        "methodArn": <methodArn>,
        "type": "TOKEN"
        }   
    """
    id_token = event['authorizationToken']
    try:
        decoded_token = auth.verify_id_token(id_token)
    except ValueError as err:
        # Deny access if the token is invalid
        print(err)
        return generatePolicy(None, 'Deny', event['methodArn'])
        # raise Exception('Unauthorized')
    # Auth succeeded so get the principalID
    principalId = decoded_token['uid']
    return generatePolicy(principalId, 'Allow', '*')


init_app()