import json
from typing import Dict, Tuple


class Organization:
    def __init__(self, data, *args, **kwargs):
        """ Class for handling Organizations

        Example:
        {
            UID	
            CreatedDate	Timestamp
            Connections	Array[Connection]
            Transfers	Array[Transfer]
            Transfer History	Array[]
            Download History	Array[]
            Upload History	Array[]
        }
        """
        if isinstance(data, dict):
            self.data = self.from_dict(data)
        elif isinstance(data, str):
            self.data = self.from_json(data)
        elif isinstance(data, tuple):
            self.data = self.from_tuple(data)
        else:
            raise AssertionError(
                "Parameter 'data' was not a valid input: dict, tuple, or JSON string"
            )

        self._uid = self.data.get("UID", None)
        self._name = self.data.get("Name", None)
        self._created_date = self.data.get("CreatedDate", None)
        # might want these later
        # self._connections = self.data.get("Connections", None)
        # self._transfers = self.data.get("Transfers", None)
        # self._transfer_history = self.data.get("TransferHistory", None)
        # self._download_history = self.data.get("DownloadHistory", None)
        # self._upload_history = self.data.get("UploadHistory", None)

    def from_dict(self, org_dict: Dict):
        try:
            return org_dict
        except Exception as e:
            print("Parameter 'org_dict' is not a valid dict: " + e)

    def from_json(self, org_json: str):
        try:
            return self.from_dict(json.loads(org_json))
        except Exception as e:
            print("Parameter 'org_json' is not a valid JSON string: " + e)

    def from_tuple(self, org_tuple: Tuple):
        try:
            return {x[0]: x[1] for x in org_tuple}
        except Exception as e:
            print("Parameter 'org_tuple' is not valid: " + e)

    def to_dict(self):
        return self._org_dict

    def to_json(self):
        return json.dumps(self._org_dict)
