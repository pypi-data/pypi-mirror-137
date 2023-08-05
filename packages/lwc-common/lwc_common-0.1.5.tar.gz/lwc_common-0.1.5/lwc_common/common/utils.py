import json
import os
from concurrent.futures import as_completed, ProcessPoolExecutor, \
    ThreadPoolExecutor
from datetime import datetime

from google.cloud import storage
from google.oauth2 import service_account

from lwc_common.common.constants import GOOGLE_CREDENTIALS_FILE, \
    CRAWLER_GCS_BUCKET_NAME, PROFILE_DOWNLOAD_DIR, MASTER_LIST

credentials = service_account.Credentials.from_service_account_file(
    GOOGLE_CREDENTIALS_FILE,
    scopes=['https://www.googleapis.com/auth/cloud-platform']
)
storage_client = storage.Client(credentials=credentials)


def upload_blob(filename, gcs_partition):
    """
    Uploads a file to the bucket.
    """
    bucket = storage_client.bucket(CRAWLER_GCS_BUCKET_NAME)
    source_file_path = os.path.join(PROFILE_DOWNLOAD_DIR, filename)
    upload_path = f"{gcs_partition}{filename}"
    blob = bucket.blob(upload_path)
    blob.upload_from_filename(source_file_path)


def delete_blob(bucket_name, blob_name):
    """
    Deletes a blob from the bucket.
    :param bucket_name: "your-bucket-name" that contains the blob.
    :param blob_name: "your-object-name" the blob name.
   """
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.delete()


def concurrent_exec(func, iterable, context=(), max_workers=None, method="thread"):
    """
    use multiprocessing to call a function on members of an iterable

    :param func: the function to call
    :param iterable: items you want to call func on
    :param context: params that are passed to all instances
    :param max_workers: maximum number of child processes to use;
                        if 0, we don't use concurrency
    :param method: process | thread (default)
    :return:
    """
    retval = []
    methods = {
        "process": ProcessPoolExecutor,
        "thread": ThreadPoolExecutor
    }
    if max_workers == 0:
        for item in iterable:
            retval.append(func(item, *context))
    else:
        Executor = methods.get(method or "process")
        print(f"Using {Executor.__name__} to call '{func.__name__}' on {iterable}")
        with Executor(max_workers=max_workers) as executor:
            future_to_item = {executor.submit(func, item, *context): item for item in iterable}
            for future in as_completed(future_to_item):
                try:
                    retval.append(future.result())
                except Exception as exc:
                    pass
    return retval


def format_gcs_partition(job_title, location):
    rv = f'{location or ""}/{job_title or ""}/'.replace(" ", "_").lower()
    return rv


def update_lists(partition: str, profile_url: str, success: bool):
    with open(MASTER_LIST) as file:
        master = json.loads(file.read() or "{}")
    monitor = master.get(partition, {})
    successes = set(monitor.get("success", []))
    failures = set(monitor.get("failure", []))
    new = set(monitor.get("new", []))
    new = new - {profile_url}
    if success:
        failures = failures - {profile_url}
        successes.add(profile_url)
    else:
        failures.add(profile_url)

    # write new data
    master[partition] = {
        "new": list(new),
        "success": list(successes),
        "failure": list(failures)
    }
    with open(MASTER_LIST, "w") as file:
        json.dump(master, file, indent=4)
