import json

class Connection:
    def __init__(self, *args, **kwargs):
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
        pass

    def from_dict(self, org_dict: Dict):
        self._org_dict = org_dict
        self._org = org_dict.get("Org", None)
        self._created_by = org_dict.get("CreatedBy", None)
        self._created_date = org_dict.get("CreatedDate", None)
        self._modified_date = org_dict.get("ModifiedDate", None)
        self._type = org_dict.get("Type", None)
        self._connection_info = org_dict.get("ConnectionInfo", None)
        self._name = org_dict.get("Name", None)
        self._uid = org_dict.get("UID", None)

    def from_json(self, org_json: str):
        self.from_dict(json.loads(org_json))

    def to_dict(self):
        return self._org_dict

    def to_json(self):
        return json.dumps(self._org_dict)

    