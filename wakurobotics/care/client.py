import paho.mqtt.client as mqtt
from wakurobotics.care.devices.v1 import DeviceValues, DeviceFactsheet, Connection, ConnectionStatus
from datetime import datetime

VERSION = "v1"

def get_timestamp():
    return datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')

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
        
        # subscribe to WAKU Care errorlog topic
        def on_message(client, userdata, msg):
            print(f"Received error message from WAKU Care: `{msg.payload.decode()}` from `{msg.topic}` topic")

        self.client.subscribe(f"{VERSION}/{self.connection_id}/errorlog")
        self.client.on_message = on_message
        self.client.loop_start()

    def connect_device(self, serial: str):
        """
        Publish a validated DeviceFactsheet message.

        :param message: MQTTMessage (Pydantic model)
        """
        topic = f"{VERSION}/{self.connection_id}/{self.customer_id}/{serial}/connection"
        payload = Connection(
            status=ConnectionStatus.online,
            timestamp=get_timestamp()
        ).model_dump_json()

        return self.client.publish(topic, payload, qos=1, retain=True)
    
    def disconnect_device(self, serial: str):
        """
        Publish a validated DeviceFactsheet message.
        """
        topic = f"{VERSION}/{self.connection_id}/{self.customer_id}/{serial}/connection"
        payload = Connection(
            status=ConnectionStatus.offline,
            timestamp=get_timestamp()
        ).model_dump_json()

        return self.client.publish(topic, payload, qos=1, retain=True)

    def register_device(self, serial: str, device_values: DeviceFactsheet):
        """
        Publish a validated DeviceFactsheet message.

        :param message: MQTTMessage (Pydantic model)
        """
        topic = f"{VERSION}/{self.connection_id}/{self.customer_id}/{serial}/factsheet"
        payload = device_values.model_dump_json()

        return self.client.publish(topic, payload, qos=1, retain=True)

    def publish_device_values(self, serial: str, device_values: DeviceValues):
        """
        Publish a validated DeviceValues message.

        :param message: MQTTMessage (Pydantic model)
        """
        topic = f"{VERSION}/{self.connection_id}/{self.customer_id}/{serial}/values"
        payload = device_values.model_dump_json()

        return self.client.publish(topic, payload, qos=0, retain=False)

    def disconnect(self):
        """Disconnect from the MQTT broker."""
        self.client.loop_stop()
        return self.client.disconnect()
