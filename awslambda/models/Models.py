import json
from typing import Dict, Tuple

### Base Model class

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

    def verify(self):
        """Verify that all properites are non-None."""
        return all(v is not None for v in self.__dict__.values())

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


### Concrete classes

class Upload(Model):
    
    def __init__(self, data, *args, **kwargs):
        super(Upload, self).__init__(data, *args, **kwargs)

    def _set_data(self):
        self._organization = self.data.get("organization")
        self._transfer = self.data.get("transfer")


class Frequency(Model):
    
    def __init__(self, data, *args, **kwargs):
        super(Frequency, self).__init__(data, *args, **kwargs)
    
    def _set_data(self):
        self._uid = self.data.get("uid")
        self._name = self.data.get("name")
        self._value = self.data.get("value")


class Connection(Model):
    
    def __init__(self, data, *args, **kwargs):
        super(Connection, self).__init__(data, *args, **kwargs)
    
    def _set_data(self):    
        self._uid = self.data.get("uid")
        self._organization = self.data.get("organization")
        self._name = self.data.get("name")
        self._created_date = self.data.get("created_datetime")
        self._created_by = self.data.get("created_by")
        self._type = self.data.get("type")
        self._connection_info = self.data.get("connection_info")


class Download(Model):
    
    def __init__(self, data, *args, **kwargs):
        super(Download, self).__init__(data, *args, **kwargs)
    
    def _set_data(self): 
        self._name = self.data.get("name")
        self._transfer_name = self.data.get("transfer_name")
        self._uid = self.data.get("uid")
        self._history_uid = self.data.get("history_uid")
        self._expiration_date_time = self.data.get("expiration_datetime")
        self._organization = self.data.get("organization")
        self._file_location_info = self.data.get("file_location_info")


class History(Model):
    
    def __init__(self, data, *args, **kwargs):
        super(History, self).__init__(data, *args, **kwargs)
    
    def _set_data(self): 
        self._type = self.data.get("type")
        self._uid = self.data.get("uid")
        self._action = self.data.get("action")
        self._name = self.data.get("name")
        self._date = self.data.get("datetime")
        self._created_by_user = self.data.get("created_by")
        self._details = self.data.get("details")
        self._source_uid = self.data.get("source_uid")
        self._organization = self.data.get("organization")


class Mapping(Model):
    
    def __init__(self, data, *args, **kwargs):
        super(Mapping, self).__init__(data, *args, **kwargs)
    
    def _set_data(self): 
        self._uid = self.data.get("uid")
        self._organization = self.data.get("organization")
        self._name = self.data.get("name")
        self._mapping = self.data.get("mapping_info")
        self._created_date = self.data.get("created_datetime")
        self._created_by = self.data.get("created_by")

    
class Mapping(Model):
    
    def __init__(self, data, *args, **kwargs):
        super(Mapping, self).__init__(data, *args, **kwargs)
    
    def _set_data(self): 
        self._uid = self.data.get("uid")
        self._name = self.data.get("name")
        self._created_date = self.data.get("created_datetime")

    
class Transfer(Model):
    
    def __init__(self, data, *args, **kwargs):
        super(Transfer, self).__init__(data, *args, **kwargs)

    def _set_data(self): 
        self._uid = self.data.get("uid")
        self._name = self.data.get("name")
        self._created_date = self.data.get("created_datetime")
        self._created_by = self.data.get("created_by")
        self._organization = self.data.get("organization")
        self._source = self.data.get("source")
        self._source_mapping = self.data.get("source_mapping")
        self._destination = self.data.get("destination")
        self._destination_mapping = self.data.get("destination_mapping")
        self._start_date_time = self.data.get("start_datetime")
        self._frequency = self.data.get("frequency")
        self._record_filter = self.data.get("record_filter")
        self._active = self.data.get("active")


class User(Model):
    
    def __init__(self, data, *args, **kwargs):
        super(User, self).__init__(data, *args, **kwargs)

    def _set_data(self): 
        self._uid = self.data.get("uid")
        self._name = self.data.get("name")
        self._created_date = self.data.get("created_datetime")
        self._organization = self.data.get("organization")
