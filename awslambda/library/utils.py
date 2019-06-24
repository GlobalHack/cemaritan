import datetime
import functools
import json

from library.exceptions import DatabaseReturnedNone

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def format_exception(e):
    """Format an exception to be returned in a function response."""
    return str(type(e)) + ' ' + str(e)


def awshandler(function):
    """A decorator to wrap AWS Lambda function hanlder in a
    try-catch that ensure returning a proper error.
    """
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        try:
            payload = function(*args, **kwargs)
        except DatabaseReturnedNone as e:
            return {"statusCode": 400, "headers": {"Access-Control-Allow-Origin": "*"},  "body": json.dumps({'message': format_exception(e)})}
        except Exception as e:
            # TODO: Rethink what to return...dumping exceptions is scary for data leakage
            logger.exception(e)
            return {"statusCode": 400, "headers": {"Access-Control-Allow-Origin": "*"},  "body": json.dumps({'message': "400 Bad Request\n\n" + format_exception(e)})} 
        # No errors, so convert payload to JSON and return http response.
        return {"statusCode": 200, "headers": {"Access-Control-Allow-Origin": "*"},  "body": json.dumps(payload)}
    return wrapper
        

def de_handler(response):
    """Undoes the effects of @awshandler so those functions can be used internally."""
    return json.loads(response['body'])


def aws_get_http_method(event):
    """Return the http method from the AWS Lambda event object."""
    return event['requestContext']['httpMethod']


def aws_get_path_parameters(event):
    """Extract path parameters from AWS Lambda event object."""
    return event['pathParameters']


def aws_get_path_parameter(event, parameter):
    """Extract specific path parameter from AWS Lambda event object."""
    return aws_get_path_parameters(event)[parameter]


def get_future_datetime(days):
    return datetime.datetime.now() + datetime.timedelta(days=days)


def format_dt(dt):
    return dt.strftime('%Y-%m-%d %H:%M:%S')


def get_future_datetime_formatted(days):
    return format_dt(get_future_datetime(days))

def get_now_datetime_formatted():
    return format_dt(datetime.datetime.now())