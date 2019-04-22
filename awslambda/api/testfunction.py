import os
import json

def test(event, context):
    try:
        value = os.getenv('TEST_ENV_VAR')
        if value == '' or value is None:
            value = 'here'
    except Exception as e:
        # TODO: Rethink what to return...dumping exceptions is scary for data leakage
        return {"statusCode": 400, "body": "400 Bad Request\n\n" + json.dumps(str(e))}
    return {"statusCode": 200, "body": value}



def test2(event, context):
    vals = {}
    try:
        vals['DB_HOST'] = os.getenv('DB_HOST')
        vals['PORT'] = os.getenv('PORT')
        vals['DB_NAME'] = os.getenv('DB_NAME')
        vals['USER'] = os.getenv('USER')
        vals['PASSWORD'] = os.getenv('PASSWORD')
    except Exception as e:
        # TODO: Rethink what to return...dumping exceptions is scary for data leakage
        return {"statusCode": 400, "body": "400 Bad Request\n\n" + json.dumps(str(e))}
    return {"statusCode": 200, "body": json.dumps(vals)}