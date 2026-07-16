import requests

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"

def execute(arguments: dict):
    """
    Returns location details for a given city.
    """

    city = arguments.get("city")

    if not city:
        return "Location Error: City is required."

    try:
        response = requests.get(
            GEOCODING_URL,
            params={
                "name": city,
                "count": 1
            },
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        if "results" not in data:
            return "City not found."

        location = data["results"][0]

        return (
            f"📍 City: {location['name']}\n"
            f"🌍 Country: {location.get('country', 'N/A')}\n"
            f"🏛 State: {location.get('admin1', 'N/A')}\n"
            f"🧭 Latitude: {location['latitude']}\n"
            f"🧭 Longitude: {location['longitude']}\n"
            f"📏 Elevation: {location.get('elevation', 'N/A')} m"
        )

    except Exception as e:
        return f"Location Error: {e}"


if __name__ == "__main__":
    print(
        execute(
            {
                "city": "Delhi"
            }
        )
    )