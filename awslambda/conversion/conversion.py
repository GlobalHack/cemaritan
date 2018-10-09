import sys
import json
from typing import Dict

RACE_FIELDS = ['AmIndAKNative', 'Asian', 'BlackAfAmerican', 'NativeHIOtherPacific', 'White']


def load_mapping() -> Dict:
    """Load the OLI to HIMS mapping into a dict."""
    return json.load(open('oli_mapping.json', 'r'))


def convert_record(record: Dict, mapping: Dict) -> Dict[str, Dict[str, str]]:
    """Convert `record` according to `mapping` and return a dict of data
    ready to be written to HMIS csv files.
    """
    csv_files = {}
    source_record = record
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
        # Need to track which columsn don't get values and write out there default values.
        if not mapped:
            hmis = elt['HMIS']
            csv_files.setdefault(hmis['csv filename'], {})[hmis['element']] = ''
    return csv_files

def hmis_conversion_logic(csv_files: Dict[str, Dict[str, str]]) -> Dict[str, Dict[str, str]]:
    """Update dicts representing csv files with logic that applies to all conversions."""
    ### Client.csv
    client_csv = csv_files['Client.csv']
    # Races
    if all((not client_csv[r]) for r in RACE_FIELDS):
        


def write_record_to_csv(converted_record: Dict) -> Dict:
    for fn, data in csv_files.items():
        with open(fn, 'w') as f:
            header = data.keys()
            f.write('\t'.join(header))
            f.write('\n')
            f.write('\t'.join(data[k] for k in header))            


def convert(record: Dict) -> Dict[str, Dict[str, str]]:
    """Main conversion function to convert a record to a dict, but
    eventually into files.
    """
    mapping = load_mapping()
    return json.dumps(convert_record(record=record, mapping=mapping))


def main():
    record = json.loads(sys.argv[1])
    print(convert(record))


### Lambda handler

def endpoint(event, context):
    
    body = convert(json.loads(event['body']))
    
    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response