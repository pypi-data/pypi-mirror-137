import uuid
import logging
import json
import requests
import base64
import os

from pathlib import Path
from datetime import datetime

from alira.instance import Instance
from alira.modules.module import Connection, InternalException

from botocore.exceptions import EndpointConnectionError

PIPELINE_MODULE_NAME = "rest"


class RestAuthentication:
    def __init__(
        self, service: str = None, username: str = None, password: str = None, **kwargs
    ):
        self.service = service or os.environ.get("ALIRA_REST_SERVICE", None)
        self.username = username or os.environ.get("ALIRA_REST_USERNAME", None)
        self.password = password or os.environ.get("ALIRA_REST_PASSWORD", None)
        self.access_token = None

    def get_access_token(self, refresh: bool = False):
        if self.access_token is None or refresh:
            logging.info(f"Authenticating Rest module at {self.service}")

            try:
                response = self._request()
                if response.status_code != 200:
                    raise InternalException(
                        f"There was an error logging in with the Rest service. Message: {response.text}"
                    )
                token = json.loads(response.text)

                self.access_token = token["access_token"]
            except InternalException as e:
                raise e
            except Exception as e:
                raise InternalException(
                    f"There was an error logging in with the Rest service. {e}"
                ) from e

        return self.access_token

    def _request(self):
        url = "/".join(
            map(
                lambda x: str(x).rstrip("/"),
                [self.service, "login"],
            )
        )
        return requests.post(
            url=url, json={"username": self.username, "password": self.password}
        )


class Rest(Connection):
    def __init__(
        self,
        configuration_directory: str,
        module_id: str = None,
        pipeline_id: str = None,
        files: str = None,
        files_directory: str = None,
        upload_files: bool = True,
        **kwargs,
    ):
        super().__init__(
            configuration_directory=configuration_directory,
            module_id=module_id or PIPELINE_MODULE_NAME,
            pipeline_id=pipeline_id,
            **kwargs,
        )

        self.files = files
        self.files_directory = files_directory or "files"
        self.upload_files = upload_files

    def run(self, instance: Instance, rest_authentication, **kwargs):
        super().run(instance, **kwargs)

        access_token = rest_authentication.get_access_token()

        url = "/".join(
            map(
                lambda x: str(x).rstrip("/"),
                [rest_authentication.service, "instances", self.pipeline_id],
            )
        )

        try:
            files = self._get_files(instance)
            response = self._request(instance, access_token, url, files)

            # If the access token we are currently using is expired, we want to
            # refresh it and try again.
            if response.status_code == 401:
                access_token = rest_authentication.get_access_token(refresh=True)
                response = self._request(instance, access_token, url, files)

            if response.status_code != 201:
                raise InternalException(
                    f"There was an error uploading instance. Message: {response.text}"
                )

            return json.loads(response.text)

        except InternalException as e:
            raise e
        except Exception as e:
            raise InternalException(
                f"There was an error uploading instance. {e}"
            ) from e

    def _get_files(self, instance: Instance):
        if self.files:
            filenames = instance.get_attribute(self.files, default=instance.files)
        else:
            filenames = instance.files

        if not isinstance(filenames, list):
            filenames = [filenames]

        result = {}
        for filename in filenames:
            if self.upload_files:
                try:
                    file_path = os.path.join(
                        self.configuration_directory, self.files_directory, filename
                    )
                    data = open(file_path, "rb").read()
                    file = base64.b64encode(data).decode("utf-8")
                except Exception as e:
                    logging.error(f"There was an error loading the file {file_path}")
                    file = None
            else:
                file = None

            result[filename] = file

        return result

    def _request(self, instance: Instance, access_token: str, url: str, files: dict):
        data = {
            "instance_id": instance.id,
            "prediction": instance.prediction,
            "confidence": instance.confidence,
            "files": files,
            "date": datetime.utcnow().isoformat(),
            "metadata": instance.metadata,
            "properties": instance.properties,
        }

        return requests.post(
            url=url,
            json=data,
            headers={"Authorization": f"Bearer {access_token}"},
        )
