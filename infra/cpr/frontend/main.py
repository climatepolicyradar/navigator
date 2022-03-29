import pulumi_aws as aws
import mimetypes
import os

from pulumi import export, FileAsset, ResourceOptions, Output


class Frontend:
    """The frontend.

    Inspired by https://github.com/pulumi/examples/tree/master/aws-py-static-website
    """

    def __init__(self):
        target_domain = "www.climatepolicyradar.org"
        web_contents_path = "todo"

        # Create an S3 bucket configured as a website bucket.
        content_bucket = aws.s3.Bucket(
            "contentBucket",
            bucket=target_domain,
            acl="public-read",
            website=aws.s3.BucketWebsiteArgs(
                index_document="index.html", error_document="404.html"
            ),
        )

        # create the bucket objects
        crawl_directory(web_contents_path, bucket_object_converter, content_bucket)

        # Create a logs bucket for the CloudFront logs
        # logs_bucket = aws.s3.Bucket('requestLogs', bucket=f'{target_domain}-logs', acl='private')

        export("content_bucket_url", Output.concat("s3://", content_bucket.bucket))
        export("content_bucket_website_endpoint", content_bucket.website_endpoint)


def bucket_object_converter(filepath, content_bucket, web_contents_path):
    """Takes a file path and returns a bucket object managed by Pulumi"""
    relative_path = filepath.replace(web_contents_path + "/", "")
    # Determine the mimetype using the `mimetypes` module.
    mime_type, _ = mimetypes.guess_type(filepath)
    content_file = aws.s3.BucketObject(
        relative_path,
        key=relative_path,
        acl="public-read",
        bucket=content_bucket.id,
        content_type=mime_type,
        source=FileAsset(filepath),
        opts=ResourceOptions(parent=content_bucket),
    )


def crawl_directory(content_dir, bucket_object_converter_fn, content_bucket):
    """Crawl `content_dir` (including subdirectories) and apply the function to each file."""
    for file in os.listdir(content_dir):
        filepath = os.path.join(content_dir, file)

        if os.path.isdir(filepath):
            crawl_directory(filepath, bucket_object_converter_fn, content_bucket)
        elif os.path.isfile(filepath):
            bucket_object_converter_fn(filepath, content_bucket, content_dir)
