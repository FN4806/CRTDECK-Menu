import curses
import datetime
from ui.screens import Screen
from ui.widgets import draw_box, draw_box_divider

WEATHER_ART = {
    "Sunny": [
        "     \\ | /   ",
        "      .-.    ",
        "   --(   )-- ",
        "      `-'    ",
        "     / | \\   ",
        "             ",
        "             ",
    ],

    "Clear": [
        "             ",
        "    .    *   ",
        "       .     ",
        "   *     .   ",
        "      '      ",
        "  .      *   ",
        "             ",
    ],

    "Partly cloudy": [
        "    \\ |      ",
        "     .-.     ",
        "  --(   ).-- ",
        "     `-(   ).",
        "       (___(_",
        "             ",
        "             ",
    ],

    "Cloudy": [
        "             ",
        "      .--.   ",
        "   .-(    ). ",
        "  (___.__)__)",
        "             ",
        "             ",
        "             ",
    ],

    "Overcast": [
        "   .--. .--. ",
        " .(    '    )",
        "(___.___.___)",
        " .--. .--.  ",
        "(____._____) ",
        "             ",
        "             ",
    ],

    "Mist": [
        "             ",
        "  _ - _ - _  ",
        " - _ - _ -   ",
        "  _ - _ - _  ",
        " - _ - _ -   ",
        "             ",
        "             ",
    ],

    "Fog": [
        "             ",
        " =========== ",
        "   ========  ",
        " =========== ",
        "  ========   ",
        " =========== ",
        "             ",
    ],

    "Light rain": [
        "      .--.   ",
        "   .-(    ). ",
        "  (___.__)__)",
        "     '   '   ",
        "   '   '     ",
        "      '      ",
        "             ",
    ],

    "Moderate rain": [
        "      .--.   ",
        "   .-(    ). ",
        "  (___.__)__)",
        "   //  //    ",
        "  //  //     ",
        "   //  //    ",
        "             ",
    ],

    "Heavy rain": [
        "      .--.   ",
        "   .-(    ). ",
        "  (___.__)__)",
        "  /////////  ",
        " /////////   ",
        "  /////////  ",
        "             ",
    ],

    "Patchy rain possible": [
        "    \\ |      ",
        "     .-.     ",
        "  --(   ).-- ",
        "     `-(   ).",
        "       (___(_",
        "    '   '    ",
        "             ",
    ],

    "Light snow": [
        "      .--.   ",
        "   .-(    ). ",
        "  (___.__)__)",
        "    *   *    ",
        "      *      ",
        "   *     *   ",
        "             ",
    ],

    "Moderate snow": [
        "      .--.   ",
        "   .-(    ). ",
        "  (___.__)__)",
        "   *  *  *   ",
        " *   *   *   ",
        "   *  *  *   ",
        "             ",
    ],

    "Heavy snow": [
        "      .--.   ",
        "   .-(    ). ",
        "  (___.__)__)",
        "  *********  ",
        " * * * * *   ",
        "  *********  ",
        "             ",
    ],

    "Sleet": [
        "      .--.   ",
        "   .-(    ). ",
        "  (___.__)__)",
        "   /*  /*    ",
        "  */  */     ",
        "   /*  /*    ",
        "             ",
    ],

    "Freezing rain": [
        "      .--.   ",
        "   .-(    ). ",
        "  (___.__)__)",
        "   //  //    ",
        "  _*_ _*_    ",
        " *_* *_*     ",
        "             ",
    ],

    "Thunderstorm": [
        "      .--.   ",
        "   .-(    ). ",
        "  (___.__)__)",
        "      /_     ",
        "    _/ /     ",
        "     /_      ",
        "             ",
    ],

    "Thundery outbreaks possible": [
        "    \\ |      ",
        "     .-.     ",
        "  --(   ).-- ",
        "     `-(   ).",
        "       /_  (_",
        "      /      ",
        "             ",
    ],

    "Blizzard": [
        "      .--.   ",
        "   .-(    ). ",
        "  (___.__)__)",
        " */*/*/*/*   ",
        "/*/*/*/*/    ",
        " */*/*/*/*   ",
        "             ",
    ],

    "Ice pellets": [
        "      .--.   ",
        "   .-(    ). ",
        "  (___.__)__)",
        "   o  o  o   ",
        " o   o   o   ",
        "   o  o  o   ",
        "             ",
    ],
}

def get_weather_art(desc):
    d = desc.lower()

    if "thunder" in d:
        return WEATHER_ART["Thunderstorm"]
    if "blizzard" in d:
        return WEATHER_ART["Blizzard"]
    if "snow" in d:
        if "heavy" in d:
            return WEATHER_ART["Heavy snow"]
        if "moderate" in d:
            return WEATHER_ART["Moderate snow"]
        return WEATHER_ART["Light snow"]
    if "sleet" in d:
        return WEATHER_ART["Sleet"]
    if "freezing" in d:
        return WEATHER_ART["Freezing rain"]
    if "rain" in d or "drizzle" in d:
        if "heavy" in d:
            return WEATHER_ART["Heavy rain"]
        if "moderate" in d:
            return WEATHER_ART["Moderate rain"]
        return WEATHER_ART["Light rain"]
    if "fog" in d:
        return WEATHER_ART["Fog"]
    if "mist" in d:
        return WEATHER_ART["Mist"]
    if "overcast" in d:
        return WEATHER_ART["Overcast"]
    if "partly" in d:
        return WEATHER_ART["Partly cloudy"]
    if "cloud" in d:
        return WEATHER_ART["Cloudy"]
    if "clear" in d:
        return WEATHER_ART["Clear"]
    if "sunny" in d:
        return WEATHER_ART["Sunny"]

    return WEATHER_ART["Cloudy"]

class WeatherScreen(Screen):
    def __init__(self, app):
        super().__init__(app)
        self.weather = app.weather
        self.message = self.weather.refresh()
        
    def handle_key(self, key):
        if key in (ord("r"), ord("R")):
            self.message = self.weather.refresh()
        elif key in (ord("b"), ord("B")):
            self.app.pop()
        elif key in (ord("q"), ord("Q")):
            self.app.home()
            
    def draw(self, win):
        win.erase()
        
        weatherDesc = self.weather.data["condition"]
        weather_art = get_weather_art(weatherDesc)
        
        loc = self.weather.data["location"]
        temp = self.weather.data["temp_c"]
        feels = self.weather.data["feels_like_c"]
        hum = self.weather.data["humidity"]
        wind_mph = self.weather.data["wind_mph"]
        wind_dir = self.weather.data["wind_dir"]
        pressure = self.weather.data["pressure"]
        lat = self.weather.data["lat"]
        lon = self.weather.data["long"]
        
        temp_1 = self.weather.data["today_00_temp"]
        temp_2 = self.weather.data["today_03_temp"]
        temp_3 = self.weather.data["today_06_temp"]
        temp_4 = self.weather.data["today_09_temp"]
        temp_5 = self.weather.data["today_12_temp"]
        temp_6 = self.weather.data["today_15_temp"]
        temp_7 = self.weather.data["today_18_temp"]
        temp_8 = self.weather.data["today_21_temp"]
        
        rain_1 = self.weather.data["today_00_rain"]
        rain_2 = self.weather.data["today_03_rain"]
        rain_3 = self.weather.data["today_06_rain"]
        rain_4 = self.weather.data["today_09_rain"]
        rain_5 = self.weather.data["today_12_rain"]
        rain_6 = self.weather.data["today_15_rain"]
        rain_7 = self.weather.data["today_18_rain"]
        rain_8 = self.weather.data["today_21_rain"]
                
        draw_box(win,2,2,18,52)
        win.addstr(2,4,"[WEATHER]",curses.A_BOLD)
        win.addstr(3,4,f"AREA: {loc}    LAT:{lat}N      LON:{lon}W", curses.A_BOLD)
        draw_box_divider(win,4,2,52)
        
        win.addstr(6,4,weather_art[0])
        win.addstr(7,4,weather_art[1])
        win.addstr(8,4,weather_art[2])
        win.addstr(9,4,weather_art[3])
        win.addstr(10,4,weather_art[4])
        win.addstr(11,4,weather_art[5])
        win.addstr(12,4,weather_art[6])
        
        win.addstr(6, 22,  f"SKY STATE  {weatherDesc}")
        win.addstr(7, 22,  f"TEMP       {temp}°C")
        win.addstr(8, 22,  f"FEELS      {feels}°C")
        win.addstr(9, 22,  f"HUMIDITY   {hum}%")
        win.addstr(10, 22, f"PRESSURE   {pressure} hPa")
        win.addstr(11, 22, f"WIND       {wind_dir} {wind_mph} mph")
        
        draw_box_divider(win,13,2,52)
        win.addstr(13,4,"[TODAY'S FORECAST]", curses.A_BOLD)
    
        win.addstr(14, 4," 0000 ")
        win.addstr(14,10," 0300 ")
        win.addstr(14,16," 0600 ")
        win.addstr(14,22," 0900 ")
        win.addstr(14,28," 1200 ")
        win.addstr(14,34," 1500 ")
        win.addstr(14,40," 1800 ")
        win.addstr(14,46," 2100 ")

        win.addstr(15, 4,f" {temp_1}°C ")
        win.addstr(15,10,f" {temp_2}°C ")
        win.addstr(15,16,f" {temp_3}°C ")
        win.addstr(15,22,f" {temp_4}°C ")
        win.addstr(15,28,f" {temp_5}°C ")
        win.addstr(15,34,f" {temp_6}°C ")
        win.addstr(15,40,f" {temp_7}°C ")
        win.addstr(15,46,f" {temp_8}°C ")


        win.addstr(16, 4,f"  {rain_1}% ")
        win.addstr(16,10,f"  {rain_2}% ")
        win.addstr(16,16,f"  {rain_3}% ")
        win.addstr(16,22,f"  {rain_4}% ")
        win.addstr(16,28,f"  {rain_5}% ")
        win.addstr(16,34,f"  {rain_6}% ")
        win.addstr(16,40,f"  {rain_7}% ")
        win.addstr(16,46,f"  {rain_8}% ")
        
        draw_box_divider(win,17,2,52)
        
        now = datetime.datetime.now()
        
        day = now.strftime("%A")
        date = now.strftime("%d") + " " + now.strftime("%B") + " " + now.strftime("%Y")
        time = now.strftime("%H") + ":" + now.strftime("%M")
        
        win.addstr(18,4,f"{day} // {date} // {time}")
        
        win.refresh()