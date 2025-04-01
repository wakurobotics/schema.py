from wakurobotics.care import Client, get_timestamp
from wakurobotics.care.devices.v1.values_schema import DeviceValues
from wakurobotics.care.devices.v1.shared.value_schema import ScalarValue, Unit as ScalarValueUnit
from wakurobotics.care.devices.v1.factsheet_schema import DeviceFactsheet
import argparse
import os
import time
import requests


TEMPERATURE = "temperature_2m"
WIND_SPEED = "wind_speed_10m"
WIND_DIRECTION = "wind_direction_10m"
SURFACE_PRESSURE = "surface_pressure"

DRESDEN_LAT = 51.0504
DRESDEN_LON = 13.7373

FLORENCE_LAT = 43.7696
FLORENCE_LON = 11.2558

def get_weather_data(lat: float, lon: float):
    features = f"{TEMPERATURE},{WIND_SPEED},{WIND_DIRECTION},{SURFACE_PRESSURE}"
    
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current={features}"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to retrieve weather data.")
        return None    
    
def weather_data_to_care_message(weather_data: dict):
    interval = weather_data['current']['interval']
    temperature = weather_data['current'][TEMPERATURE]
    wind_speed = weather_data['current'][WIND_SPEED]
    wind_direction = weather_data['current'][WIND_DIRECTION]
    surface_pressure = weather_data['current'][SURFACE_PRESSURE]
    
    print(f"Temperature: {temperature}C, Wind Speed: {wind_speed}kph, Surface Pressure: {surface_pressure}hpa")
    
    # Create a valid message
    message = DeviceValues(
            timestamp=get_timestamp(),
            interval=interval,
            values=[
                ScalarValue(
                    name="temperature-every-15-minutes",
                    value=temperature,
                    # API returns temperature in celsius
                    unit=ScalarValueUnit.c
                ),
                ScalarValue(
                    name="windspeed-every-15-minutes",
                    value=wind_speed,
                    # API returns wind speed in km/h
                    unit=ScalarValueUnit.kph
                ),
                ScalarValue(
                    name="winddirection-every-15-minutes",
                    value=wind_direction,
                    # API returns wind direction in degrees
                    unit=ScalarValueUnit.deg
                ),
                ScalarValue(
                    name="pressure-every-15-minutes",
                    value=surface_pressure,
                    # API returns surface pressure in hPa
                    unit=ScalarValueUnit.hpa
                )
            ]
        )

    return message
    
# Get MQTT credentials from environment variables with defaults
MQTT_HOST = os.getenv('MQTT_HOST')
MQTT_PORT = os.getenv('MQTT_PORT')
MQTT_USER = os.getenv('MQTT_USER')
MQTT_PASS = os.getenv('MQTT_PASS')

# Parse command line arguments
parser = argparse.ArgumentParser(description='Publish device values to WAKU Care MQTT API')
parser.add_argument('--connection-id', required=True, help='Connection ID')
parser.add_argument('--customer-id', required=True, help='Customer ID')

args = parser.parse_args()

# Add credential verification
if not MQTT_USER or not MQTT_PASS:
    raise ValueError("MQTT_USER and MQTT_PASS environment variables must be set")

print(f"Connecting to {MQTT_HOST}:{MQTT_PORT} with user {MQTT_USER}")

# Create the WAKU Care client
publisher = Client(customer_id=args.customer_id, connection_id=args.connection_id, broker=MQTT_HOST, port=int(MQTT_PORT), username=MQTT_USER, password=MQTT_PASS)

# Connect to broker
publisher.connect()

# within our connection we would like to identify this device by this serial number
DRESDEN_SERIAL = "DRESDEN-001"
# within our connection we would like to identify this device by this serial number
FLORENCE_SERIAL = "FLORENCE-001"

# First register a device
publisher.register_device(
    serial=DRESDEN_SERIAL,
    device_values=DeviceFactsheet(
        # this is the unique serial number from the manufacturer of this device
        # it is NOT the serial number we use within our connection
        serial='11111111',
        name="Dresden Weather Station",
        manufacturer="default",
        model="default",
        version="1.0.0",
        deployment="Logistics AG (Demo)",
    )
)

# You can register more devices within the same connection
publisher.register_device(
    serial=FLORENCE_SERIAL,
    device_values=DeviceFactsheet(
        # this is the unique serial number from the manufacturer of this device
        # it is NOT the serial number we use within our connection
        serial='22222222',
        name="Florence Weather Station",
        manufacturer="default",
        model="default",
        version="1.0.0",
        deployment="Logistics AG (Demo)",
    )
)

# Connect the devices
publisher.connect_device(serial=DRESDEN_SERIAL)
publisher.connect_device(serial=FLORENCE_SERIAL)

try:
    while True:
        weather_data_dd = get_weather_data(DRESDEN_LAT, DRESDEN_LON)
        weather_data_fl = get_weather_data(FLORENCE_LAT, FLORENCE_LON)

        message_dd = weather_data_to_care_message(weather_data_dd)
        message_fl = weather_data_to_care_message(weather_data_fl)

        # Publish the message - note the additional required parameters
        publisher.publish_device_values(
            serial=DRESDEN_SERIAL,
            device_values=message_dd
        )
        publisher.publish_device_values(
            serial=FLORENCE_SERIAL,
            device_values=message_fl
        )

        time.sleep(1)
except KeyboardInterrupt:
    # Disconnect the devices
    publisher.disconnect_device(serial=DRESDEN_SERIAL)
    publisher.disconnect_device(serial=FLORENCE_SERIAL)

    # Disconnect after sending
    publisher.disconnect()


