import json
from typing import Dict, Tuple


class Model:
    """Base class for all models.

    Example:
    {	
        "uid": uid
        "org": uid
        "created_datetime": Timestamp
        "Roles": Array[string]
    }

    """
    def __init__(self, data, *args, **kwargs):

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
        self._set_data()

    def _set_data(self):
        raise NotImplementedError()

    def from_dict(self, data_dict: Dict):
        try:
            return data_dict
        except Exception as e:
            print("Parameter 'data_dict' is not a valid dict: " + e)

    def from_json(self, data_json: str):
        try:
            return self.from_dict(json.loads(data_json))
        except Exception as e:
            print("Parameter 'data_json' is not a valid JSON string: " + e)

    def from_tuple(self, data_tuple: Tuple):
        try:
            return {x[0]: x[1] for x in data_tuple}
        except Exception as e:
            print("Parameter 'data_tuple' is not valid: " + e)

    def to_dict(self):
        return self.data

    def to_json(self):
        return json.dumps(self.data)


class Upload(Model):
    
    def __init__(self, data, *args, **kwargs):
        super(Upload, self).__init__(data, *args, **kwargs)

    def _set_data(self):
        self._organization = self.data.get("organization")
        self._transfer = self.data.get("transfer")
