import curses
from ui.screens import Screen
from ui.widgets import draw_box, draw_box_divider

class DabScreen(Screen):
    def __init__(self, app):
        super().__init__(app)
        
    def handle_key(self, key):
        if key in (ord("b"), ord("B")):
            self.app.pop()
        elif key in (ord("q"), ord("Q")):
            self.app.home()
    
    def draw(self, win):
        win.erase()
        
        draw_box(win, 2, 2, 18, 52)
        win.addstr(2,4,"[DAB RADIO]",curses.A_BOLD)
        
        draw_box(win,3,12, 12,32)
        win.addstr(3,23,"[STATIONS]",curses.A_BOLD)
        
        win.addstr(4,14,"Radio 1")
        win.addstr(5,14,"Radio 2")
        win.addstr(6,14,"Radio 3")
        win.addstr(7,14,"Radio 4")
        win.addstr(8,14,"Classic FM")
        win.addstr(9,14,"Planet Rock")
        win.addstr(10,14,"Absolute Rock Radio")
        win.addstr(11,14,"Absolute 80s")
        win.addstr(12,14,"Smooth Radio")
        win.addstr(13,14,"Jazz FM")
        
        draw_box_divider(win, 15,2,52)
        win.addstr(15,4,"[CURRENTLY PLAYING]", curses.A_BOLD)
        win.addstr(16,4,"You Shook Me - Led Zeppelin")
        win.addstr(17,4,"Absolute 80s")
        win.addstr(17,49,"12A")
        win.addstr(18,4,"Example")
        
        win.refresh()