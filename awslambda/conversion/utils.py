
from typing import Dict, List

from customtyping import *

# # Define new types
# CsvRow = Dict[str, str]
# CsvFile = Dict[str, List[CsvRow]]

# SfObject = Dict[str, str]
# SfRecord = Dict[str, SfObject]

# MappingType = List[Dict[str, Any]]

    
def write_records_to_str(csv_files: Dict[str, str], field_order: Dict[str, str]) -> str:
    """Write the converted records to a string with correct field order.
    
    Parameters
    ----------
    csv_files : Dict
        Filenames to dicts of fieldname: list of values.
    
    Returns
    -------
    str
        String ready to be write to csv file.
    """
    # TODO 1: This is total not going to work if there are lists of values.
    for fn, converted_records in csv_files.items():
        ordered_headers = field_order[fn]
        s = []
        s.append('\t'.join(ordered_headers))
        s.append('\t'.join(converted_records[k] for k in ordered_headers)) 
        return '\n'.join(s)


# def write_records_to_str(converted_records: Dict[str, str]) -> str:
#     """Convert a dict of field names to values to a string representating file content."""
#     s = []
#     header = converted_records.keys()
#     s.append('\t'.join(header))
#     s.append('\t'.join(converted_records[k] for k in header)) 
#     return '\n'.join(s)