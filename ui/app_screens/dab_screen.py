import curses
from ui.screens import Screen
from ui.widgets import draw_box, draw_box_divider

class DabScreen(Screen):
    def __init__(self, app):
        super().__init__(app)
        self.selected = 0
        self.top_index = 0
        self.stations = [
            {"name": "Radio 1", "band": "12A"},
            {"name": "Radio 2", "band": "12A"},
            {"name": "Radio 3", "band": "12A"},
            {"name": "Radio 4", "band": "12A"},
            {"name": "Radio Classic FM", "band": "12A"},
            {"name": "Planet Rock", "band": "12A"},
            {"name": "Absolute Rock Radio", "band": "12A"},
            {"name": "Absolute 80s", "band": "12A"},
            {"name": "Smooth Radio", "band": "12A"},
            {"name": "Jazz FM", "band": "12A"},
            {"name": "Absolute 00s", "band": "12A"},
            {"name": "Absolute 90s", "band": "12A"},
            {"name": "Absolute 70s", "band": "12A"},
            {"name": "Absolute 60s", "band": "12A"},
        ]
        self.playing = False
        self.station = 0
        self.station_message = ""
        self.stream_info = ""
        
    def handle_key(self, key):
        if key in (ord("b"), ord("B")):
            self.app.pop()
        elif key in (ord("q"), ord("Q")):
            self.app.home()
        elif key == curses.KEY_UP:
            self.selected = max(0, self.selected - 1)
        elif key == curses.KEY_DOWN:
            self.selected = min(len(self.stations) - 1, self.selected + 1)
        elif key in (10, 13):
            
            if self.station == self.selected and self.playing:
                self.playing = False
            else:
                self.playing = True
                self.station = self.selected
    
    def draw(self, win):
        win.erase()
        
        draw_box(win, 2, 2, 18, 52)
        win.addstr(2,4,"[DAB RADIO]",curses.A_BOLD)
        
        draw_box(win,3,12, 12,32)
        win.addstr(3,23,"[STATIONS]",curses.A_BOLD)
        
        start_y = 4
        num_rows = 10
        
        if self.selected - self.top_index > 9:
            self.top_index += 1
        elif self.selected < self.top_index:
            self.top_index -= 1
            
        visible_stations = self.stations[self.top_index:self.top_index + num_rows]
        
        for index, station in enumerate(visible_stations):
            real_index = self.top_index + index
            
            style = curses.A_REVERSE if real_index == self.selected else curses.A_NORMAL
            win.addstr(start_y + index, 14, station["name"][:28], style)
            
        
        draw_box_divider(win, 15,2,52)
        win.addstr(15,4,"[CURRENTLY PLAYING]", curses.A_BOLD)
        
        if self.playing:
            win.addstr(16,4,"You Shook Me - Led Zeppelin")
            win.addstr(17,4,self.stations[self.station]["name"])
            win.addstr(17,49,self.stations[self.station]["band"])
            win.addstr(18,4,"Example")
        
        else:
            win.addstr(17,4,"        Press Enter to Select a Station")
        
        win.refresh()