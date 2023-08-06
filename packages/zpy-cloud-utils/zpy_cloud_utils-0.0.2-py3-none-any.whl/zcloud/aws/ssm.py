from typing import Dict, Union
from zpy.utils.objects import ZObjectModel
from zcloud.aws import AWSCredentials, AWS_DEFAULT_REGION
import boto3
import json

__author__ = "Noé Cruz | contactozurckz@gmail.com"
__copyright__ = "Copyright 2021, Small APi Project"
__credits__ = ["Noé Cruz", "Zurck'z"]
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "Noé Cruz"
__email__ = "contactozurckz@gmail.com"
__status__ = "Dev"


class SSMParameter:
    ssm_client = None
    with_profile: bool = False
    store = {}
    prefix: str = None

    def __init__(
            self,
            credentials: AWSCredentials = None,
            with_profile: bool = True,
            prefix: str = None,
    ) -> None:
        self.with_profile = with_profile
        self.prefix = prefix
        if with_profile or credentials is None:
            self.ssm = boto3.client("ssm", region_name=AWS_DEFAULT_REGION)
        else:
            self.ssm = boto3.client(
                "ssm",
                aws_access_key_id=credentials.access_key,
                aws_secret_access_key=credentials.secret_key,
                region_name=credentials.region,
            )

    def get_from_cache(self, name: str, model: ZObjectModel = None) -> Union[Dict, ZObjectModel]:
        """
        Get parameter stored in cache.
        """
        if name not in self.store:
            return None
        data = self.store[name]
        if model == None:
            return data
        return model(**data)

    def get(
            self,
            prefix: str = None,
            decryption: bool = True,
            store: bool = False,
            store_name: str = "",
            model: ZObjectModel = None,
            refresh: bool = False,
    ) -> Union[Dict, ZObjectModel]:
        """
        Get paramater from AWS SSM
        """
        if store_name in self.store and refresh is False:
            data = self.store[store_name]
            if model is not None:
                return model(**data)
            return data

        if prefix is None and self.prefix is None:
            raise Exception("Prefix or parameter name didnt provided.")
        real_path = prefix or ""
        if self.prefix is not None:
            real_path = f"{self.prefix}{real_path}"
        parameter = self.ssm.get_parameter(Name=real_path, WithDecryption=decryption)
        if store and store_name:
            self.store[store_name] = json.loads(parameter["Parameter"]["Value"])
        if model is None:
            return json.loads(parameter["Parameter"]["Value"])
        return model(**json.loads(parameter["Parameter"]["Value"]))
