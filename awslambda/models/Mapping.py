import json
from typing import Dict, Tuple


class Mapping:
    def __init__(self, data, *args, **kwargs):
        """Class for handling Mapping
        
        Example:
            {
                "Name":	string,
                "uid": string,
                "MappingInfo": []
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

        self._uid = self.data.get("uid", None)
        self._organization = self.data.get("organization", None)
        self._name = self.data.get("Name", None)
        self._mapping = self.data.get("MappingInfo", [])
        self._created_date = self.data.get("created_datetime", None)
        self._created_by = self.data.get("created_by", None)

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
