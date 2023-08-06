from google.cloud import storage
from google.oauth2 import service_account


class GcsWrapper:
    client = None
    bucket_name: str
    credentials_file_path: str = ""
    auth_scopes: list = ['https://www.googleapis.com/auth/cloud-platform']

    def __init__(
        self,
        bucket_name: str,
        credentials_file_path: str = None,
        auth_scopes: list = None
    ):
        self.bucket_name = bucket_name
        self.credentials_file_path = credentials_file_path or self.credentials_file_path
        self.auth_scopes = auth_scopes or self.auth_scopes
        self._prepare_objects()

    def _prepare_objects(self):
        if self.credentials_file_path:
            creds = service_account.Credentials.from_service_account_file(
                self.credentials_file_path,
                scopes=self.auth_scopes
            )
            self.client = storage.Client(credentials=creds)
        else:
            self.client = storage.Client()
        self.bucket = self.client.bucket(self.bucket_name)

    def upload_blob_from_file(self, source_filepath: str, dest_filepath: str):
        """
        Uploads a local file at `source_filepath` to the
        bucket at `dest_filepath` where `dest_filepath`
        includes the partition and desired remote name
        """
        blob = self.bucket.blob(dest_filepath)
        blob.upload_from_filename(source_filepath)

    def upload_blob_from_string(self, source_string: str, dest_filepath: str):
        """
        Uploads a local file at `source_filepath` to the
        bucket at `dest_filepath` where `dest_filepath`
        includes the partition and desired remote name
        """
        blob = self.bucket.blob(dest_filepath)
        blob.upload_from_string(source_string)

    def download_blob_as_string(self, blob_name: str) -> str:
        """
        Uploads a local file at `source_filepath` to the
        bucket at `dest_filepath` where `dest_filepath`
        includes the partition and desired remote name
        """
        blob = self.bucket.blob(blob_name)
        return blob.download_as_string()

    def delete_blob(self, blob_name: str):
        """
        Deletes a blob from the bucket.
        :param blob_name: remote name of blob including partition.
       """
        blob = self.bucket.blob(blob_name)
        blob.delete()

    @staticmethod
    def format_gcs_partition(job_title, location):
        rv = f'{location or ""}/{job_title or ""}/'
        rv = rv.replace(" ", "_").lower()
        return rv
