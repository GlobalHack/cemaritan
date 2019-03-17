import json


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
        pass

    def from_dict(self, transfer_dict: Dict):
        self._transfer_dict = transfer_dict
        self._created_date = transfer_dict.get("CreatedDate", None)
        self._created_by_user = transfer_dict.get("CreatedByUser", None)
        self._org = transfer_dict.get("Org", None)
        self._source = transfer_dict.get("Source", None)
        self._source_mapping = transfer_dict.get("SourceMapping", None)
        self._destination = transfer_dict.get("Destination", None)
        self._destination_mapping = transfer_dict.get("DestinationMapping", None)
        self._start_time = transfer_dict.get("StartTime", None)
        self._frequency = transfer_dict.get("Frequency", None)
        self._one_time = transfer_dict.get("OneTime", True)
        self._record_filter = transfer_dict.get("RecordFilter", None)
        self._name = transfer_dict.get("Name", None)
        self._uid = transfer_dict.get("UID", None)
        self._active = transfer_dict.get("Active", True)

    def from_json(self, transfer_json: str):
        self.from_dict(json.loads(transfer_json))

    def to_dict(self):
        return self._transfer_dict

    def to_json(self):
        return json.dumps(self._transfer_dict)
