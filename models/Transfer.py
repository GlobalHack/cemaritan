import json
from typing import Dict, Tuple


class Transfer:
    def __init__(self, *args, **kwargs):
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

    def from_dict(self, transfer_dict: Dict):
        self._transfer_dict = transfer_dict
        self._uid = transfer_dict.get("UID", None)
        self._name = transfer_dict.get("Name", None)
        self._created_date = transfer_dict.get("CreatedDate", None)
        self._created_by = transfer_dict.get("CreatedBy", None)
        self._organization = transfer_dict.get("Organization", None)
        self._source = transfer_dict.get("Source", None)
        self._source_mapping = transfer_dict.get("SourceMapping", None)
        self._destination = transfer_dict.get("Destination", None)
        self._destination_mapping = transfer_dict.get("DestinationMapping", None)
        self._start_date_time = transfer_dict.get("StartDateTime", None)
        self._frequency = transfer_dict.get("Frequency", None)
        self._record_filter = transfer_dict.get("RecordFilter", None)
        self._active = transfer_dict.get("Active", True)

    def from_json(self, transfer_json: str):
        self.from_dict(json.loads(transfer_json))

    def from_tuple(self, transfer_tuple: Tuple):
        (
            self._uid,
            self._name,
            self._created_date,
            self._created_by,
            self._organization,
            self._source,
            self._source_mapping,
            self._destination,
            self._destination_mapping,
            self._start_date_time,
            self._frequency,
            self._record_filter,
            self._active,
        ) = transfer_tuple

    def to_dict(self):
        return self._transfer_dict

    def to_json(self):
        return json.dumps(self._transfer_dict)
