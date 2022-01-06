import os
import typing as t
import re

import boto3
from botocore.exceptions import ClientError

from app.log import get_logger

logger = get_logger(__name__)


class S3Document:
    def __init__(self, bucket_name: str, region: str, key: str):
        self.bucket_name = bucket_name
        self.region = region
        self.key = key

    @property
    def url(self):
        return f"https://{self.bucket_name}.s3.{self.region}.amazonaws.com/{self.key}"

    @classmethod
    def from_url(cls, url: str) -> "S3Document":
        """Create an S3 document from a URL

        Returns:
            S3Document
        """

        bucket_name, region, key = re.findall(
            r"https:\/\/([\w-]+).s3.([\w-]+).amazonaws.com\/([\w.-]+)", url
        )[0]

        return S3Document(bucket_name=bucket_name, region=region, key=key)


class S3Client:
    """Helper class to connect to S3 and perform actions on buckets and documents."""

    def __init__(self):
        self.client = boto3.client(
            "s3",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        )

    def upload_fileobj(
        self, fileobj: t.BinaryIO, bucket: str, key: str
    ) -> t.Union[S3Document, bool]:
        """Upload a file object to an S3 bucket.

        Args:
            fileobj (t.IO): a file object opened in binary mode, not text mode.
            bucket (str): name of the bucket to upload the file to.
            key (str): filename of the resulting file on s3. Should include the file extension.

        Returns:
            S3Document representing file if upload succeeds, False if it fails.
        """

        try:
            self.client.upload_fileobj(fileobj, bucket, key)
        except ClientError as e:
            logger.error(e)
            return False

        return S3Document(bucket, os.getenv("AWS_REGION"), key)

    def upload_file(
        self, file_name: str, bucket: str, key: t.Optional[str] = None
    ) -> t.Union[S3Document, bool]:
        """Upload a file to an S3 bucket by providing its filename.

        Args:
            file_name (str): name of the file to upload.
            bucket (str): name of the bucket to upload the file to.
            key (str, optional): filename of the resulting file on s3. Should include the file extension. If not provided, the name of the local file is used.

        Returns:
            URL to file if upload succeeds, False if it fails.
        """

        # If S3 object_name was not specified, use file_name
        if key is None:
            key = os.path.basename(file_name)

        # Upload the file
        try:
            self.client.upload_file(file_name, bucket, key)
        except ClientError as e:
            logger.error(e)
            return False

        return S3Document(bucket, os.getenv("AWS_REGION"), key)

    def copy_document(
        self, s3_document: S3Document, new_bucket: str, new_key: t.Optional[str] = None
    ) -> S3Document:
        """Copy a document from one bucket and key to another bucket, and optionally a new key.

        Args:
            s3_document (S3Document): original document.
            new_bucket (str): bucket to copy document to.
            new_key (str, optional): key for the new document. Defaults to None, meaning that the key
            of the original document is used.

        Returns:
            S3Document: representing the copied document.
        """

        copy_source = {"Bucket": s3_document.bucket_name, "Key": s3_document.key}

        if not new_key:
            new_key = s3_document.key

        self.client.copy_object(CopySource=copy_source, Bucket=new_bucket, Key=new_key)

        return S3Document(new_bucket, os.getenv("AWS_REGION"), new_key)

    def delete_document(self, s3_document: S3Document) -> None:
        """Delete a document.

        Args:
            s3_document (S3Document): document to delete.
        """

        self.client.delete_object(Bucket=s3_document.bucket_name, Key=s3_document.key)

    def move_document(
        self, s3_document: S3Document, new_bucket: str, new_key: t.Optional[str] = None
    ) -> S3Document:
        """Move a document from one bucket and key to another bucket, and optionally a new key.

        Args:
            s3_document (S3Document): original document.
            new_bucket (str): bucket to move document to.
            new_key (str, optional): key for the new document. Defaults to None, meaning that the key
            of the original document is used.

        Returns:
            S3Document: representing the moved document.
        """

        self.copy_document(s3_document, new_bucket, new_key)

        self.delete_document(s3_document)

        return S3Document(new_bucket, os.getenv("AWS_REGION"), new_key)


def get_s3_client():
    return S3Client()
