"""AWS Helper classes."""
import logging
import os
import re
import typing as t

import boto3
import botocore.client
from botocore.exceptions import ClientError
from botocore.response import StreamingBody

logger = logging.getLogger(__name__)

AWS_REGION = os.getenv("AWS_REGION", "eu-west-1")


class S3Document:
    """A class representing an S3 document."""

    def __init__(self, bucket_name: str, region: str, key: str):  # noqa: D107
        self.bucket_name = bucket_name
        self.region = region
        self.key = key

    @property
    def url(self):
        """Return the URL for this S3 document."""
        return f"https://{self.bucket_name}.s3.{self.region}.amazonaws.com/{self.key}"

    @classmethod
    def from_url(cls, url: str) -> "S3Document":
        """Create an S3 document from a URL.

        Returns:
            S3Document
        """
        bucket_name, region, key = re.findall(
            r"https:\/\/([\w-]+).s3.([\w-]+).amazonaws.com\/([\w.-]+)", url
        )[0]

        return S3Document(bucket_name=bucket_name, region=region, key=key)


class S3Client:
    """Helper class to connect to S3 and perform actions on buckets and documents."""

    def __init__(self):  # noqa: D107
        self.client = boto3.client(
            "s3",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            config=botocore.client.Config(
                signature_version="s3v4",
                region_name=AWS_REGION,
                connect_timeout=10,
            ),
        )

    def upload_fileobj(
        self,
        fileobj: t.BinaryIO,
        bucket: str,
        key: str,
        content_type: t.Optional[str] = None,
    ) -> t.Union[S3Document, bool]:
        """Upload a file object to an S3 bucket.

        Args:
            fileobj (t.IO): a file object opened in binary mode, not text mode.
            bucket (str): name of the bucket to upload the file to.
            key (str): filename of the resulting file on s3. Should include the file extension.
            content_type (str, optional): optional content-type of the file

        Returns:
            S3Document representing file if upload succeeds, False if it fails.
        """
        try:
            if content_type:
                logger.info(
                    f"upload_fileobj: {bucket} {key} with content-type {content_type}"
                )
                self.client.upload_fileobj(
                    fileobj, bucket, key, ExtraArgs={"ContentType": content_type}
                )
                logger.info("upload_fileobj with content-type: DONE")
            else:
                logger.info(f"upload_fileobj: {bucket} {key} with no content-type")
                self.client.upload_fileobj(fileobj, bucket, key)
                logger.info("upload_fileobj with no content-type: DONE")
        except ClientError as e:
            logger.error(e)
            return False
        logger.info("Returning S3Document {} {} {}".format(bucket, AWS_REGION, key))
        return S3Document(bucket, AWS_REGION, key)

    def upload_file(
        self,
        file_name: str,
        bucket: str,
        key: t.Optional[str] = None,
        content_type: t.Optional[str] = None,
    ) -> t.Union[S3Document, bool]:
        """Upload a file to an S3 bucket by providing its filename.

        Args:
            file_name (str): name of the file to upload.
            bucket (str): name of the bucket to upload the file to.
            key (str, optional): filename of the resulting file on s3. Should include the file extension. If not provided, the name of the local file is used.
            content_type (str, optional): optional content-type of the file

        Returns:
            URL to file if upload succeeds, False if it fails.
        """
        # If S3 object_name was not specified, use file_name
        if key is None:
            key = os.path.basename(file_name)

        # Upload the file
        try:
            if content_type:
                self.client.upload_file(
                    file_name, bucket, key, ExtraArgs={"ContentType": content_type}
                )
            else:
                self.client.upload_file(file_name, bucket, key)
        except ClientError:
            logger.exception(f"Uploading {file_name} encountered an error")
            return False

        return S3Document(bucket, AWS_REGION, key)

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

        return S3Document(new_bucket, AWS_REGION, new_key)

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

        return S3Document(new_bucket, AWS_REGION, new_key or s3_document.key)

    def list_files(
        self, bucket: str, max_keys=1000
    ) -> t.Generator[S3Document, None, None]:
        """Yield the documents contained in a bucket on S3.

        Calls the s3 list_objects_v2 function to return all the keys in a given s3 bucket.
        The argument max_keys can be used to control how many keys are returned in each
        call made to s3. This function will always yield all keys in the bucket.

        Args:
            bucket (str): name of the bucket in which the files will be listed.
            max_keys (int): maximum number of s3 keys to return on each request made to s3.

        Returns:
            False if the operation was unsuccessful.

        Yields:
            S3Document: representing each document.
        """
        is_truncated = True
        next_continuation_token = None
        try:
            while is_truncated:
                # Include a continuation token in the arguments to boto3 list_objects_v2
                # if we want to continue listing files from the last call

                kwargs = {"Bucket": bucket, "MaxKeys": max_keys}
                if next_continuation_token:
                    kwargs["ContinuationToken"] = next_continuation_token

                response = self.client.list_objects_v2(**kwargs)

                for s3_file in response.get("Contents", []):
                    yield S3Document(bucket, AWS_REGION, s3_file["Key"])

                # Find out whether request was truncated and get continuation token
                is_truncated = response.get("IsTruncated", False)
                next_continuation_token = response.get("NextContinuationToken", None)

        except ClientError:
            logger.exception("Request to list files in bucket '{bucket}' failed")
            raise

    def download_file(self, s3_document: S3Document) -> StreamingBody:
        """Download a file from S3.

        Args:
            s3_document (S3Document): s3 document to retrieve

        Returns:
            Streaming file object
        """
        try:
            response = self.client.get_object(
                Bucket=s3_document.bucket_name, Key=s3_document.key
            )

            return response["Body"]

        except ClientError:
            logger.exception(f"Request for object {s3_document.key} failed")
            raise

    def generate_pre_signed_url(
        self,
        s3_document: S3Document,
    ) -> str:
        """
        Generate a pre-signed URL to an object for file uploads

        :param S3Document s3_document: A description of the document to create/update
        :return str: A pre-signed URL
        """
        try:
            url = self.client.generate_presigned_url(
                "put_object",
                Params={
                    "Bucket": s3_document.bucket_name,
                    "Key": s3_document.key,
                },
            )
            return url
        except ClientError:
            logger.exception(
                f"Request to create pre-signed URL for {s3_document.key} failed"
            )
            raise

    def document_exists(self, s3_document: S3Document) -> bool:
        """
        Detect whether an S3Document already exists in storage.

        :param S3Document s3_document: The s3 document description to check for.
        :return bool: A flag indicating whether the described document already exists.
        """
        try:
            self.client.head_object(Bucket=s3_document.bucket_name, Key=s3_document.key)
            return True
        except ClientError:
            return False


def get_s3_client():
    """Get s3 client for API."""
    return S3Client()
