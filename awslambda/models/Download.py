import json
from typing import Dict, Tuple


class Download:
    def __init__(self, data, *args, **kwargs):
        """Class for handling Download objects
        
        Example:
            {
                "Name": str,
                "TransferName": str,
                "uid": int,
                "HistoryUID": int,
                "ExpirationDateTime": str,
                "Organization": int,
                "file_location_info": str
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

        self._name = self.data.get("Name", None)
        self._transfer_name = self.data.get("TransferName", None)
        self._uid = self.data.get("uid", None)
        self._history_uid = self.data.get("HistoryUID", None)
        self._expiration_date_time = self.data.get("ExpirationDateTime", None)
        self._organization = self.data.get("organization", None)
        self._file_location_info = self.data.get("file_location_info", None)

    def from_dict(self, dm_dict: Dict):
        try:
            return dm_dict
        except Exception as e:
            print("Parameter 'dm_dict' is not a valid dict: " + e)

    def from_json(self, dm_json):
        try:
            return self.from_dict(json.loads(dm_json))
        except Exception as e:
            print("Parameter 'dm_json' is not a valid JSON string: " + e)

    def from_tuple(self, dm_tuple: Tuple):
        try:
            return {x[0]: x[1] for x in dm_tuple}
        except Exception as e:
            print("Parameter 'dm_tuple' is not valid: " + e)

    def to_dict(self):
        return self.data

    def to_json(self):
        return json.dumps(self.data)
