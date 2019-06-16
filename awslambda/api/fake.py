

from library.utils import awshandler



@awshandler
def test_api_key(event, context):
    return {'message': 'needed key'}