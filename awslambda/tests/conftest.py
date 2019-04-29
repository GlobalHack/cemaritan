import json
import pytest
from pathlib import Path


# try:
#     os.unlink('/Users/kylesykes/repos/cemaritan/awslambda/api/models')
# except:
#     os.symlink('/Users/kylesykes/repos/cemaritan/awslambda/models', '/Users/kylesykes/repos/cemaritan/awslambda/api/models')


@pytest.fixture()
def connections_event():
    return {
        "resource": "/organizations/{organization_id}/transfers",
        "path": "/organizations/1/transfers",
        "httpMethod": "GET",
        "headers": {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "cache-control": "no-cache",
            "CloudFront-Forwarded-Proto": "https",
            "CloudFront-Is-Desktop-Viewer": "True",
            "CloudFront-Is-Mobile-Viewer": "False",
            "CloudFront-Is-SmartTV-Viewer": "False",
            "CloudFront-Is-Tablet-Viewer": "False",
            "CloudFront-Viewer-Country": "US",
            "Host": "6u7n9sc5o8.execute-api.us-east-1.amazonaws.com",
            "Postman-Token": "3e049cd5-7375-4f1c-bc10-4b00d5f6e113",
            "User-Agent": "PostmanRuntime/7.6.1",
            "Via": "1.1 e8ff6e511452028b739414de422b3bb8.cloudfront.net (CloudFront)",
            "X-Amz-Cf-Id": "BZouIkKvh0poMWgFTcoBE9atSG739R1_JcIzjACJ5ENReM3_N1YhDQ==",
            "X-Amzn-Trace-Id": "Root=1-5cbeb18e-cbcefbf0909eb5f86934728c",
            "X-Forwarded-For": "24.107.13.69, 54.182.238.53",
            "X-Forwarded-Port": "443",
            "X-Forwarded-Proto": "https",
        },
        "multiValueHeaders": {
            "Accept": ["*/*"],
            "Accept-Encoding": ["gzip, deflate"],
            "cache-control": ["no-cache"],
            "CloudFront-Forwarded-Proto": ["https"],
            "CloudFront-Is-Desktop-Viewer": ["True"],
            "CloudFront-Is-Mobile-Viewer": ["False"],
            "CloudFront-Is-SmartTV-Viewer": ["False"],
            "CloudFront-Is-Tablet-Viewer": ["False"],
            "CloudFront-Viewer-Country": ["US"],
            "Host": ["6u7n9sc5o8.execute-api.us-east-1.amazonaws.com"],
            "Postman-Token": ["3e049cd5-7375-4f1c-bc10-4b00d5f6e113"],
            "User-Agent": ["PostmanRuntime/7.6.1"],
            "Via": ["1.1 e8ff6e511452028b739414de422b3bb8.cloudfront.net (CloudFront)"],
            "X-Amz-Cf-Id": ["BZouIkKvh0poMWgFTcoBE9atSG739R1_JcIzjACJ5ENReM3_N1YhDQ=="],
            "X-Amzn-Trace-Id": ["Root=1-5cbeb18e-cbcefbf0909eb5f86934728c"],
            "X-Forwarded-For": ["24.107.13.69, 54.182.238.53"],
            "X-Forwarded-Port": ["443"],
            "X-Forwarded-Proto": ["https"],
        },
        "queryStringParameters": None,
        "multiValueQueryStringParameters": None,
        "pathParameters": {"organization_id": "1"},
        "stageVariables": None,
        "requestContext": {
            "resourceId": "4u7wey",
            "resourcePath": "/organizations/{organization_id}/transfers",
            "httpMethod": "GET",
            "extendedRequestId": "YlCuVF33oAMFsaQ=",
            "requestTime": "23/Apr/2019:06:32:46 +0000",
            "path": "/dev/organizations/1/transfers",
            "accountId": "471110211490",
            "protocol": "HTTP/1.1",
            "stage": "dev",
            "domainPrefix": "6u7n9sc5o8",
            "requestTimeEpoch": 1556001166936,
            "requestId": "9bc20da4-6591-11e9-9ce4-11bd9f5c1f10",
            "identity": {
                "cognitoIdentityPoolId": None,
                "accountId": None,
                "cognitoIdentityId": None,
                "caller": None,
                "sourceIp": "24.107.13.69",
                "accessKey": None,
                "cognitoAuthenticationType": None,
                "cognitoAuthenticationProvider": None,
                "userArn": None,
                "userAgent": "PostmanRuntime/7.6.1",
                "user": None,
            },
            "domainName": "6u7n9sc5o8.execute-api.us-east-1.amazonaws.com",
            "apiId": "6u7n9sc5o8",
        },
        "body": None,
        "isBase64Encoded": False,
    }


@pytest.fixture()
def sample_connection_response():
    return {
        "statusCode": 200,
        "headers": {"Access-Control-Allow-Origin": "*"},
        "body": '[{"uid": 1, "organization": 1, "name": "SF", "createddate": "2019-03-09 20:42:03", "createdby": 1, "type": "A", "connectioninfo": "{conn string}"}, {"uid": 2, "organization": 1, "name": "CW", "createddate": "2019-03-10 04:42:03", "createdby": 1, "type": "B", "connectioninfo": "{conn string}"}, {"uid": 6, "organization": 1, "name": "Secure Download", "createddate": "2019-03-23 20:42:03", "createdby": 0, "type": "F", "connectioninfo": "0"}]',
    }
