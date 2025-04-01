# Care Python SDK

This is an experimental Python SDK for WAKU Care's MQTT API.
The MQTT API is documented [here](https://docs.waku-robotics.com/#/)

In Order to use this SDK, you need to acquire WAKU Care MQTT login credentials.
Please contact the WAKU Care team for details on how to do that.

## Installation

First, clone this repository: `git clone git@github.com:wakurobotics/schema.py.git`.
Then cd into schema.py and run `pip3 install -e .` to install the package.

## Usage

Basic usage and import.

```python
# Create the WAKU Care client
from wakurobotics.care import Client

publisher = Client(
    customer_id=<YOUR_CUSTOMER_ID>,
    connection_id=<YOUR_CONNECTION_ID>,
    broker=<CARE_MQTT_HOST>,
    port=8883,
    username=<YOUR_MQTT_USER>,
    password=<YOUR_MQTT_PASSWORD>
)

# Connect to broker
publisher.connect()

# send data

# Disconnect after sending
publisher.disconnect()

```

See the examples directory containing a sample WAKU Care client to send weather data, gathered from [api.open-meteo.com](api.open-meteo.com).
