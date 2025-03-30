from google.cloud import storage
import io
import json
from typing import List
import csv

ALLOWED_ROLES = ["WRITER", "READER", "OWNER"]


def download_file(bucket_name:str, file_path:str, file_object:any=io.BytesIO()) -> List[dict]:
    """Download a file from Google Cloud Storage to a stream

    Args:
        bucket_name (str): name of the GCS bucket
        file_path (str): file_path of the file
        file_object (any, optional): type of file. Defaults to io.BytesIO().

    Returns:
        List[dict]: The data in the file
    """
    blob = storage.Client().bucket(bucket_name).blob(file_path)
    blob.download_to_file(file_object)
    file_object.seek(0)
    reader = csv.DictReader(io.TextIOWrapper(file_object))
    data = list(reader)
    return data