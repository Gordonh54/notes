import curses
import random 
def window(stdscr):
  #sets variables as height and width of screen.
  (sh,sw) = stdscr.getmaxyx()
  
  #setup colors
  curses.start_color()
  curses.use_default_colors()

  #initialize color pairs
  for i in range(0, curses.COLORS):
    curses.init_pair(i+1, i, -1)
    #stdscr.addstr("<{0}>".format(i+1), curses.color_pair(i+1))

  #turn off delay of the getchr function
  stdscr.nodelay(True)
  stdscr.timeout(250)

  while True:
    #get random letter ASCII code number
    letter=random.randint(33,126)
    #get random color number
    color = random.randint(1,curses.COLORS+1)
    #get random location
    y = random.randint(0, sh-1)
    x= random.randint(0,sw-1)

    stdscr.addstr(y,x,chr(letter),curses.color_pair(color))

    if stdscr.getch()==27: break

  stdscr.getch()

curses.wrapper(window)