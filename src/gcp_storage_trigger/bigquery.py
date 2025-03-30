import google.auth
from google.cloud import bigquery
from loguru import logger


DEFAULT_SCOPES = [
    "https://www.googleapis.com/auth/bigquery",
]

def _client() -> bigquery.Client:
    """Initialize a bigquery.Client object

    Returns:
        bigquery.Client: An authorized bigquery.Client object
    """
    credentials, project = google.auth.default(scopes=DEFAULT_SCOPES)
    return bigquery.Client(project, credentials)


def write_to_table(data: list[dict], table: str) -> None:
    """Upload data to a table in BigQuery

    Args:
        data (List[dict]): The data to upload
        table (str): The table to upload the data to

    Raises:
        RuntimeError: Raise an error if something goes wrong
    """
    logger.info(f"Appending {len(data)} row(s) into {table}")
    if not data:
        logger.info("No data to insert")
        return None
    
    errors = _client().insert_rows_json(table=table, json_rows=data)
    if errors:
        logger.error(errors)
        raise RuntimeError(
            "Data upload to BigQuery failed. Check the logs for more information"
        )
    return None


def move_delta_to_table(delta:str ,datetime_str:str, table:str) -> None:
    """Ingest data from a delta table to a main table

    Args:
        delta (str): The delta table
        datetime_str (str): The datetime string
        table (str): The main table
    """
    logger.info(f"Ingesting data from {delta} to {table}")
    query = f"""
    INSERT INTO `{table}`
    SELECT * FROM `{delta}`
    WHERE DATETIME(last_update) = DATETIME("{datetime_str}")
    """
    job = _client().query(query)
    job.result()
    if job.errors:
        logger.error(job.errors)
        raise RuntimeError(
            f"Data ingestion from {delta} to {table} failed"
        )
    logger.info(f"Data ingested from {delta} to {table} successfully")

    return None


def get_table(table:str) -> bigquery.Table:
    """Get a BigQuery table object

    Args:
        table (str): The table to get

    Returns:
        bigquery.Table: The BigQuery table object
    """
    return _client().get_table(table)