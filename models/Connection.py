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

        self._uid = self.data.get("UID", None)
        self._organization = self.data.get("Organization", None)
        self._name = self.data.get("Name", None)
        self._created_date = self.data.get("CreatedDate", None)
        self._created_by = self.data.get("CreatedBy", None)
        self._type = self.data.get("Type", None)
        self._connection_info = self.data.get("ConnectionInfo", None)

    def from_dict(self, conn_dict: Dict):
        try:
            return conn_dict

        except Exception as e:
            print("Parameter 'conn_dict' is not a valid dict: " + e)

    def from_json(self, conn_json: str):
        try:
            return self.from_dict(json.loads(conn_json))
        except Exception as e:
            print("Parameter 'conn_json' is not a valid JSON string: " + e)

    def from_tuple(self, conn_tuple: Tuple):
        try:
            return {
                "UID": conn_tuple[0],
                "Organization": conn_tuple[1],
                "Name": conn_tuple[2],
                "CreatedDate": conn_tuple[3],
                "CreatedBy": conn_tuple[4],
                "Type": conn_tuple[5],
                "ConnectionInfo": conn_tuple[6],
            }
        except Exception as e:
            print("Parameter 'conn_tuple' is not valid: " + e)

    def to_dict(self):
        return self.data

    def to_json(self):
        return json.dumps(self.data)
