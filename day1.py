user ={
    'name': 'manjunath',
    'city': 'gonioppal',
    'age': 45,
    'height': 5.8,
    'weight': 55,
    'is_married': True,
    'children': 2
}
print(f"Hello {user['name']}!")
print(f"Delivering to {user['city']}")

#instagram 
user={

    "name" : "rijesh",
"followers" : 1000,
"following" : 500,
"post" : 25
}

print(f"Hello {user['name']}!")
print(f"You have {user['followers']} followers")
print(f"You are following {user['following']} people")
print(f"You have {user['post']} posts")
from transformers import pipeline
generator = pipeline("text-generation", model="gpt2")
output = generator("ones upon the time", max_length=50)
print(output[0]["generated_text"])
import requests

TEMP_HOT_C = 35
TEMP_COLD_C = 5
WIND_STRONG_KMH = 50
HUMID_LOW = 20
HUMID_HIGH = 80
RAIN_MM = 1


#climate 
def get_coordinates(city: str):
    """Convert a city name to latitude/longitude using Open-Meteo's geocoding API."""
    geo_url = "https://geocoding-api.open-meteo.com/v1/search"
    resp = requests.get(geo_url, params={"name": city, "count": 1}, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    if not data.get("results"):
        raise ValueError(f"City '{city}' not found.")
    r = data["results"][0]
    return r["latitude"], r["longitude"], r.get("name"), r.get("country")


def fetch_climate(lat: float, lon: float) -> dict:
    """Fetch current climate data for the given coordinates."""
    weather_url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": ",".join([
            "temperature_2m",
            "relative_humidity_2m",
            "apparent_temperature",
            "is_day",
            "precipitation",
            "rain",
            "wind_speed_10m",
            "wind_direction_10m",
            "weather_code",
        ]),
        "timezone": "auto",
    }
    resp = requests.get(weather_url, params=params, timeout=10)
    resp.raise_for_status()
    return resp.json()


WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Fog", 48: "Depositing rime fog",
    51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
    61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
    71: "Slight snow", 73: "Moderate snow", 75: "Heavy snow",
    80: "Slight rain showers", 81: "Moderate rain showers", 82: "Violent rain showers",
    95: "Thunderstorm", 96: "Thunderstorm w/ slight hail", 99: "Thunderstorm w/ heavy hail",
}


def describe_weather(code: int) -> str:
    return WEATHER_CODES.get(code, f"Unknown (code {code})")


def evaluate_alerts(c: dict) -> list:
    """Return a list of human-readable climate alerts based on thresholds."""
    alerts = []
    if c["temperature_2m"] >= TEMP_HOT_C:
        alerts.append(f"🔥 HEAT ALERT: {c['temperature_2m']}°C >= {TEMP_HOT_C}°C")
    if c["temperature_2m"] <= TEMP_COLD_C:
        alerts.append(f"🥶 COLD ALERT: {c['temperature_2m']}°C <= {TEMP_COLD_C}°C")
    if c["wind_speed_10m"] >= WIND_STRONG_KMH:
        alerts.append(f"💨 WIND ALERT: {c['wind_speed_10m']} km/h")
    if c["relative_humidity_2m"] <= HUMID_LOW:
        alerts.append(f"🏜️  DRY ALERT: humidity {c['relative_humidity_2m']}%")
    if c["relative_humidity_2m"] >= HUMID_HIGH:
        alerts.append(f"💧 HUMID ALERT: humidity {c['relative_humidity_2m']}%")
    if c.get("rain", 0) >= RAIN_MM or c.get("precipitation", 0) >= RAIN_MM:
        rain = c.get("rain", c.get("precipitation", 0))
        alerts.append(f"🌧️  RAIN ALERT: {rain} mm")
    return alerts


def check_climate(city: str) -> None:
    lat, lon, name, country = get_coordinates(city)
    data = fetch_climate(lat, lon)
    c = data["current"]

    print("=" * 56)
    print(f"📍  {name}, {country}  ({lat:.3f}, {lon:.3f})")
    print(f"🕒  {c['time']}  ({data.get('timezone', 'local')})")
    print("=" * 56)
    print(f"🌡️  Temperature  : {c['temperature_2m']} °C  (feels like {c['apparent_temperature']} °C)")
    print(f"☁️  Condition    : {describe_weather(c['weather_code'])}")
    print(f"💧  Humidity     : {c['relative_humidity_2m']} %")
    print(f"🌬️  Wind         : {c['wind_speed_10m']} km/h  @ {c['wind_direction_10m']}°")
    print(f"🌧️  Precipitation: {c.get('precipitation', 0)} mm  (rain: {c.get('rain', 0)} mm)")
    print("-" * 56)

    alerts = evaluate_alerts(c)
    if alerts:
        print("⚠️  ALERTS:")
        for a in alerts:
            print("   -", a)
    else:
        print("✅  Climate conditions are within normal thresholds.")
    print("=" * 56)


def main() -> None:
    city = input("Enter a city name (e.g. London, Tokyo, New York): ").strip()
    if not city:
        print("No city provided. Exiting.")
        return
    try:
        check_climate(city)
    except requests.RequestException as e:
        print(f"Network error: {e}")
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()