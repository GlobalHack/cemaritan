import json


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
        pass

    def from_dict(self, user_dict: Dict):
        self._user_dict = user_dict
        self._org = user_dict.get("Org", None)
        self._uid = user_dict.get("UID", None)
        self._created_by = user_dict.get("CreatedBy", None)
        self._roles = user_dict.get("Roles", [])

    def from_json(self, user_json: str):
        self.from_dict(json.loads(user_json))

    def to_dict(self):
        return self._user_dict

    def to_json(self):
        return json.dumps(self._user_dict)
