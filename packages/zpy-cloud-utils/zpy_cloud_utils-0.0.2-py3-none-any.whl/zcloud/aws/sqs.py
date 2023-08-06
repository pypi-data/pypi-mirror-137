from typing import Union
import boto3


class SQS:
    queue_name = None
    sqs_client = None
    queue_object = None
    global_initialized: bool = False

    def __init__(self, queue_url: str = None) -> None:
        self.sqs_client = boto3.client("sqs")
        if queue_url is not None:
            self.queue_name = queue_url
            # self.__sqs_initializer(name=queue_url, is_global=True)

    def __sqs_initializer(self, name: str = None, is_global: bool = False):
        sqs_name = self.__validate(name=name)
        sqs_object = self.sqs_client.get_queue_by_name(QueueName=sqs_name)
        if is_global:
            self.queue_name = sqs_name
            self.queue_object = sqs_object
            self.global_initialized = True
            return self.queue_object
        return sqs_object

    def __validate(self, name: str = None) -> Union[str, None]:
        """
        Validate sqs name and return sqs object acording name
        """
        real_name = self.queue_name if name is None else name
        if real_name is None:
            raise Exception("SQS Name didn't provide")
        return real_name

    def send(self, msg: str, queue_url: str = None, attributes: dict = {}):
        real_url = self.queue_name if queue_url is None else queue_url
        if real_url is None:
            raise Exception("SQS URL didn't provided")
        response = self.sqs_client.send_message(
            QueueUrl=queue_url,
            DelaySeconds=0,
            MessageAttributes=attributes,
            MessageBody=msg,
        )
        return response

    def __send_message(self, msg: str, queue_url: str = None):
        """
        Send MESSAGE to SQS
        IN DEVELOP STAGE
        """
        client = self.__sqs_initializer(queue_url)
