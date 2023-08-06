import os
import re
import json
import logging
import boto3
import requests

from alira.instance import Instance
from alira.modules.module import Connection, ServiceException, Module

from botocore.exceptions import EndpointConnectionError

from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException


PIPELINE_EMAIL_MODULE_NAME = "email"
PIPELINE_SMS_MODULE_NAME = "sms"


class Notification(Connection):
    def __init__(
        self,
        module_id: str,
        filtering: str = None,
        **kwargs,
    ):
        super().__init__(
            module_id=module_id,
            **kwargs,
        )

        self.filtering = self._load_function(filtering)

    def _load_template(self, instance: Instance, template_file):
        with open(
            os.path.join(self.configuration_directory, template_file),
            encoding="UTF-8",
        ) as file:
            template = file.read()

        variables_pattern = re.compile(r"\[\[([A-Za-z0-9_.\"]+)\]\]")

        variables = variables_pattern.findall(template)
        for variable in variables:
            template = template.replace(
                f"[[{variable}]]", str(instance.get_attribute(variable, default=""))
            )

        return template


class EmailNotification(Notification):
    def __init__(
        self,
        configuration_directory: str,
        sender: str,
        recipients: list,
        subject: str,
        template_html_filename: str,
        template_text_filename: str,
        filtering: str = None,
        provider=None,
        **kwargs,
    ):
        super().__init__(
            configuration_directory=configuration_directory,
            module_id=PIPELINE_EMAIL_MODULE_NAME,
            filtering=filtering,
            **kwargs,
        )

        self.sender = sender
        self.recipients = recipients
        self.template_html_filename = template_html_filename
        self.template_text_filename = template_text_filename
        self.subject = subject

        self.provider = provider or AwsSesEmailNotificationProvider(**kwargs)

    def run(self, instance: Instance, **kwargs) -> dict:
        super().run(instance, **kwargs)

        if self.filtering and not self.filtering(instance):
            logging.info(
                f"The instance didn't pass the filtering criteria. Instance: {instance}"
            )
            return {"status": "SKIPPED"}

        if not hasattr(self.provider, "send_email") or not callable(
            self.provider.send_email
        ):
            logging.info("The specified provider is not valid")
            return {
                "status": "FAILURE",
                "message": "Specified provider is not valid",
            }

        try:
            template_text = self._load_template(instance, self.template_text_filename)
        except FileNotFoundError as e:
            logging.exception(e)
            return {
                "status": "FAILURE",
                "message": f"Template file {self.template_text_filename} not found",
            }
        except Exception as e:
            logging.exception(e)
            return {
                "status": "FAILURE",
                "message": "Couldn't load the template text file",
            }

        try:
            template_html = self._load_template(instance, self.template_html_filename)
        except FileNotFoundError as e:
            logging.exception(e)
            return {
                "status": "FAILURE",
                "message": f"Template file {self.template_html_filename} not found",
            }
        except Exception as e:
            logging.exception(e)
            return {
                "status": "FAILURE",
                "message": "Couldn't load the template html file",
            }

        logging.info(
            f"Sending an email with provider {self.provider.__class__.__name__}"
        )

        try:
            self.provider.send_email(
                sender=self.sender,
                recipients=self.recipients,
                subject=self.subject,
                template_text=template_text,
                template_html=template_html,
            )
        except ServiceException as e:
            logging.exception(e)
            raise e
        except Exception as e:
            logging.exception(e)
            return {
                "status": "FAILURE",
                "message": "Couldn't send email notification",
            }

        return {"status": "SUCCESS"}


class SmsNotification(Notification):
    def __init__(
        self,
        configuration_directory: str,
        sender: str,
        recipients: list,
        template_text_filename: str,
        filtering: str = None,
        image: str = None,
        provider=None,
        **kwargs,
    ):
        super().__init__(
            configuration_directory=configuration_directory,
            module_id=PIPELINE_SMS_MODULE_NAME,
            filtering=filtering,
            **kwargs,
        )

        self.sender = sender
        self.recipients = recipients
        self.template_text_filename = template_text_filename
        self.image = image

        self.provider = provider or TwilioSmsNotificationProvider(**kwargs)

    def run(self, instance: Instance, **kwargs):
        super().run(instance, **kwargs)

        if self.filtering and not self.filtering(instance):
            logging.info(
                f"The instance didn't pass the filtering criteria. Instance: {instance}"
            )
            return {"status": "SKIPPED"}

        if not hasattr(self.provider, "send_sms") or not callable(
            self.provider.send_sms
        ):
            logging.info("The specified provider is not valid")
            return {
                "status": "FAILURE",
                "message": "Specified provider is not valid",
            }

        try:
            template_text = self._load_template(instance, self.template_text_filename)
        except FileNotFoundError as e:
            logging.exception(e)
            return {
                "status": "FAILURE",
                "message": f"Template file {self.template_text_filename} not found",
            }
        except Exception as e:
            logging.exception(e)
            return {
                "status": "FAILURE",
                "message": "Couldn't load the template text file",
            }

        logging.info(f"Sending SMS with provider {self.provider.__class__.__name__}")

        image_url = instance.get_attribute(self.image, default=None)
        logging.info(f"Image included in message: {image_url}")

        try:
            self.provider.send_sms(
                sender=self.sender,
                recipients=self.recipients,
                message=template_text,
                image=image_url,
            )
        except ServiceException as e:
            logging.exception(e)
            raise e
        except Exception as e:
            logging.exception(e)
            return {
                "status": "FAILURE",
                "message": "Couldn't send sms notification",
            }

        return {"status": "SUCCESS"}


class SocketIO(Module):
    def __init__(
        self,
        pipeline_id: str,
        endpoint: str,
        event: str = "dispatch",
        **kwargs,
    ):
        super().__init__(
            pipeline_id=pipeline_id,
            **kwargs,
        )
        self.endpoint = endpoint
        self.event = event

    def run(self, instance: Instance, **kwargs):
        payload = {
            "message": "pipeline-new-instance",
            "data": instance.__dict__,
            "pipeline_id": self.pipeline_id,
        }

        self.emit(self.event, payload)

        return None

    def emit(self, event: str, payload=None):
        if not self.endpoint:
            return

        logging.info(
            f"Sending Socket IO notification to {self.endpoint}. "
            f"Namespace: {self.pipeline_id}"
        )

        payload["event"] = event
        payload["namespace"] = self.pipeline_id

        try:
            requests.post(
                url=self.endpoint,
                data=json.dumps(payload),
                headers={"Content-type": "application/json"},
            )
        except Exception:
            logging.exception("There was an error sending the socket io notification")


class TwilioSmsNotificationProvider(object):
    def __init__(self, account_sid: str = None, auth_token: str = None, **kwargs):

        self.account_sid = account_sid or os.environ.get(
            "ALIRA_TWILIO_ACCOUNT_SID", None
        )
        self.auth_token = auth_token or os.environ.get("ALIRA_TWILIO_AUTH_TOKEN", None)

        if not self.account_sid or not self.auth_token:
            raise RuntimeError("The Twilio credentials were not specified")

    def send_sms(
        self,
        sender: str,
        recipients: list,
        message: str,
        image: str = None,
        **kwargs,
    ):
        logging.info("Sending message using Twilio")

        for phone_number in recipients:
            try:
                logging.info(
                    f"Sending message to '{phone_number}': Message -> '{message}'..."
                )
                self.send_message(sender, phone_number, message, image)

            except TwilioRestException as e:
                raise ServiceException(e)

        return None

    def send_message(
        self,
        phone_number_origin: str,
        phone_number_dest: str,
        message: str,
        media_url: str = None,
    ):
        client = Client(self.account_sid, self.auth_token)
        arguments = {
            "to": phone_number_dest,
            "from_": phone_number_origin,
            "body": message,
        }

        if media_url:
            arguments["media_url"] = [media_url]

        return client.messages.create(**arguments)


class AwsSesEmailNotificationProvider(object):
    def __init__(
        self,
        aws_access_key: str = None,
        aws_secret_key: str = None,
        aws_region_name: str = None,
        **kwargs,
    ):
        self.aws_access_key = aws_access_key or os.environ.get(
            "ALIRA_AWS_ACCESS_KEY_ID", None
        )
        self.aws_secret_key = aws_secret_key or os.environ.get(
            "ALIRA_AWS_SECRET_ACCESS_KEY", None
        )
        self.aws_region_name = aws_region_name or os.environ.get(
            "ALIRA_AWS_REGION_NAME", None
        )

        if (
            not self.aws_access_key
            or not self.aws_secret_key
            or not self.aws_region_name
        ):
            raise RuntimeError("The AWS credentials were not specified")

    def send_email(
        self,
        sender: str,
        recipients: list,
        subject: str,
        template_text: str,
        template_html: str,
    ):
        payload = {
            "Destination": {"ToAddresses": recipients},
            "Message": {
                "Body": {
                    "Html": {"Charset": "UTF-8", "Data": template_html},
                    "Text": {"Charset": "UTF-8", "Data": template_text},
                },
                "Subject": {"Charset": "UTF-8", "Data": subject},
            },
            "Source": sender,
        }

        try:
            logging.info(
                (
                    "Sending an email using AWS SES Service... \n"
                    f"Sender: {sender}\n"
                    f"Recipients: {recipients}\n"
                    f"Subject: {subject}"
                )
            )

            client = boto3.client(
                "ses",
                aws_access_key_id=self.aws_access_key,
                aws_secret_access_key=self.aws_secret_key,
                region_name=self.aws_region_name,
            )

            client.send_email(**payload)

        except EndpointConnectionError as e:
            raise ServiceException(e)
