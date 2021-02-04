import curses
def window(stdscr):
  #sets variables as height and width of screen.
  (sh,sw) = stdscr.getmaxyx()
  
  #setup colors
  curses.start_color()
  curses.use_default_colors()

  #initialize color pairs
  for i in range(0, curses.COLORS):
    curses.init_pair(i+1, i, -1)
    curses.init_pair(curses.COLORS+1+i, 1, i)
    #stdscr.addstr("<{0}>".format(i+1), curses.color_pair(i+1))
    #stdscr.addstr("   ", curses.color_pair(curses.COLORS+1+i))
  #loop for all rows

  #counter for the colours
  textcolor = 1
  highlighter = textcolor+curses.COLORS
  
  for i in range(0,8): #for 16 columns
    for j in range(0,32):#loop for the entire row, 16 items   
      stdscr.addstr(i*2,j*4, "    ",curses.color_pair(highlighter))
      #stdscr.addstr(i*2,j," ",curses.color_pair(highlighter))
      #print text under
      stdscr.addstr(i*2+1,j*4, "{0}".format(textcolor),curses.color_pair(textcolor))
      #stdscr.addstr(i*2+1,j,"{0}".format(textcolor), curses.color_pair(textcolor))
      #colour increment
      textcolor+=1
      highlighter = textcolor + curses.COLORS
  stdscr.getch()

curses.wrapper(window)