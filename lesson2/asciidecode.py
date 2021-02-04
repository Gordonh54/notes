import curses
import random

random.seed()
def window(stdscr):
  #sets variables as height and width of screen.
  (sh,sw) = stdscr.getmaxyx()
  #print string welcome message
  msg = "Welcome to the ASCII decoder!"
  stdscr.addstr(0,sw//2 - len(msg)//2, msg)
  #setup colors
  curses.start_color()
  curses.use_default_colors()
  #initialize color pairs
  for i in range(0, curses.COLORS):
    curses.init_pair(i+1, i, -1)
    #stdscr.addstr("<{0}>".format(i+1), curses.color_pair(i+1))

  while True:
    userKey = stdscr.getch()
    stdscr.erase()
    if userKey == 27: #if button pressed is esc, break
      #ask if you want to break, press esc again. Otherwise, if any other button is pressed, ignore and print the ESC key
      stdscr.erase()
      #correctly position the message
      stdscr.addstr("Press ESC again to leave")
      decodemsg = "ASCII: {0}, Button: ESC".format(userKey)
      stdscr.addstr(1,0,decodemsg)
      userKey = stdscr.getch()
      if userKey == 27:
        break
      else:
        stdscr.erase()
    
    #creating random colors
    randcolor=random.randint(1,curses.COLORS-1)
    randcolor1=random.randint(1,curses.COLORS-1)
    while randcolor==randcolor1:#reset colors if they match  
      randcolor=random.randint(1,curses.COLORS-1)
      randcolor1=random.randint(1,curses.COLORS-1)
    borderchar = "-"
    if userKey == 9:
      decodemsg = "ASCII: 9, Button: TAB"
    elif userKey == 10:
      userChar = "ENTER"
    else:
      userChar = chr(userKey)
      borderchar = chr(userKey)
    
    stdscr.erase()
    stdscr.addstr(0,sw//2 - len(msg)//2, msg)
    #creating the borders
    for i in range(1,sw-1):#top row
      stdscr.addstr(1,i, borderchar, curses.color_pair(randcolor))
    for i in range(1,sw-1):#bottom row
      stdscr.addstr(sh-1,i,borderchar, curses.color_pair(randcolor))
    for i in range(2,sh-1):#left column
      stdscr.addstr(i,1,borderchar, curses.color_pair(randcolor))
    for i in range(2,sh-1):#right column
      stdscr.addstr(i,sw-2,borderchar, curses.color_pair(randcolor))
  
    if userKey != 9:
      decodemsg = "ASCII: {0}, Button: {1}".format(userKey, userChar)
    #correctly position the message
    stdscr.addstr(sh//2+1, sw//2-len(decodemsg)//2, decodemsg, curses.color_pair(randcolor1))
    
    
  #collect user info, but for now just 'holds on' to the screen
  #stdscr.getch()

#wrap up window function
curses.wrapper(window)