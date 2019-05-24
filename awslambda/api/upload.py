import library.db_queries as db_queries

from library.exceptions import DatabaseReturnedNone
from library.db_connections import Postgres, get_conn
from library.utils import awshandler, aws_get_path_parameter

from models.Models import Upload

conn = Postgres()

@awshandler
def create_upload(event, context):
    organization_id = aws_get_path_parameter(event, "organization_id")
    # body = json.loads(event['body'])
    # The better way to do this might be to send back a signed URL 
    # to the client and have them upload to S3. 
    # Then have the client make another post to kick off the conversion process.
    return {'message': 'File uploaded'}