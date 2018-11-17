"""
This module can load HMIS standard csv files and convert them to OLI Salesforce object.
A separate record for each client is created.

It needs HMIS csv files and the Cemaritan mapping json file, oli_mapping.json
"""

import os
import itertools
import functools
import json
from typing import Any, Dict, List, Tuple

import pandas as pd


def _get_sf_value(hmis_value: str, source: Any, singlevalue: bool) -> Tuple[str, str, str]:
    """Retrieve SF value corresponding to the supplied HMIS value.
    
    Parameters
    ----------
    hmis_value : str
        Value from HMIS csv file.
    source : Dict[str, str] or List[Dict[str, str]]
        Source object from the mapping for the SF object corresponding to the HMIS object.
    singvalue : bool
        True if `source` is a Dict. False if a List.
    """
    if singlevalue:
        sf_obj = source['SF Object']
        sf_field = source['SF Field']
        if (sf_obj is None) or (sf_field is None):
            return None
        return (sf_obj, sf_field, hmis_value)
    else:
        # Loop through the multiple choices to find the one that matches the input.
        for elt in source:
            sf_obj = elt['SF Object']
            sf_field = elt['SF Field']
            sf_val = elt['SF Value']
            if (sf_obj is None) or (sf_field is None):
                continue
            if str(elt['HMIS Value']) == str(hmis_value):
                return (sf_obj, sf_field, sf_val)
            

def collect_mappings_by_filename(mapping: List[Dict[str, Dict[str, Any]]]) -> Dict[str, List[Dict[str, Dict[str, Any]]]]:
    """Collect the mapping elements by filenames."""
    mappings_by_csv = {}
    for elt in mapping:
        csv_fn = elt['HMIS']['csv filename']
        mappings_by_csv.setdefault(csv_fn, []).append(elt)
    return mappings_by_csv


def _create_lists_of_tuples(client_files_dfs: Dict[str, pd.DataFrame], 
                           mappings_by_csv: Dict[str, Dict]) -> Dict[str, List[Tuple[str, str, str]]]:
    """Convert HMIS csv files into lists of tuples, mapped to by client Ids.
    
    Parameters
    ----------
    client_files_dfs
        Dict[filename, csv file as DataFrame]
    mappings_by_csv
        Dict[filename, Dict]
    
    Return
    ------
    Dict[client_id, List of Tuples or List of Lists of Tuples]
    
    """
    id_to_tuples = {}
    # Loop through HMIS csv files.
    for name, df in client_files_dfs.items():
        # Get the mapping entries related to this file.
        file_mapping = mappings_by_csv.get(name)
        if file_mapping is not None:
            # Loop through each row from the file.
            for row in df.iterrows():
                temp = []
                # For each element in the mapping file, get the mapping info
                # and pass to function to build SF object.
                for elt in file_mapping:
                    hmis_val = row[1][elt['HMIS']['element']]
                    res = _get_sf_value(hmis_val, elt['Source'], elt['SingleValue'])
                    if res is not None:
                        temp.append(res)
                if len(temp) > 0:
                    id_to_tuples.setdefault(row[1]['PersonalID'], []).append(temp)
    return id_to_tuples


def _build_object(list_of_tuples: List[Tuple[str, str, str]]) -> Dict[str, str]:
    """Convert list of tuples into a SF object."""
    obj = {}
    for tup in list_of_tuples:
        obj[tup[1]] = tup[2]
    return obj


singletons = ['OLI_Client__c']
multiples = ['Snapshots_Forms__c']

def _create_sf_object(all_list_of_tuples: Any) -> Dict[str, Dict[str, str]]:
    """Convert list of (possibly lists) of tuples into SF objects."""
    objs_for_client = {}
    # Handle records for objects that are one per client.
    for obj_name in singletons:
        list_of_tuples = list(itertools.chain.from_iterable(x for x in all_list_of_tuples if x[0][0] == obj_name))
        res = _build_object(list_of_tuples)
        objs_for_client[obj_name] = res
        
    # Handle records for objects that can have multiple instances per client.
    for obj_name in multiples:
        temp = []
        list_of_lists_of_tuples = [x for x in all_list_of_tuples if x[0][0] == obj_name]
        for list_of_tuples in list_of_lists_of_tuples:
            res = _build_object(list_of_tuples)
            temp.append(res)
        objs_for_client[obj_name] = temp
    return objs_for_client
    

def convert_files(csv_folder_path: str, mapping_path: str, output_folder_path: str=None):
    """Converts 9 of the HMIS standard csv files to SF objects.

    Converts the following files. Only Client.csv is required.
    'IncomeBenefits.csv',
    'Client.csv',
    'EmploymentEducation.csv',
    'Exit.csv',
    'Services.csv',
    'EnrollmentCoC.csv',
    'Disabilities.csv',
    'Enrollment.csv',
    'HealthAndDV.csv'
    """

    mapping = json.load(open(mapping_path))

    # Collect mapping by csv files.
    mappings_by_csv = collect_mappings_by_filename(mapping)

    # Files to load.
    fns = ['IncomeBenefits.csv',
            'Client.csv',
            'EmploymentEducation.csv',
            'Exit.csv',
            'Services.csv',
            'EnrollmentCoC.csv',
            'Disabilities.csv',
            'Enrollment.csv',
            'HealthAndDV.csv']

    # Load csv files into separate dataframes and key by filename.
    dfs = {fn: pd.read_csv(os.path.join(csv_folder_path, fn)) for fn in fns}

    # Create lists of (possibly lists) of tuples[filename, SF object name, value]
    id_to_tuples = _create_lists_of_tuples(client_files_dfs=dfs, mappings_by_csv=mappings_by_csv)

    # Convert the lists (of lists) of tuples into SF objects.
    sf_objects = {id_: _create_sf_object(tuples) for id_, tuples in id_to_tuples.items()}

    return sf_objects