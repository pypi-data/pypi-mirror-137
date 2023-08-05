import boto3
import uuid
import logging
import os

from pathlib import Path

from alira.instance import Instance
from alira.modules.module import Connection

from botocore.exceptions import EndpointConnectionError

PIPELINE_MODULE_NAME = "s3"


class S3(Connection):
    def __init__(
        self,
        configuration_directory: str,
        aws_s3_bucket: str,
        aws_s3_key_prefix: str,
        aws_s3_public: bool,
        module_id: str = None,
        aws_access_key: str = None,
        aws_secret_key: str = None,
        aws_region_name: str = None,
        autogenerate_name: bool = False,
        filtering: str = None,
        file: str = None,
        files_directory: str = None,
        **kwargs,
    ):
        super().__init__(
            configuration_directory=configuration_directory,
            module_id=module_id or PIPELINE_MODULE_NAME,
            **kwargs,
        )

        self.aws_access_key = aws_access_key or os.environ.get(
            "ALIRA_AWS_ACCESS_KEY_ID", None
        )
        self.aws_secret_key = aws_secret_key or os.environ.get(
            "ALIRA_AWS_SECRET_ACCESS_KEY", None
        )
        self.aws_region_name = aws_region_name or os.environ.get(
            "ALIRA_AWS_REGION_NAME", None
        )

        self.filtering = self._load_function(filtering)
        self.aws_s3_bucket = aws_s3_bucket
        self.aws_s3_key_prefix = aws_s3_key_prefix

        self.autogenerate_name = autogenerate_name

        if self.aws_s3_key_prefix and self.aws_s3_key_prefix.endswith("/"):
            self.aws_s3_key_prefix = self.aws_s3_key_prefix[:-1]

        self.aws_s3_public = aws_s3_public

        self.file = file
        self.files_directory = files_directory or "files"

    def run(self, instance: Instance, **kwargs):
        super().run(instance, **kwargs)

        if self.filtering and not self.filtering(instance):
            logging.info(
                f"The instance didn't pass the filtering criteria. Instance: {instance}"
            )
            return {"status": "SKIPPED"}

        default_file = instance.files[0] if instance.files else None
        if self.file:
            filename = instance.get_attribute(self.file, default=default_file)
        else:
            filename = default_file

        if self.autogenerate_name:
            _, file_extension = os.path.splitext(filename)
            s3_key = f"{uuid.uuid4().hex}{file_extension}"
        else:
            s3_key = os.path.basename(filename)

        if self.aws_s3_key_prefix:
            s3_key = f"{self.aws_s3_key_prefix}/{s3_key}"

        filename = os.path.join(
            self.configuration_directory, self.files_directory, filename
        )

        if not os.path.isfile(filename):
            logging.info(f"The file {filename} does not exist")
            return {
                "status": "FAILURE",
                "message": f"The file {filename} does not exist",
            }

        try:
            with open(filename, "rb") as file:
                buffer = file.read()
        except FileNotFoundError:
            logging.exception(f"There was an error loading the file {filename}")
            return {
                "status": "FAILURE",
                "message": f"There was an error loading the file {filename}",
            }

        try:
            self.upload(s3_key=s3_key, filename=filename, buffer=buffer)

            result = {
                "status": "SUCCESS",
                "file_url": f"s3://{self.aws_s3_bucket}/{s3_key}",
            }

            if self.aws_s3_public:
                result[
                    "public_url"
                ] = f"https://{self.aws_s3_bucket}.s3.amazonaws.com/{s3_key}"

            return result
        except EndpointConnectionError as e:
            raise e
        except Exception:
            logging.exception("There was an error uploading the file")
            return {
                "status": "FAILURE",
                "message": "Error uploading the file",
            }

    def upload(self, s3_key, filename, buffer):
        logging.info(
            f'Uploading {filename} to bucket "{self.aws_s3_bucket}" '
            f"and location {s3_key}..."
        )

        session = boto3.Session(
            aws_access_key_id=self.aws_access_key,
            aws_secret_access_key=self.aws_secret_key,
            region_name=self.aws_region_name,
        )
        client = session.client("s3")

        arguments = {"Bucket": self.aws_s3_bucket, "Key": s3_key, "Body": buffer}

        extension = Path(filename).suffix.lower()
        content_type = "binary/octet-stream"
        if extension in [".jpg", ".jpeg"]:
            content_type = "image/jpeg"
        elif extension == ".png":
            content_type = "image/png"

        arguments["ContentType"] = content_type

        if self.aws_s3_public:
            arguments["ACL"] = "public-read"

        client.put_object(**arguments)

        s3_location = f"s3://{self.aws_s3_bucket}/{s3_key}"
        logging.info(f"Uploaded {filename} to {s3_location}")

        return s3_location
