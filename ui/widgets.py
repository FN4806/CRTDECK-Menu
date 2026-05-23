import curses

def draw_box(win, y, x, h, w):
    win.addch(y, x, curses.ACS_ULCORNER)
    win.addch(y, x + w - 1, curses.ACS_URCORNER)
    win.addch(y + h - 1, x, curses.ACS_LLCORNER)
    win.addch(y + h - 1, x + w - 1, curses.ACS_LRCORNER)
    
    win.hline(y, x + 1, curses.ACS_HLINE, w - 2)
    win.hline(y + h - 1, x + 1, curses.ACS_HLINE, w - 2)
    
    win.vline(y + 1, x, curses.ACS_VLINE, h - 2)
    win.vline(y + 1, x + w - 1, curses.ACS_VLINE, h - 2)