import curses
from ui.screens import Screen
from ui.widgets import draw_box, draw_box_divider

class DabScreen(Screen):
    def __init__(self, app):
        super().__init__(app)
        self.selected = 0
        self.top_index = 0
        
        self.dab = app.dab
        
        self.playing = False
        self.station = 0
        self.station_message = ""
        self.stream_info = ""
        
        self.station_list = self.dab.get_station_list()
        
        self.dab.start_welle()
        
    def handle_key(self, key):
        if key in (ord("b"), ord("B")):
            self.app.pop()
        elif key in (ord("q"), ord("Q")):
            self.app.home()
        elif key == curses.KEY_UP:
            self.selected = max(0, self.selected - 1)
        elif key == curses.KEY_DOWN:
            self.selected = min(len(self.station_list) - 1, self.selected + 1)
        elif key in (10, 13):
            if not self.station_list:
                return
            
            station = self.station_list[self.selected]
            is_playing = self.dab.toggle_station(station)
            self.playing = is_playing
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
            
        visible_stations = self.station_list[self.top_index:self.top_index + num_rows]
        
        for index, station in enumerate(visible_stations):
            real_index = self.top_index + index
            
            style = curses.A_REVERSE if real_index == self.selected else curses.A_NORMAL
            win.addstr(start_y + index, 14, station["stationName"][:28], style)
            
        
        draw_box_divider(win, 15,2,52)
        win.addstr(15,4,"[CURRENTLY PLAYING]", curses.A_BOLD)
        
        if self.playing:
            info = self.dab.get_current_service_info()
            
            win.addstr(16,4,info["dls"])
            win.addstr(17,4,self.station_list[self.station]["stationName"])
            win.addstr(17,49,self.station_list[self.station]["channelName"])
            win.addstr(18,4,f"{info["bitrate"]} kbps {info["codec"]} {info["protection"]}  Signal:{info["snr"]}")
        
        else:
            win.addstr(17,4,"        Press Enter to Select a Station")
        
        win.refresh()