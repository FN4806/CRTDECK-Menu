import curses
from ui.screens import Screen
from enum import IntFlag
from ui.widgets import draw_box
from ui.app_screens.weather_screen import WeatherScreen

class MenuStyles(IntFlag):
    NONE = 0
    CENTRED = 1
    BOXED = 2
    FULLSCREEN = 4

class MenuScreen(Screen):
    def __init__(self, app, title, items, style=MenuStyles.NONE):
        super().__init__(app)
        self.title = title
        self.items = items
        self.selected = 0
        self.style = style
        
    def handle_key(self, key):
        if key == curses.KEY_UP:
            self.selected = max(0, self.selected - 1)
            
        elif key == curses.KEY_DOWN:
            self.selected = min(len(self.items) - 1, self.selected + 1)
        
        elif key in (10, 13):
            self.items[self.selected][1]()
            
        elif key in (ord("b"), ord("B")):
            self.app.pop()
            
        elif key in (ord("q"), ord("Q")):
            self.app.home()
    
    def draw(self, win):
        win.clear()
        h, w = win.getmaxyx()
        
        menu_width = 28
        menu_height = len(self.items) + 4
        
        if self.style & MenuStyles.CENTRED:
            y0 = max(0, (h-menu_height) // 2)
            x0 = max(0, (w-menu_width) // 2)
        else:
            y0 = 0
            x0 = 0
            
        if self.style & MenuStyles.BOXED:
            draw_box(win, y0, x0, menu_height, menu_width)

            inner_y = y0 + 1
            inner_x = x0 + 2
            inner_width = menu_width - 4
        else:
            inner_y = y0
            inner_x = x0
            inner_width = menu_width
            
        title_x = x0 + max(1, (menu_width - len(self.title)) // 2)
        win.addstr(inner_y, title_x, self.title[:inner_width], curses.A_BOLD)
        
        for index, (label, _) in enumerate(self.items):
            attr = curses.A_REVERSE if index == self.selected else curses.A_NORMAL
            win.addstr(inner_y + index + 2, inner_x, label[:inner_width], attr)
            
        win.addstr(h - 1, 2, "↑↓=Navigate Enter=Select  B=Back  Q=Home")
        win.refresh()
    
    
def build_main_menu(app):
    return MenuScreen(app, "CRTDECK", [
        ("Radio", lambda: app.push(build_radio_menu(app))),
        ("System", lambda: app.push(build_system_menu(app))),
        ("Tools", lambda: app.push(build_tools_menu(app))),
        ("Visuals", lambda: app.push(build_visuals_menu(app))),
        ("Settings", lambda: app.push(build_settings_menu(app))),
        ("Exit", lambda: setattr(app, "running", False)),
    ], MenuStyles.BOXED | MenuStyles.CENTRED)
        
def build_radio_menu(app):
    return MenuScreen(app, "Radio", [
        ("DAB", lambda: None),
        ("FM", lambda: None),
        ("RTL-SDR", lambda: None),
    ], MenuStyles.BOXED | MenuStyles.CENTRED)
    
def build_system_menu(app):
    return MenuScreen(app, "System", [
        ("Status", lambda: None),
        ("Network", lambda: None),
        ("Audio Test", lambda: None),
        ("Reboot", lambda: None),
        ("Shutdown", lambda: None),
    ], MenuStyles.BOXED | MenuStyles.CENTRED)

def build_tools_menu(app):
    return MenuScreen(app, "Tools", [
        ("GPIO", lambda: None),
        ("Serial Console", lambda: None),
        ("File Browser", lambda: None),
        ("Hex Viewer", lambda: None),
    ], MenuStyles.BOXED | MenuStyles.CENTRED)

def build_visuals_menu(app):
    return MenuScreen(app, "Visuals", [
        ("Matrix", lambda: None),
        ("Fire", lambda: None),
        ("Clock", lambda: None),
        ("Doom", lambda: None),
        ("Weather", lambda: app.push(WeatherScreen(app)))
    ], MenuStyles.BOXED | MenuStyles.CENTRED)

def build_settings_menu(app):
    return MenuScreen(app, "Settings", [
        ("Audio", lambda: None),
        ("Display", lambda: None),
        ("Controls", lambda: None),
        ("About", lambda: None)
    ], MenuStyles.BOXED | MenuStyles.CENTRED)