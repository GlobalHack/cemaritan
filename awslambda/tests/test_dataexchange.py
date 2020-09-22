import json

# from unittest.mock import Mock, patch

import pytest


from dataexchange.upload import do_upload, do_transfer

import logging

for name in logging.Logger.manager.loggerDict.keys():
    if ('boto' in name) or ('urllib3' in name) or ('s3transfer' in name) or ('boto3' in name) or ('botocore' in name) or ('nose' in name):
        logging.getLogger(name).setLevel(logging.CRITICAL)



# def test_do_upload_function(sample_do_upload_event):
#     do_upload(sample_do_upload_event, None)


def test_do_transfer_function(sample_do_transfer_event):
    do_transfer(sample_do_transfer_event, None)


# # @patch('dataexchange.salesforce_api.requests.post')
# def test_do_upload_function(mock_get, sample_do_upload_event):
# #     mock_get.return_value.ok = True
# #     mock_get.return_value.json.return_value = {'id': 1}

#     do_upload(sample_do_upload_event, None)
# #     print(f'mock called {mock_get.call_count}')


