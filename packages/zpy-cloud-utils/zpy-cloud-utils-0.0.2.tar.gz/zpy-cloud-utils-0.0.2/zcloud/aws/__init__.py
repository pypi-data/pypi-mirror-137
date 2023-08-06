
from enum import Enum


__author__ = "Noé Cruz | contactozurckz@gmail.com"
__copyright__ = "Copyright 2021, Small APi Project"
__credits__ = ["Noé Cruz", "Zurck'z"]
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "Noé Cruz"
__email__ = "contactozurckz@gmail.com"
__status__ = "Dev"

AWS_DEFAULT_REGION = "us-east-1"
AWS_DNS = "https://s3.amazonaws.com/"


class AWSCredentials:
    def __init__(self, ak: str, sk: str, st: str = "", region: str = AWS_DEFAULT_REGION) -> None:
        self.access_key = ak
        self.secret_key = sk
        self.session_token = st
        self.region = region


class CredentialsMode(Enum):
    PROFILE = 1
    CREDENTIALS = 2