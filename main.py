from wakurobotics.care import Client
from wakurobotics.care.devices.v1.values_schema import DeviceValues
from wakurobotics.care.devices.v1.shared.value_schema import ScalarValue
from datetime import datetime
import argparse
import os
import time

# Get MQTT credentials from environment variables with defaults
MQTT_HOST = os.getenv('MQTT_HOST', 'care-dev.waku-robotics.com')
MQTT_PORT = os.getenv('MQTT_PORT', 8883)
MQTT_USER = os.getenv('MQTT_USER')
MQTT_PASS = os.getenv('MQTT_PASS')

# Parse command line arguments
parser = argparse.ArgumentParser(description='Publish device values to WAKU Care MQTT API')
parser.add_argument('--connection-id', required=True, help='Connection ID')
parser.add_argument('--customer-id', required=True, help='Customer ID')
parser.add_argument('--serial', required=True, help='Device serial number')

args = parser.parse_args()

# Add credential verification
if not MQTT_USER or not MQTT_PASS:
    raise ValueError("MQTT_USER and MQTT_PASS environment variables must be set")

print(f"Connecting to {MQTT_HOST}:{MQTT_PORT} with user {MQTT_USER}")

# Create MQTT Publisher
publisher = Client(customer_id=args.customer_id, connection_id=args.connection_id, broker=MQTT_HOST, port=int(MQTT_PORT), username=MQTT_USER, password=MQTT_PASS)  # Free test broker

# Connect to broker
publisher.connect()

# Create a valid message
message = DeviceValues(
        timestamp=datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'),
        values=[
            ScalarValue(
                name="temperature",
                value=23.5,
                unit="c"
            ),
            ScalarValue(
                name="windspeed",
                value=60.0,
                unit="kph"
            )
        ]
    )

# Publish the message - note the additional required parameters
publisher.publish_device_values(
    serial=args.serial,
    device_values=message
)

# Disconnect after sending
publisher.disconnect()
