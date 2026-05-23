import curses
from ui.screens import App
from ui.app_screens.menus import build_main_menu

def main(stdscr):
    app = App(stdscr)
    app.push(build_main_menu(app))
    app.run()

curses.wrapper(main)

# from apps.weather import WeatherManager

# w = WeatherManager("Swansea")
# data = w.refresh()

# for key, value in data.items():
#     print(f"{key}: {value}")
    