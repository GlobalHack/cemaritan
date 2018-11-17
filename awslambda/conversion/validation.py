"""
The HMIS data standard includes logic for setting values in certain fields based 
on the values or non-values in other fields. This logic is depenendent on the field 
values once they are transformed from the source vocabulary to the HMIS vocabulary 
and mapped from source fields to HMIS fields. Thus, this logic is source independent 
and is applied only after all the source to HMIS mapping and translations have occurred. 
Thus, the code to apply this logic can be written once and used for all data conversions 
regardless of the source.

Currently throwing error, but should eventually log out the errors for bad data.

Printing a warning where the HMIS logic is unclear. Need to get clarification 
on what to do in that situation.
"""

import logging
import re
from typing import Any, Dict, List

from customtyping import *

RACE_FIELDS = ['AmIndAKNative', 'Asian', 'BlackAfAmerican', 'NativeHIOtherPacific', 'White']
RACE_NOT_SELECTED = '0'
DATA_NOT_COLLECTED = '99'


def validate_csv_files(converted_csv_files: Dict[str, CsvFile]) -> Dict[str, CsvFile]:
    """Perform HMIS logic and validation on a converted record.
    
    This is an in-place operation because any unaltered values still 
    need to be return as part of the object.
    """
    converted_csv_files['Client.csv'] = [_client(_csvrow) for _csvrow in converted_csv_files['Client.csv']]
    return converted_csv_files
    

### Functions to apply HMIS logic and validation to individual Csv Rows.

def _client(client_csv: CsvRow) -> CsvRow:
    """Perform post conversion HMIS logic on Client.csv data."""
    client_csv = _race(client_csv)
    client_csv = _veteran(client_csv)
    return client_csv
    
    
def _race(client_csv: CsvRow) -> CsvRow:
    """Apply HMIS logic to race fields."""
    ### Races
    # Check if any race was select.
    if any((client_csv[r]) for r in RACE_FIELDS):
        # At least one race was selected, so set the others to 0.
        for r in RACE_FIELDS:
            if not client_csv[r]:
                client_csv[r] = RACE_NOT_SELECTED
    else:
        # No race was selected.
        # Check if RaceNone field has a value:
        # 8 Client doesn’t know
        # 9 Client refused
        # 99 Data not collected
        
        # Check if RaceNone is empty.
        if client_csv['RaceNone'] == '':
            # RaceNone field is empty, so print a warning and set it to DNC.
            # Printing a warning, because not sure what should actually be done here 
            # according to HMIS specs.
            logging.warning('Value is missing for: RaceNone. Setting to DNC.')
            client_csv['RaceNone'] = DATA_NOT_COLLECTED
        # Check if RaceNone is DNC
        if client_csv['RaceNone'] == DATA_NOT_COLLECTED:
            # Fill in all races with DNC value
            for r in RACE_FIELDS:
                if not client_csv[r]:
                    client_csv[r] = DATA_NOT_COLLECTED
        elif client_csv['RaceNone'] not in {8, 9}:
            # RaceNone is not DNC, so it must be 8 or 9, else throw an error.
            raise ValueError(f'Invalid value of {client_csv["RaceNone"]} for RaceNone.')
    return client_csv


def _veteran(client_csv: CsvRow) -> CsvRow:
    """Apply HMIS logic to veteran fields."""
    # Fill in DNC if blank
    if client_csv['VeteranStatus'] == '':
        client_csv['VeteranStatus'] = DATA_NOT_COLLECTED
    # Check years
    year_re = re.compile('^19[2-9]/d|20[0-1]/d$')
    if client_csv['YearEnteredService'] != '':
        if len(year_re.find(client_csv['YearEnteredService'])) < 1:
            raise ValueError(f"Invalid value of {client_csv['YearEnteredService']} for YearEnteredService.")
    if client_csv['YearSeparated'] != '':
        if len(year_re.find(client_csv['YearSeparated'])) < 1:
            raise ValueError(f"Invalid value of {client_csv['YearSeparated']} for YearSeparated.")
    return client_csv
