"""
This module contains utitily functions for converting records to string
and for interacting with AWS resources.
"""

from typing import Dict, List

import boto3

from customtyping import *

# # Define new types
# CsvRow = Dict[str, str]
# CsvFile = Dict[str, List[CsvRow]]

# SfObject = Dict[str, str]
# SfRecord = Dict[str, SfObject]

# MappingType = List[Dict[str, Any]]


### General Utility Functions

def combine_csv_files(csv_files: List[Dict[str, CsvFile]]) -> Dict[str, CsvFile]:
    """Combine csv files from multiple clients into a single set of files.
    
    Parameters
    ----------
    csv_files : List[Dict[str, CsvFile]]
        Each Dict[str, CsvFile] in the List represents a single client from SF.
    
    Returns
    -------
    Dict[str, CsvFile]
        This is the same structure as a single client's csv files, but contains
        information from multiple client records.
    """
    combined_files = {}
    for single_client_dict in csv_files:
        # Dict[str, CsvFile]
        for filename, csvfile in single_client_dict.item():
            combined_files.setdefault(filename, []).extend(csvfile)
    return combined_files


def write_csvfile_to_str(csv_file: CsvFile) -> str:
    """Write the converted records to a string with correct field order.
    
    Assumes that the fields (CsvFile dict keys) are in the HMIS order.
    They should be ordered by `conversion.convert_record`.

    Parameters
    ----------
    csv_files
        Filenames to dicts of fieldname: list of values.
    
    Returns
    -------
    str
        String ready to be written to csv file.
    """
    s = []
    # TODO 2: Can these csvfiles be empty?
    s.append('\t'.join(csv_file[0].keys()))
    for csv_row in csv_file:
        s.append('\t'.join(csv_row.values())) 
    return '\n'.join(s)


### AWS Functions

def save_string_to_s3(s3, bucket: str, name: str, content: str):
    """Save `content` as a file named `name` in bucket `bucket`.
    
    Parameters
    ----------
    s3 : boto3.resource
        A boto3 S3 resource object.
    bucket : str
        Name of the bucket.
    name : str
        Filename to save string as.
    content : str
        Content of the file.
    """
    s3.Object(bucket, name).put(Body=content)


def save_files_to_s3(bucket: str, csv_files: Dict[str, CsvFile]):
    """Save content of HMIS files to S3."""
    # Get S3 resource object
    s3 = boto3.resource('s3')
    # Save each csv HMIS file to S3.
    for filename, csvfile in csv_files.items():
        save_string_to_s3(s3=s3, bucket=bucket, name=filename, content=write_csvfile_to_str(csvfile))

