
import os
import json
from typing import Dict, List

import pandas as pd

#PATH = '/Users/mpitlyk/Matt/Cemaritan/OLI/notebooks/data/HMIS Data Mapping for OLI - HMIS to SF Data Mapping.tsv'


def convert_spreadsheet_to_json(source: str, destination_path: str):
    """Convert spreadsheet of mapping to json.
    
    Parameters
    ----------
    source : str
        Path of Excel spreadsheet containing mapping on first sheet.
    destination_path : str
        Path to save two output files (mapping and field order).
    """
    df = _load_mapping_spreadsheet(path=source)
    mapping, field_order = _convert_df_to_dict(df=df)
    _save_output(path=destination_path, mapping=mapping, field_order=field_order)


def _load_mapping_spreadsheet(path: str) -> pd.DataFrame:
    """Load the mapping from an Excel spreadsheet and nulls to None."""
    df = pd.read_csv(path, sep='\t', dtype='object')
    df = df.where((pd.notnull(df)), None)
    return df


def _convert_df_to_dict(df: pd.DataFrame) -> Dict:
    """Convert the mapping dataframe to a Dict."""
    # Groupby filename and HMIS element name
    grpby = df.groupby(['Export Filename', 'Name'])

    mapping = []

    current_col_names = ['Type', 'Value', 'Text', 'Default', 'Required', 'SF Object', 'SF Field', 'SF Value']
    new_col_names = ['HMIS Datatype', 'HMIS Value', 'HMIS Text', 'HMIS Default', 'HMIS Required', 'SF Object', 'SF Field', 'SF Value']

    # Building field mappings.
    for name, group in grpby:
        if len(group) == 1:
            # Get only row in group
            row = group.iloc[0]
            # Get HMIS info
            hmis = {}
            hmis['csv filename'] = name[0]
            hmis['element'] = name[1]
            hmis['DE#'] = row['DE#']
            hmis['datatype'] = row['Type']
            # Get SF info
            sf = {}
            sf['SF Object'] = row['SF Object']
            sf['SF Field'] = row['SF Field']
            mapping.append({'HMIS': hmis, 'Source': sf, 'SingleValue': True})
        else:
            # More than one row in group, which means there is a 
            # values list for this HMIS element which each need 
            # to be mapped.
            # Get HMIS info
            hmis = {}
            hmis['csv filename'] = name[0]
            hmis['element'] = name[1]
            hmis['DE#'] = row['DE#']
            hmis['datatype'] = row['Type']
            # Get all value mappings.
            temp = group[current_col_names]
            temp.columns = new_col_names
            sf = temp.to_dict(orient='records')
            mapping.append({'HMIS': hmis, 'Source': sf, 'SingleValue': False})
            
    # Validate mapping elements.
    _ = [_validate_mapping_element(e) for e in mapping]
    # Save field order per csv field.
    # This helps the convesion code create csv files with the correct field order.
    grpby = df.groupby('Export Filename')
    field_order = {}
    for name, group in grpby:
        field_order[name] = group.Name.drop_duplicates().tolist()
    return mapping, field_order


# Vaidation functions

def _check_sf_object_and_field(source: Dict, elt: Dict):
    if (source['SF Object'] is None) != (source['SF Field'] is None):
        # Cannot have one without the other.
        hmis = elt['HMIS']
        raise ValueError(f"SF Object and SF Field must both be present of missing. HMIS filename: {hmis['csv filename']}, HMIS element: {hmis['element']}")


def _validate_mapping_element(elt: Dict):
    """Throws an error if there is a malformed mapping element."""
    hmis = elt['HMIS']
    # Add checks for HMIS element
    source = elt['Source']
    if isinstance(source, list):
        _ = [_check_sf_object_and_field(source=e, elt=elt) for e in source]
    else:
        _check_sf_object_and_field(source=source, elt=elt)


# Save functions

def _save_output(path: str, mapping: List, field_order: Dict):
    """Save the mapping and field order objects to json files."""
    # Save mapping file
    json.dump(mapping, open(os.path.join(path, 'oli_mapping.json'), 'w'))

    # Save field order
    json.dump(field_order, open(os.path.join(path, 'hmis_field_order.json'), 'w'))  


