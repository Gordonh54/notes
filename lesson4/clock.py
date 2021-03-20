import curses
import datetime

def window(stdscr):
  #sets variables as height and width of screen.
  (sh,sw) = stdscr.getmaxyx()
  stdscr.nodelay(True)
  curses.curs_set(0)
  stdscr.timeout(100)
  x=datetime.datetime.now()
  while True:
      userKey = stdscr.getch()
      if userKey == 27:
        break
      y=datetime.datetime.now()
      men = (y-x)
      stdscr.addstr(0,0,str(men.seconds))
  #collect user info, but for now just 'holds on' to the screen
  #stdscr.getch()

#wrap up window function
curses.wrapper(window)