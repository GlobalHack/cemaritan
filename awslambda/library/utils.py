
import functools
import json


def awshandler(function):
    """A decorator to wrap AWS Lambda function hanlder in a
    try-catch that ensure returning a proper error.
    """
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        try:
            payload = function(*args, **kwargs)
        except Exception as e:
            # TODO: Rethink what to return...dumping exceptions is scary for data leakage
            return {"statusCode": 400, "headers": {"Access-Control-Allow-Origin": "*"},  "body": "400 Bad Request\n\n" + json.dumps(str(e))}
        return {"statusCode": 200, "headers": {"Access-Control-Allow-Origin": "*"},  "body": payload}
    return wrapper
        
