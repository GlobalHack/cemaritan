import json
from typing import Dict, Tuple


class Transfer:
    def __init__(self, data, *args, **kwargs):
        """Class for handling Transfers

        Example:
        {
            CreatedDate	Timestamp
            CreatedByUser	UID
            Org	UID
            Source	Connection
            SourceMapping	DataMapping
            Destination	Connection
            DestinationMapping	DataMapping
            StartTime	Timestamp
            Frequency	
            OneTime	boolean
            RecordFilter	
            Name	string
            UID	UID
            Active	boolean
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
        self._name = self.data.get("Name", None)
        self._created_date = self.data.get("CreatedDate", None)
        self._created_by = self.data.get("CreatedBy", None)
        self._organization = self.data.get("Organization", None)
        self._source = self.data.get("Source", None)
        self._source_mapping = self.data.get("SourceMapping", None)
        self._destination = self.data.get("Destination", None)
        self._destination_mapping = self.data.get("DestinationMapping", None)
        self._start_date_time = self.data.get("StartDateTime", None)
        self._frequency = self.data.get("Frequency", None)
        self._record_filter = self.data.get("RecordFilter", None)
        self._active = self.data.get("Active", True)

    def from_dict(self, transfer_dict: Dict):
        try:
            return transfer_dict
        except Exception as e:
            print("Parameter 'transfer_dict' is not a valid dict: " + e)

    def from_json(self, transfer_json: str):
        try:
            return self.from_dict(json.loads(transfer_json))
        except Exception as e:
            print("Parameter 'transfer_json' is not a valid JSON string: " + e)

    def from_tuple(self, transfer_tuple: Tuple):
        try:
            return {
                "UID": transfer_tuple[0],
                "Name": transfer_tuple[1],
                "CreatedDate": transfer_tuple[2],
                "CreatedBy": transfer_tuple[3],
                "Organization": transfer_tuple[4],
                "Source": transfer_tuple[5],
                "SourceMapping": transfer_tuple[6],
                "Destination": transfer_tuple[7],
                "DestinationMapping": transfer_tuple[8],
                "StartDateTime": transfer_tuple[9],
                "Frequency": transfer_tuple[10],
                "RecordFilter": transfer_tuple[11],
                "Active": transfer_tuple[12],
            }
        except Exception as e:
            print("Parameter 'transfer_tuple' is not valid: " + e)

    def to_dict(self):
        return self.data

    def to_json(self):
        return json.dumps(self.data)
