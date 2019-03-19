import json
from typing import Dict, Tuple


class DataMapping:
    def __init__(self, *args, **kwargs):
        """Class for handling DataMapping
        
        Example:
            {
                "Name":	string,
                "UID": string,
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

    def from_dict(self, dm_dict: Dict):
        self._dm_dict = dm_dict
        self._uid = dm_dict.get("UID", None)
        self._organization = dm_dict.get("Organization", None)
        self._name = dm_dict.get("Name", None)
        self._mapping = dm_dict.get("MappingInfo", [])
        self._created_date = dm_dict.get("CreatedDate", None)
        self._created_by = dm_dict.get("CreatedBy", None)

    def from_json(self, dm_json):
        self.from_dict(json.loads(dm_json))

    def from_tuple(self, dm_tuple: Tuple):
        (
            self._uid,
            self._organization,
            self._name,
            self._mapping,
            self._created_date,
            self._created_by,
        ) = dm_tuple

    def to_dict(self):
        return self._dm_dict

    def to_json(self):
        return json.dumps(self._dm_dict)
