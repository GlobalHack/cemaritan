import json
from typing import Dict, Tuple

class User:
    def __init__(self, *args, **kwargs):
        """Class for handling Users

        Example:
        {	
            "UID": UID
            "Org": UID
            "CreatedDate": Timestamp
            "Roles": Array[string]
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

    def from_dict(self, user_dict: Dict):
        self._user_dict = user_dict
        self._uid = user_dict.get("UID", None)
        self._name = user_dict.get("Name", [])
        self._created_date = user_dict.get("CreatedDate", None)
        self._organization = user_dict.get("Organization", None)

    def from_json(self, user_json: str):
        self.from_dict(json.loads(user_json))

    def from_tuple(self, user_tuple: Tuple):
        (self._uid, self._name, self._created_date, self._org) = user_tuple

    def to_dict(self):
        return self._user_dict

    def to_json(self):
        return json.dumps(self._user_dict)
