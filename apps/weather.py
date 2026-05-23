import subprocess
import json

class WeatherManager:
    def __init__(self, location="Swansea"):
        self.location = location
        self.data = {}
        
    def refresh(self):    
        result = subprocess.run(
            ["curl", "-s", f"wttr.in/{self.location}?format=j1"],
            capture_output=True,
            encoding="utf-8",
            text=True,
            timeout=10            
        )
            
        if result.returncode != 0:
            self.data = {"error": result.stderr.strip()}
            return self.data

        raw = json.loads(result.stdout)
        current = raw["current_condition"][0]
        today = raw["weather"][0]
        tomorrow = raw["weather"][1]
        day_after = raw["weather"][2]
        area = raw["nearest_area"][0]
        
        self.data = {
            "location": area["areaName"][0]["value"],
            "lat": area["latitude"],
            "long": area["longitude"],
            "condition": current["weatherDesc"][0]["value"],
            "temp_c": current["temp_C"],
            "feels_like_c": current["FeelsLikeC"],
            "humidity": current["humidity"],
            "wind_mph": current["windspeedMiles"],
            "wind_dir": current["winddir16Point"],
            "pressure": current["pressure"],
            "visibility": current["visibility"],
            "uv_index": current["uvIndex"],
            
            "today_max_c": today["maxtempC"],
            "today_avg_c": today["avgtempC"],
            "today_min_c": today["mintempC"],
            "today_uv": today["uvIndex"],
            "today_date": today["date"],
            "today_moon_ill": today["astronomy"][0]["moon_illumination"],
            "today_sunrise": today["astronomy"][0]["sunrise"],
            "today_sunset": today["astronomy"][0]["sunset"],
            
            "today_00_temp": today["hourly"][0]["tempC"],
            "today_03_temp": today["hourly"][1]["tempC"],
            "today_06_temp": today["hourly"][2]["tempC"],
            "today_09_temp": today["hourly"][3]["tempC"],
            "today_12_temp": today["hourly"][4]["tempC"],
            "today_15_temp": today["hourly"][5]["tempC"],
            "today_18_temp": today["hourly"][6]["tempC"],
            "today_21_temp": today["hourly"][7]["tempC"],
            
            "today_00_rain": today["hourly"][0]["chanceofrain"],
            "today_03_rain": today["hourly"][1]["chanceofrain"],
            "today_06_rain": today["hourly"][2]["chanceofrain"],
            "today_09_rain": today["hourly"][3]["chanceofrain"],
            "today_12_rain": today["hourly"][4]["chanceofrain"],
            "today_15_rain": today["hourly"][5]["chanceofrain"],
            "today_18_rain": today["hourly"][6]["chanceofrain"],
            "today_21_rain": today["hourly"][7]["chanceofrain"],
            
            
            "tomorrow_max_c": tomorrow["maxtempC"],
            "tomorrow_avg_c": tomorrow["avgtempC"],
            "tomorrow_min_c": tomorrow["mintempC"],
            "tomorrow_uv": tomorrow["uvIndex"],
            "tomorrow_date": tomorrow["date"],
            "tomorrow_moon_ill": tomorrow["astronomy"][0]["moon_illumination"],
            "tomorrow_sunrise": tomorrow["astronomy"][0]["sunrise"],
            "tomorrow_sunset": tomorrow["astronomy"][0]["sunset"],
            
            "day_after_max_c": day_after["maxtempC"],
            "day_after_avg_c": day_after["avgtempC"],
            "day_after_min_c": day_after["mintempC"],
            "day_after_uv": day_after["uvIndex"],
            "day_after_date": day_after["date"],
            "day_after_moon_ill": day_after["astronomy"][0]["moon_illumination"],
            "day_after_sunrise": day_after["astronomy"][0]["sunrise"],
            "day_after_sunset": day_after["astronomy"][0]["sunset"],
        }
            
        return self.data