import json

import boto3

from library.utils import awshandler
from library.db_connections import Postgres
from library.db_queries import get_transfers


conn = Postgres()


@awshandler
def get_transfers_for_org(event, context):
    # body = json.loads(event['body'])
    # organization_id = body['organization_id']
    # transfers = get_transfers(conn, organization_id)
    transfers = get_transfers(conn, 1)
    lambda_client = boto3.client('lambda')
    for t in transfers:
        msg = {"transfer": t.to_dict()}
        lambda_client.invoke(FunctionName='aws-cemaritan-dataexchange-dev-do_transfer',
                             InvocationType='Event',
                             Payload=json.dumps(msg))
    return {"Number of transfers": len(transfers)}





def do_transfer(event, context):
    print(event)
    
