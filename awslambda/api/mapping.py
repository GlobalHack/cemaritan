import requests
import json

# from library.connection import Postgres
# from library.database import *

# define DB connection here


def mappings(event, context):
    try:
        s = event["body"]

        # replace mapping_list here with actual database function call
        mapping_list = [
            {"UID": 1, "Organization": 1, "Name": "SF to HUD", "StartFormat": "csv", "EndFormat": "json", "NumOfTransfers": 1, "MappingInfo": "{}"},
            {"UID": 2, "Organization": 1, "Name": "CW to HUD", "StartFormat": "csv", "EndFormat": "json", "NumOfTransfers": 1, "MappingInfo": "{}"},
            {
                "UID": 6,
                "Organization": 1,
                "Name": "new_mapping",
                "StartFormat": "csv", "EndFormat": "json", "NumOfTransfers": 1, 
                "MappingInfo": "blahdiblah",
            },
        ]
        payload = json.dumps(mapping_list)

    except Exception as e:
        # TODO: Rethink what to return...dumping exceptions is scary for data leakage
        return {"statusCode": 400, "body": "400 Bad Request\n\n" + json.dumps(str(e))}
    return {"statusCode": 200, "body": payload}
