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


### Connections ###

class Connection:

    def __init__(self, mapping):
        self.mapping = mapping

    def get_data(self):
        raise NotImplementedError()

    def convert(self):
        raise NotImplementedError()

    def send_data(self):
        raise NotImplementedError()
    

class Upload(Connection):
    """Can be a source, but not a destination.
    """
    def __init__(self, mapping, location: str):
        super().__init__(self, mapping=mapping)
        self.location = location
    
    def get_data(self):
        s3_client = boto3.client('s3')


class Download(Connection):
    """Can be a destination, but not a source.
    """
    def __init__(self, mapping, location: str):
        super().__init__(self, mapping=mapping)
        self.location = location

    def get_data(self):
        pass

    def convert(self):
        if mapping is not None:
            # Convert
            pass

    def put_data(self):
        s3_client = boto3.client('s3')
        s3.Object('cemaritan-dev-test', f'test_{rand_int}.txt').put(Body='test body')


class Salesforce(Connection):
    """Can be both a source and a destination.
    """
    def __init__(self, mapping=mapping):
        super().__init__(self, mapping=mapping)
        