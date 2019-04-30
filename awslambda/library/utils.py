
import functools
import json

from library.exceptions import DatabaseReturnedNone

def awshandler(function):
    """A decorator to wrap AWS Lambda function hanlder in a
    try-catch that ensure returning a proper error.
    """
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        try:
            payload = function(*args, **kwargs)
        except DatabaseReturnedNone as e:
            return {"statusCode": 400, "headers": {"Access-Control-Allow-Origin": "*"},  "body": json.dumps({'message': str(e)})}
        except Exception as e:
            # TODO: Rethink what to return...dumping exceptions is scary for data leakage
            return {"statusCode": 400, "headers": {"Access-Control-Allow-Origin": "*"},  "body": "400 Bad Request\n\n" + json.dumps(str(e))}
        return {"statusCode": 200, "headers": {"Access-Control-Allow-Origin": "*"},  "body": json.dumps(payload)}
    return wrapper
        

def aws_get_http_method(event):
    """Return the http method from the AWS Lambda event object."""
    return event['requestContext']['httpMethod']


def aws_get_path_parameters(event):
    """Extract path parameters from AWS Lambda event object."""
    return event['pathParameters']


def aws_get_path_parameter(event, parameter):
    """Extract specific path parameter from AWS Lambda event object."""
    return aws_get_path_parameters(event)[parameter]