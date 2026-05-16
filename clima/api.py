from . import utils
import openmeteo_requests
import requests_cache
from retry_requests import retry
import numpy
def get_data(request,lat,long):
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)
    url="https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": long,
        "hourly": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "precipitation_probability",
                    "rain", "cloud_cover", "wind_speed_10m"],
        "timezone": "auto",
        "start_date": str(request.POST.get("date_event")),
        "end_date": str(request.POST.get("date_event")),
    }
    responses=openmeteo.weather_api(url,params=params)
    response=responses[0]
    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
    hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()
    hourly_apparent_temperature = hourly.Variables(2).ValuesAsNumpy()
    hourly_precipitation_probability = hourly.Variables(3).ValuesAsNumpy()
    hourly_rain = hourly.Variables(4).ValuesAsNumpy()
    hourly_cloud_cover = hourly.Variables(5).ValuesAsNumpy()
    hourly_wind_speed_10m = hourly.Variables(6).ValuesAsNumpy()
    list_variables=[hourly.Variables(0).ValuesAsNumpy(),hourly.Variables(1).ValuesAsNumpy(),hourly.Variables(2).ValuesAsNumpy(),
                    hourly.Variables(3).ValuesAsNumpy(),hourly.Variables(4).ValuesAsNumpy(),hourly.Variables(5).ValuesAsNumpy(),
                    hourly.Variables(6).ValuesAsNumpy()]
    return list_variables