import os
import typing as t

import boto3
from botocore.exceptions import ClientError

from app.log import get_logger

logger = get_logger(__name__)


def make_s3_url(bucket_name: str, region: str, object_name: str):
    return f"https://{bucket_name}.s3.{region}.amazonaws.com/{object_name}"


class S3Client:
    """Helper class to connect to S3 and perform actions on buckets and documents."""

    def __init__(self):
        self.client = boto3.client(
            "s3",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        )

    def upload_fileobj(
        self, fileobj: t.BinaryIO, bucket: str, object_name: str
    ) -> t.Union[str, bool]:
        """Upload a file object to an S3 bucket.

        Args:
            fileobj (t.IO): a file object opened in binary mode, not text mode.
            bucket (str): name of the bucket to upload the file to.
            object_name (str): key (filename) of the resulting file on s3. Should include the file extension.

        Returns:
            URL to file if upload succeeds, False if it fails.
        """

        try:
            self.client.upload_fileobj(fileobj, bucket, object_name)
        except ClientError as e:
            logger.error(e)
            return False

        return make_s3_url(bucket, os.getenv("AWS_REGION"), object_name)

    def upload_file(
        self, file_name: str, bucket: str, object_name: t.Optional[str] = None
    ) -> t.Union[str, bool]:
        """Upload a file to an S3 bucket by providing its filename.

        Args:
            file_name (str): name of the file to upload.
            bucket (str): name of the bucket to upload the file to.
            object_name (str, optional): key (filename) of the resulting file on s3. Should include the file extension. If not provided, the name of the local file is used.

        Returns:
            URL to file if upload succeeds, False if it fails.
        """

        # If S3 object_name was not specified, use file_name
        if object_name is None:
            object_name = os.path.basename(file_name)

        # Upload the file
        s3_client = boto3.client("s3")
        try:
            s3_client.upload_file(file_name, bucket, object_name)
        except ClientError as e:
            logger.error(e)
            return False

        return make_s3_url(bucket, os.getenv("AWS_REGION"), object_name)
