
import time
import requests

print("Welcome to AAJ KA MAUSAM")
time.sleep(1)

def get_location(city):
    response = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={"name": city},
        timeout=10
    )
    response.raise_for_status()

    location_data = response.json()
    results = location_data.get("results")

    if not results:
        return None

    location = results[0]
    latitude = location["latitude"]
    longitude = location["longitude"]

    return latitude, longitude


def get_weather(latitude, longitude):
    response = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,relative_humidity_2m,wind_speed_10m"
        },
        timeout=10
    )
    response.raise_for_status()

    weather_data = response.json()
    current = weather_data["current"]

    temperature = current["temperature_2m"]
    humidity = current["relative_humidity_2m"]
    wind = current["wind_speed_10m"]

    return temperature, humidity, wind


city = input("Enter the city name: ").strip()

if not city:
    print("Please enter a city name.")

else:
    try:
        location = get_location(city)

        if location is None:
            print("City not found. Please check the spelling.")

        else:
            latitude, longitude = location

            temperature, humidity, wind = get_weather(
                latitude, longitude
            )

            print("\n====================")
            print("    AAJ KA MAUSAM")
            print("====================")
            print("City:", city.title())
            print("Temperature:", temperature, "°C")
            print("Humidity:", humidity, "%")
            print("Wind speed:", wind, "km/h")
            print("====================")

    except requests.RequestException:
        print("Could not connect to the weather service.")
        print("Please check your internet connection and try again.")

    except (KeyError, ValueError):
        print("The weather service returned unexpected data.")
        print("Please try again later.")