
import os
import sys
import json

from typing import Dict, List, Any

import conversion.validation as val
from conversion.oli_mapping import oli_mapping
from conversion.hmis_field_order import hmis_field_order
from conversion.utils import combine_csv_files

from conversion.customtyping import *


RACE_FIELDS = ['AmIndAKNative', 'Asian', 'BlackAfAmerican', 'NativeHIOtherPacific', 'White']


def load_mapping() -> MappingType:
    """Load the OLI to HIMS mapping into a dict."""
    # return json.load(open('oli_mapping.json', 'r'))
    return oli_mapping


def load_field_order() -> Dict[str, List[str]]:
    """Load the HMIS field order for each csv file."""
    # return json.load(open('hmis_field_order.json', 'r'))
    return hmis_field_order


def convert_record(record_object: SfRecord, mapping: MappingType, field_order: Dict[str, List[str]]) -> Dict[str, CsvFile]:
    """Convert `record_object` according to `mapping` and return a dict of data
    ready to be written to HMIS csv files.

    New version of `convert_record` accounts for one-to-many relationships.

    Parameters
    ----------
    record_object : Dict
        This is an OLI client record in the following schema:
        {"OLI_Client__c" : _OLI_Client__c_object_,
         "Snapshots_Forms__c": [_Snapshots_Forms__c_object_1_, _Snapshots_Forms__c_object_2_]
        }
        Each `__c_object_` is a Dict[str, str]

    mapping : Dict
        The output of ss_to_json.convert_spreadsheet_to_json which is a dict representing
        the mapping from OLI to HMIS.

        {
            "HMIS": {
                "csv filename": "Client.csv",
                "element": "AfghanistanOEF",
                "DE#": "V1.7",
                "datatype": "I"
            },
            "Source": {
                            "SF Object": null,
                            "SF Field": null
                    },
            "SingleValue": true
        }

    field_order : Dict
        This is used to specify the field order in the returned dict. Python 3.6+ is required to ensure field order.

    Returns
    --------
    return : Dict[str, CsvFile]
        Keys are csv filenames. Values are lists of dict representing a single line in that csv.
    """
    # Collect mapping by csv files.
    mappings_by_csv = {}
    for elt in mapping:
        csv_fn = elt['HMIS']['csv filename']
        mappings_by_csv.setdefault(csv_fn, []).append(elt)
    # Convert data by CSV file. 
    # It is not clear right now what the best, most generic approach is for converting
    # data from SF objects to HMIS format. This code is going to hardcode some special 
    # cases that the current generic mapping framework cannot handle. Once all the 
    # mapping works, and it is clear that it will be worth the effort to generialize 
    # all the conversion steps, this code can be refactored. At the moment, however,
    # it is too hard to envision every edge case, and it is slowing down development.
    csv_files = {}
    # Client.csv
    csv_files['Client.csv'] = [convert_object_single_csv(record_object=record_object, mapping=mappings_by_csv['Client.csv'])]
    # Enrollment.csv
    csv_files['Enrollment.csv'] = convert_enrollment(record_object=record_object, mapping=mappings_by_csv['Enrollment.csv'])
    # Disabilities.csv
    csv_files['Disabilities.csv'] = [convert_object_single_csv(record_object=record_object, mapping=mappings_by_csv['Disabilities.csv'])]
    # Exit.csv
    csv_files['Exit.csv'] = [convert_object_single_csv(record_object=record_object, mapping=mappings_by_csv['Exit.csv'])]
    # EnrollmentCoC.csv
    csv_files['EnrollmentCoC.csv'] = [convert_object_single_csv(record_object=record_object, mapping=mappings_by_csv['EnrollmentCoC.csv'])]
    # IncomeBenefits.csv
    csv_files['IncomeBenefits.csv'] = convert_incomebenefits(record_object=record_object, mapping=mappings_by_csv['IncomeBenefits.csv'])
    # HealthAndDV.csv
    csv_files['HealthAndDV.csv'] = [convert_object_single_csv(record_object=record_object, mapping=mappings_by_csv['HealthAndDV.csv'])]
    # Services.csv
    csv_files['Services.csv'] = convert_services(record_object=record_object, mapping=mappings_by_csv['Services.csv'])

    # Reorder fields
    csv_files_ordered = {}
    for filename, f_order in field_order.items():
        # Get list of unordered dicts.
        unordered_file = csv_files[filename]
        # Create new list of dicts with ordered fields.
        csv_files_ordered[filename] = [{f:_csvrow[f] for f in f_order} for _csvrow in unordered_file]
    return csv_files_ordered


### Generic convert_object function. Used by specific conversion functions.

def convert_object(record_object: SfRecord, mapping: MappingType) -> Dict[str, CsvRow]:
    """Convert a single instance of a SF object to a single row in one or more HMIS csv files."""
    csv_files = {}
    source_record = record_object
    for elt in mapping:
        mapped = False
        if elt['SingleValue']:
            source_object = elt['Source']['SF Object']
            source_field = elt['Source']['SF Field']
            source_value = None
            if source_field is not None:
                source_value = source_record[source_object][source_field]
            if source_value is not None:
                hmis = elt['HMIS']
                csv_files.setdefault(hmis['csv filename'], {})[hmis['element']] = source_value
                mapped = True
                
        else:
            for source in elt['Source']:
                source_object = source['SF Object']
                source_field = source['SF Field']
                source_value = None
                if source_field is not None:
                    source_value = source_record[source_object][source_field]
                if source_value is not None:
                    if source_value == source['HMIS Text']:
                        #print(source_value)
                        hmis = elt['HMIS']
                        csv_files.setdefault(hmis['csv filename'], {})[hmis['element']] = source['SF Value']
                        mapped = True
        # Need to track which columns don't get values and write out their default values.
        if not mapped:
            hmis = elt['HMIS']
            csv_files.setdefault(hmis['csv filename'], {})[hmis['element']] = ''
    return csv_files    


def convert_object_single_csv(record_object: SfRecord, mapping: MappingType) -> CsvRow:
    """Wrapper for `convert_object` that only returns a single csv file."""
    csv_files = convert_object(record_object=record_object, mapping=mapping)
    if len(csv_files) > 1:
        raise ValueError('Too many csv files were returned. Should only be one.')
    return list(csv_files.values())[0]   # Get the list of values, which is a single element.


### Functions for converting specific csv files.
# Must return: CsvFile = List[Dict[str, str]]

def convert_enrollment(record_object: SfRecord, mapping: MappingType) -> CsvFile:
    enroll = convert_object_single_csv(record_object=record_object, mapping=mapping)
    # Hardcoding value because OLI only has one type.
    # TODO 2: Looking at the OLI STC data, this is not true. Need to revisit.
    enroll['RelationshipToHoH'] = 1
    return [enroll]


def convert_incomebenefits(record_object: SfRecord, mapping: MappingType) -> CsvFile:
    """Uses an array of SF objects."""
    converted = []
    for snapshot in record_object['Snapshots_Forms__c']:
        converted.append(convert_object_single_csv(record_object={'Snapshots_Forms__c': snapshot}, mapping=mapping))
    return converted


def convert_services(record_object: SfRecord, mapping: MappingType) -> CsvFile:
    """Uses an array of SF objects."""
    converted = []
    return converted


# Main convert record function
def convert(record: SfRecord) -> Dict[str, CsvFile]:
    """
    Main conversion function to convert a record to a dict.

    Calls functions to convert/translate the record from SF to HMIS,
    perform HMIS logic, and HMIS validation.
    """
    mapping = load_mapping()
    field_order = load_field_order()
    converted_csv_files = convert_record(record_object=record, mapping=mapping, field_order=field_order)
    validated_csv_files = val.validate_csv_files(converted_csv_files=converted_csv_files)
    return validated_csv_files
    

def convert_many(records: List[SfRecord]) -> Dict[str, CsvFile]:
    list_of_converted_objects = [convert(obj) for obj in records]
    # Consolidate into a single set of csv files.
    consolidated_csv_files = combine_csv_files(csv_files=list_of_converted_objects)
    return consolidated_csv_files


# def main():
#     record = json.loads(sys.argv[1])
#     print(convert(record))
