import curses
from ui.screens import Screen
from ui.widgets import draw_box, draw_box_divider

class FmScreen(Screen):
    def __init__(self, app):
        super().__init__(app)
        self.frequency = 88
        
    def handle_key(self, key):
        if key in (ord("b"), ord("B")):
            self.app.pop()
            
        elif key in (ord("q"), ord("Q")):
            self.app.home()
            
        elif key == curses.KEY_LEFT:
            self.frequency = max(88, self.frequency - 0.05)
            
        elif key == curses.KEY_RIGHT:
            self.frequency = min(108, self.frequency + 0.05)
    
    def draw(self, win):
        win.erase()
        
        draw_box(win, 2, 2, 18, 52)
        win.addstr(2,4,"[FM RADIO]",curses.A_BOLD)
        
        target = ((self.frequency - 88) * 45) / 20
        target = round(target)
        
        win.addstr(7,5,"88       92       96      100      104     108")
        win.addstr(8,5,"├────────┼────────┼────────┼────────┼────────┤", curses.A_BOLD)
        win.addstr(9,(5 + target),"▲")
        win.addstr(10,(2 + target),f"{self.frequency:.2f} MHz ")
        
        draw_box_divider(win, 12, 2, 52)
        
        win.refresh()