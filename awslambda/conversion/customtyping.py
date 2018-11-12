
from typing import Dict, List, Any

# Define typing aliases
CsvRow = Dict[str, str]
CsvFile = List[CsvRow]

SfObject = Dict[str, str]
SfRecord = Dict[str, SfObject]

MappingType = List[Dict[str, Any]]