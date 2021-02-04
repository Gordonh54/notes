import curses

def window(stdscr):
  #sets variables as height and width of screen.
  (sh,sw) = stdscr.getmaxyx()
  #print string welcome message
  msg = "Welcome to the ASCII decoder!"
  stdscr.addstr(sh//2,sw//2 - len(msg)//2, msg)

  while True:
      userKey = stdscr.getch()
      stdscr.addstr("ASCII: {0}, Button: {1} ".format(userKey, chr(userKey)))
      if userKey == 27:
        break
  #collect user info, but for now just 'holds on' to the screen
  #stdscr.getch()

#wrap up window function
curses.wrapper(window)