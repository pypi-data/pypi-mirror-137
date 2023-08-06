import json
from botocore.exceptions import ClientError
import boto3
from typing import Any, Dict
from . import AWSCredentials, CredentialsMode, AWS_DEFAULT_REGION


class S3:
    initialized: bool = False
    s3_client = None
    with_profile: bool = True

    def __init__(
            self,
            credentials: AWSCredentials = None,
            bucket: str = None,
            initialize: bool = False,
            with_profile: bool = True,
    ) -> None:
        self.credentials = credentials
        self.bucket = bucket
        self.with_profile = with_profile
        if initialize:
            self.__init_client(credentials, with_profile)

    def set_credentials_mode(self, mode: CredentialsMode):
        if mode == CredentialsMode.CREDENTIALS:
            self.with_profile = False
            return True
        self.with_profile = True
        return True

    def __init_client(self, credentials: AWSCredentials, profile: bool = True):
        if credentials is None and profile == False:
            raise Exception("Credentials didn't provided")
        if credentials is not None and profile == False:
            self.s3_client = boto3.client(
                "s3",
                aws_access_key_id=credentials.access_key,
                aws_secret_access_key=credentials.secret_key,
                # aws_session_token=credentials.session_token,
                region_name=AWS_DEFAULT_REGION,
            )
        else:
            self.s3_client = boto3.client(
                "s3",
                region_name=AWS_DEFAULT_REGION,
            )
        self.initialized = True

    def get(
            self, full_key: str, bucket: str = None, credentials: AWSCredentials = None
    ) -> Any:
        """
        Get object from s3 bucket
        """
        real_bucket = self.__validate(bucket, credentials)
        s3_object = self.s3_client.get_object(Bucket=real_bucket, Key=full_key)
        content = s3_object["Body"].read()
        return content

    def download(
            self,
            full_key: str,
            bucket: str,
            local_file: str,
            credentials: AWSCredentials = None,
    ) -> Any:
        """
        Get object from s3 bucket
        """
        real_bucket = self.__validate(bucket, credentials)
        self.s3_client.download_file(real_bucket, full_key, local_file)
        return True

    def get_json(
            self, full_key: str, bucket: str = None, credentials: AWSCredentials = None
    ):
        json_obj = self.get(full_key, bucket, credentials)
        return json.loads(json_obj.decode("utf-8"))

    def put(
            self,
            object_value: Any,
            full_key: str,
            bucket: str = None,
            credentials: AWSCredentials = None,
    ) -> Any:
        """
        Put object from s3 bucket
        """
        real_bucket = self.__validate(bucket, credentials)
        result = self.s3_client.put_object(Body=object_value, Bucket=real_bucket, Key=full_key)
        return result

    def put_json(
            self,
            json_object: Dict,
            full_key: str,
            bucket: str = None,
            credentials: AWSCredentials = None,
    ):
        """
        Upload JSON|DICT object to S3

        Parameters
        ----------
        json_object : dict
            The dict json to upload s3
        full_key : str
            The file name
        bucket : str, optional
            Bucket name
        """
        json_parsed = str(json.dumps(json_object))
        return self.put(json_parsed, full_key, bucket, credentials)

    def upload(
            self,
            object_up: Any,
            object_name: str,
            bucket: str = None,
            credentials: AWSCredentials = None,
    ) -> bool:
        try:
            real_bucket = self.__validate(bucket, credentials)
            response = self.s3_client.upload_fileobj(
                object_up, real_bucket, object_name
            )
            return response
        except ClientError as e:
            print(e)
            return None

    def __validate(self, bucket: str = None, credentials: AWSCredentials = None) -> str:
        """
        Vrify aws credentials
        """
        real_bucket = self.bucket if bucket is None else bucket
        if real_bucket is None:
            raise Exception("Bucket didn't provided")
        if self.initialized is False:
            self.__init_client(self.credentials if credentials is None else credentials)
        return real_bucket
