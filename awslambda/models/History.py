import json
from typing import Dict, Tuple


class History:
    def __init__(self, data, *args, **kwargs):
        """Class for handling History
        
        Example:
            {
                "Type":	string,
                "Action": string,
                "Date": string,
                "CreatedByUser": string,
                "Name": string,
                "UID": int,
                "Details": string,
                "SourceUID": int,
                "Organization": int
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

        self._type = self.data.get("Type", None)
        self._uid = self.data.get("UID", None)
        self._action = self.data.get("Action", None)
        self._name = self.data.get("Name", None)
        self._date = self.data.get("Date", [])
        self._created_by_user = self.data.get("CreatedByUser", None)
        self._details = self.data.get("Details", None)
        self._source_uid = self.data.get("SourceUID", None)
        self._organization = self.data.get("Organization", None)

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
