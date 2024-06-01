from google.cloud import storage
from io import BytesIO
import pandas as pd
from os import environ
from base64 import b64decode
from json import loads

# from dotenv import load_dotenv

# load_dotenv()


def get():
    """
    Get the data from a storage bucket and combine it into a single DataFrame.

    Returns:
        pandas.DataFrame: The combined DataFrame containing the data from all the Parquet files.
    """

    bucket_name = environ.get("BUCKET_NAME")
    directory_name = "recently_played"

    gcp_cred_file = environ.get("GCP_CREDS")
    gcp_cred_file = b64decode(gcp_cred_file)
    gcp_cred_file = loads(gcp_cred_file.decode())

    storage_client = storage.Client.from_service_account_info(gcp_cred_file)

    bucket = storage_client.bucket(bucket_name)
    blobs = bucket.list_blobs(prefix=directory_name)
    files = [blob.name for blob in blobs if blob.name.endswith(".parquet")]

    # Download each Parquet file and read it into a DataFrame
    dfs = []
    for file in files:
        blob = bucket.blob(file)
        file_content = blob.download_as_string()
        df = pd.read_parquet(BytesIO(file_content))
        dfs.append(df)
    df = pd.concat(dfs, ignore_index=True)
    storage_client.close()
    return df
