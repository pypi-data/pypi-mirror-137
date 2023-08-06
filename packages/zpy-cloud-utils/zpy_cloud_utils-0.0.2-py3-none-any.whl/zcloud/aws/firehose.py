from typing import Any, Dict, List
from zcloud.aws import AWSCredentials, AWS_DEFAULT_REGION
import boto3
import json


class Firehose:
    fh_client = None
    with_profile: bool = False

    def __init__(
            self,
            credentials: AWSCredentials = None,
            with_profile: bool = True,
    ) -> None:
        self.with_profile = with_profile
        if with_profile or credentials is None:
            self.fh_client = boto3.client("firehose", region_name=AWS_DEFAULT_REGION)
        else:
            self.fh_client = boto3.client(
                "firehose",
                aws_access_key_id=credentials.access_key,
                aws_secret_access_key=credentials.secret_key,
                region_name=credentials.region,
            )

    def send_data_record(self, data: dict, stream_name: str):
        """
        Put one record to delivery stream
        """
        try:
            response = self.fh_client.put_record(
                DeliveryStreamName=stream_name, Record=self.__prepare_record(data)
            )
            return response
        except Exception as e:
            print(e)
            return None

    def __prepare_record(self, data: Dict) -> Dict:
        dumped = json.dumps(data)
        encoded = dumped.encode("utf-8")
        return {"Data": encoded}

    def send_batch_data(self, data: List[Dict[Any, Any]], stream_name: str):
        """
        Put one record to delivery stream
        :data List of record to send firehouse
        """
        try:
            records = list(map(self.__prepare_record, data))
            response = self.fh_client.put_record_batch(
                DeliveryStreamName=stream_name, Records=records
            )
            return response
        except Exception as e:
            print(e)
            return None

    def describe_stream(
            self, stream_name: str, limit: int = 123, start_id: str = None
    ) -> dict:
        try:
            response = self.fh_client.describe_delivery_stream(
                DeliveryStreamName=stream_name,
                Limit=limit,
                ExclusiveStartDestinationId=start_id,
            )
            return response
        except Exception as e:
            print(e)
            return None
