import curses
import time
from apps.weather import WeatherManager
from apps.dab import DabManager

class App:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.running = True
        self.screens = []
        self.weather = WeatherManager("Llansamlet")
        self.dab = DabManager()
        
    def push(self, screen):
        self.screens.append(screen)
        
    def pop(self):
        if len(self.screens) > 1:
            self.screens.pop()
            
    def home(self):
        self.screens = self.screens[:1]
        
    def current(self):
        return self.screens[-1]
    
    def run(self):
        curses.curs_set(0)
        self.stdscr.timeout(250)
        self.stdscr.keypad(True)
        
        while self.running:
            self.current().draw(self.stdscr)
            key = self.stdscr.getch()
            self.current().handle_key(key)
            time.sleep(0.03)
            
            
class Screen:
    def __init__(self, app):
        self.app = app
        
    def handle_key(self, key):
        pass
    
    def draw(self, win):
        pass