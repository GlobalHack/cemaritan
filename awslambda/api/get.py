import requests


def connections(event, context):
    try:
        s = event["body"]

        connection_list = ["org1", "org2"]

    except Exception as e:
        return {"statusCode": 400, "body": "400 Bad Request\n\n" + json.dumps(str(e))}
    return {"statusCode": 200, "body": connection_list}


def file_upload(event, context):
    """Accept a file with either a single or an array of Salesforce objects and convert them."""
    s = event["body"]
    s_split = s.split("\n")
    payload = "\n".join(s_split[3:-2])
    try:
        obj = json.loads(payload)
        if isinstance(obj, list):
            obj_len = len(obj)
            list_of_converted_objects = [convert(obj) for obj in obj]
            # Consolidate into a single set of csv files.
            consolidated_csv_files = combine_csv_files(
                csv_files=list_of_converted_objects
            )
            # Pass the converted objects to be combined, written to strings, and saved as files in S3.
            prefix = str(datetime.datetime.now()).replace(" ", "T")
            save_files_to_s3(
                bucket=S3_BUCKET_NAME, csv_files=consolidated_csv_files, prefix=prefix
            )
        else:
            obj_len = 1
            # Convert record
            converted_data = convert(obj)

            # Save results to S3
            prefix = str(datetime.datetime.now()).replace(" ", "T")
            save_files_to_s3(
                bucket=S3_BUCKET_NAME, csv_files=converted_data, prefix=prefix
            )

        # Send success notification.
        send_notification(n=obj_len)
    except Exception as e:
        return {"statusCode": 400, "body": "400 Bad Request\n\n" + json.dumps(str(e))}

    return {"statusCode": 200, "body": "Upload successful."}

