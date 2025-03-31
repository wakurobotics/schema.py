import json
import paho.mqtt.client as mqtt
from wakurobotics.care.devices.v1 import DeviceValues, DeviceFactsheet

VERSION = "v1"

class Client:
    def __init__(self, customer_id: str, connection_id: str, broker: str, port: int = 8883, username: str = None, password: str = None):
        self.client = mqtt.Client(client_id=f"python-care-client-{customer_id}-{connection_id}", protocol=mqtt.MQTTv5 )
        # care uses mqtt over tls
        self.client.tls_set()
        self.broker = broker
        self.port = port
        self.customer_id = customer_id
        self.connection_id = connection_id
        self.username = username
        self.password = password
        

    def connect(self):
        """Connect to the MQTT broker."""
        if self.username and self.password:
            self.client.username_pw_set(self.username, self.password)
                    
        self.client.connect(self.broker, self.port)
        self.client.loop_start()


    def register_device(self, serial: str, device_values: DeviceFactsheet):
        """
        Publish a validated DeviceFactsheet message.

        :param message: MQTTMessage (Pydantic model)
        """
        topic = f"{VERSION}/{self.connection_id}/{self.customer_id}/{serial}/factsheet"
        payload = device_values.model_dump_json()

        self.client.publish(topic, payload)
        print(f"Published to {topic}: {payload}")


    def publish_device_values(self, serial: str, device_values: DeviceValues):
        """
        Publish a validated DeviceValues message.

        :param message: MQTTMessage (Pydantic model)
        """
        topic = f"{VERSION}/{self.connection_id}/{self.customer_id}/{serial}/values"
        payload = device_values.model_dump_json()

        self.client.publish(topic, payload)
        print(f"Published to {topic}: {payload}")
        

    def disconnect(self):
        """Disconnect from the MQTT broker."""
        self.client.loop_stop()
        self.client.disconnect()
