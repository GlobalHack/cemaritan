from typing import Dict, List
import json


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
        pass

    def from_dict(self, dm_dict):
        self._dm_dict = dm_dict
        self._name = dm_dict.get("Name", None)
        self._uid = dm_dict.get("UID", None)
        self._mapping = dm_dict.get("MappingInfo", [])

    def from_json(self, dm_json):
        self.from_dict(json.loads(dm_json))

    def to_dict(self):
        return self._dm_dict

    def to_json(self):
        return json.dumps(self._dm_dict)
