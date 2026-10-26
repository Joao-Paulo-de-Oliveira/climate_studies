import unittest
from unittest.mock import patch
import requests
from get_weather import get_weather_data


class WeatherCollectorTests(unittest.TestCase):
    @patch("get_weather.requests.get")
    def test_success_and_query(self, get):
        payload = {"hourly": {"wind_speed_10m": [8.1]}}
        get.return_value.json.return_value = payload
        self.assertEqual(get_weather_data(-19.75, -43.91, "2024-04-09", "2024-04-09"), payload)
        get.return_value.raise_for_status.assert_called_once_with()
        self.assertEqual(get.call_args.kwargs["timeout"], 30)
        self.assertEqual(get.call_args.kwargs["params"], {
            "latitude": -19.75, "longitude": -43.91,
            "start_date": "2024-04-09", "end_date": "2024-04-09",
            "hourly": ["wind_speed_10m"],
        })

    @patch("get_weather.requests.get")
    def test_timeout(self, get):
        get.side_effect = requests.exceptions.Timeout("simulated")
        with patch("builtins.print"):
            self.assertIsNone(get_weather_data(0, 0, "2024-04-09", "2024-04-09"))

    @patch("get_weather.requests.get")
    def test_http_error(self, get):
        get.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError("simulated")
        with patch("builtins.print"):
            self.assertIsNone(get_weather_data(0, 0, "2024-04-09", "2024-04-09"))
        get.return_value.json.assert_not_called()
