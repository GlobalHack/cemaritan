import json
from typing import Dict, Tuple

class Connection:
    def __init__(self, data, *args, **kwargs):
        """Class for handling Connections

        Example:
        {
            "Org": UID,
            "CreatedBy": UID,
            "CreatedDate": Timestamp,
            "ModifiedDate": Timestamp,
            "Type": string (Salesforce, CW..),
            "ConnectionInfo": {"connectionstring": ..},
            "Name": string,
            "UID": UID,
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

    def from_dict(self, conn_dict: Dict):
        try:
            self._conn_dict = conn_dict
            self._uid = conn_dict.get("UID", None)
            self._organization = conn_dict.get("Organization", None)
            self._name = conn_dict.get("Name", None)
            self._created_date = conn_dict.get("CreatedDate", None)
            self._created_by = conn_dict.get("CreatedBy", None)
            self._type = conn_dict.get("Type", None)
            self._connection_info = conn_dict.get("ConnectionInfo", None)
        except Exception as e:
            print("Parameter 'conn_dict' is not a valid dict: " + e)

    def from_json(self, conn_json: str):
        try:
            self.from_dict(json.loads(conn_json))
        except Exception as e:
            print("Parameter 'conn_json' is not a valid JSON string: " + e)

    def from_tuple(self, conn_tuple: Tuple):
        (
            self._conn_dict,
            self._uid,
            self._organization,
            self._name,
            self._created_date,
            self._created_by,
            self._type,
            self._connection_info,
        ) = conn_tuple

    def to_dict(self):
        return self._conn_dict

    def to_json(self):
        return json.dumps(self._conn_dict)

