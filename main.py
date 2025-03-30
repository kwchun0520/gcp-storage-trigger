import functions_framework
from loguru import logger
from typing import Dict
from datetime import datetime,timezone
from src.gcp_storage_trigger.config import CONFIG
from src.gcp_storage_trigger.google import get_project
from src.gcp_storage_trigger.bigquery import write_to_table, move_delta_to_table, get_table
from src.gcp_storage_trigger.storage import download_file
from cloudevents.http import CloudEvent
import uuid


##create a function that will be triggered by a GCS event
@functions_framework.cloud_event
def main(cloud_event:CloudEvent) -> Dict[str,str]:

    data:dict = cloud_event.data
    logger.info(f"Received data: {data}")

    file_path:str = data["name"]
    bucket_name:str = data["bucket"]
    dataset_name,table_name,_ = file_path.split("/")

    if f"{dataset_name}.{table_name}" not in CONFIG.tables:
        logger.warning(f"Table {file_path} is not in the list of tables to process")
        return {"response":"No action taken"}
      
    if not file_path.endswith(".csv"):
        logger.warning(f"File {file_path} is not a CSV file")
        return {"response":"No action taken"}

    logger.info(f"Processing file: {file_path}")
    project = get_project()

    try:
        get_table(table=f"{dataset_name}.{table_name}")
    except Exception as e:
        logger.error(e)
        return {"response":"No action taken"}
    
    datetime_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    job_id = str(uuid.uuid4())
    logger.info(f"Current datetime: {datetime_str}")
    data = download_file(bucket_name=bucket_name, file_path=file_path)
    updated_data = list(map(lambda d: {**d, "last_update":datetime_str, "job_id":job_id, "file_path":file_path}, data))

    destination_table = f"{project}.{dataset_name}.{table_name}"
    delta_table = f"{destination_table}_{CONFIG.delta_suffix}"

    try:
        write_to_table(data=updated_data, table=delta_table)
    except Exception as e:
        logger.error(e)
        return {"response":"An error occurred"}
    
    try:
        move_delta_to_table(delta=delta_table, datetime_str=datetime_str, job_id=job_id, table=destination_table)
    except Exception as e:
        logger.error(e)
        return {"response":"An error occurred"}
    
    return {"response":"File processed successfully"}


if __name__ == '__main__':

    ##create a fake CloudEvent
    attributes = {
        "type": "com.example.sampletype1",
        "source": "https://example.com/event-producer",
    }

    data = {"name": "my_dataset/my_table2/test.csv", "bucket": "my-new-project-bucket-1234"}
    event = CloudEvent(attributes, data)
    main(event)