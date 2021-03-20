import curses

def window(stdscr):
  #sets variables as height and width of screen.
  (sh,sw) = stdscr.getmaxyx()
  #print string welcome message
  #initialize color pairs
  curses.start_color()
  curses.use_default_colors()
  for i in range(0, curses.COLORS):
    curses.init_pair(i+1, i, -1)
  curses.curs_set(0)
  
  msg = ""
  filer = open("lesson4/writing","r")
  oldmsg = filer.read()
  msg = oldmsg + msg
  filer.close()

  filew = open("lesson4/writing", "w")
  
  while True:
    stdscr.erase()
    stdscr.addstr(0,0, msg + chr(9608))
    userKey = stdscr.getch()
    if userKey == 27:
      break
    elif userKey == 10:
      msg += "\n"
    elif userKey == 263:
      #slice function: grabs a section of the string not from 0-last (doesn't actually count the last one)
      msg = msg[0:-1]
    else:
      msg += chr(userKey)
    
  filew.write(msg)
      
  #collect user info, but for now just 'holds on' to the screen
  #stdscr.getch()

#wrap up window function
curses.wrapper(window)