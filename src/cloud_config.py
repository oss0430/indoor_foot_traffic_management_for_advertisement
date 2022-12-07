import json
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient


class AWSMQTTConfig():

    def __init__(
        self,
        thing_name = None,
        host_name = None,
        root_ca_path = None,
        private_key_path = None,
        cert_file_path = None,
        disconnection_timeout : int = 10,
        mqtt_operation_timeout : int = 5
    ):

        self.thing_name = thing_name
        self.host_name = host_name
        self.root_ca_path = root_ca_path
        self.private_key_path = private_key_path
        self.cert_file_path = cert_file_path
        self.disconnection_timeout = disconnection_timeout
        self.mqtt_operation_timeout = mqtt_operation_timeout


    def read_config_json(
        self,
        path
    ):
        json_file = open(path)

        aws_data_dict = json.load(json_file)

        self.thing_name = aws_data_dict['Thing_Name']
        self.host_name = aws_data_dict['Host_Name']
        self.root_ca_path = aws_data_dict['Root_CA']
        self.private_key_path = aws_data_dict['Private_Key']
        self.cert_file_path = aws_data_dict['Cert_File']



    def to_dict(
        self
    ):

        return {
            'thing_name': self.thing_name,
            'host_name': self.host_name,
            'root_ca_path': self.root_ca_path,
            'private_key_path': self.private_key_path,
            'cert_file_path': self.cert_file_path,
            'disconnection_timeout': self.disconnection_timeout,
            'mqtt_operation_timeout': self.mqtt_operation_timeout
        }
