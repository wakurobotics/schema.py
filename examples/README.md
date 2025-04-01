# WAKU Care SDK Openapi Weather Client

This code queries the weather for Dresden and Florence (because Dresden is called the ['Florence of the Elbe'](https://en.wikipedia.org/wiki/Dresden#:~:text=With%20a%20pleasant%20location%20and,(Florence%20on%20the%20Elbe))) every second from [api.openmetor.com](https://api.open-meteo.com/).

You can use the [API](https://api.open-meteo.com/v1/forecast?latitude=51.0504&longitude=13.7373&current=temperature_2m,wind_speed_10m,wind_direction_10m,surface_pressure) for yourself to see what it will return:

```json
{
  "latitude": 51.06,
  "longitude": 13.74,
  "generationtime_ms": 0.0396966934204102,
  "utc_offset_seconds": 0,
  "timezone": "GMT",
  "timezone_abbreviation": "GMT",
  "elevation": 115,
  "current_units": {
    "time": "iso8601",
    "interval": "seconds",
    "temperature_2m": "°C",
    "wind_speed_10m": "km/h",
    "wind_direction_10m": "°",
    "surface_pressure": "hPa"
  },
  "current": {
    "time": "2025-04-01T10:15",
    "interval": 900,
    "temperature_2m": 9.9,
    "wind_speed_10m": 10.2,
    "wind_direction_10m": 51,
    "surface_pressure": 1013.8
  }
}
```

The script parses these values and sends them via the `values` topic to WAKU Care.
This script will also register devices (aka "weather stations") in WAKU Care.
In reality, these devices could be wind turbines and the measurements, provided by openmeteor would be sensor readings on that turbine.

To run this script, run:

```bash
MQTT_HOST=<WAKU_CARE_MQTT_HOST> MQTT_PORT=8883 MQTT_USER=<YOUR_USER_NAME> MQTT_PASS=<YOUR_USER_PASSWORD> python3 examples/weather.py --connection-id=<YOUR_CONNECTOR_ID> --customer-id=<YOUR_CUSTOMER_ID>
```

Currently, All the values in `<>` will be provided by the WAKU Care Team directly and are not available anywhere in the WAKU Care app.
