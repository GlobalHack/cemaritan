import json

class Organization:
    def __init__(self, *args, **kwargs):
        """ Class for handling Organizations

        Example:
        {
            UID	
            CreatedDate	Timestamp
            Connections	Array[Connection]
            Transfers	Array[Transfer]
            Transfer History	Array[]
            Download History	Array[]
            Upload History	Array[]
        }
        """
        pass
    
    def from_dict(self, org_dict: Dict):
        self._org_dict = org_dict
        self._uid = org_dict.get("UID", None)
        self._created_date = org_dict.get("CreatedDate", None)
        self._connections = org_dict.get("Connections", None)
        self._transfers = org_dict.get("Transfers", None)
        self._transfer_history = org_dict.get("TransferHistory", None)
        self._download_history = org_dict.get("DownloadHistory", None)
        self._upload_history = org_dict.get("UploadHistory", None)

    def from_json(self, org_json: str):
        self.from_dict(json.loads(org_json))

    def to_dict(self):
        return self._org_dict

    def to_json(self):
        return json.dumps(self._org_dict)
