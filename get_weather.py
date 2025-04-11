import pandas as pd
import requests
import json


def get_weather_data(lat, long, start_date, end_date):

    url = "https://historical-forecast-api.open-meteo.com/v1/forecast"

    try:
        params = {    
            "latitude": lat,
            "longitude": long,
            "start_date": start_date,
            "end_date": end_date,
            "hourly": ["wind_speed_10m"]
            }
        
        response = requests.get(url=url,params=params)

        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None