import curses
from curses import textpad 
import random
import math

block=chr(9608)

def initfield(stdscr,center,size):
  field=[]
  r,c=0,0
  for y in range(center[0]-size[0]//2,center[0]+size[0]//2):
    field.append([[0,0,0]]*size[1])
    for x in range(center[1]-size[1], center[1]+size[1],2):
      field[r][c]=[y,x,0]
      c+=1
    r+=1
    c=0

  #generate random bombs
  i=0
  while i < math.prod(size)//7:
    rand=random.randint(0,math.prod(size)-1)
    row=rand//size[1]
    column=rand-row*size[1]
    if field[row][column][2]== -1:
      continue
    else:
      field[row][column][2] = -1
      i += 1
  #calc bombs
  for r in range(0,size[0]):
    for c in range(0, size[1]):
      if field[r][c][2] == -1: continue
      for sr in [r-1, r, r+1]:
        for sc in [c-1, c, c+1]:
          #check if out of bounds
          if sr < 0 or sr > size[0]-1 or sc > size[1]-1 or sc < 0:
            continue
          elif sr == r and sc == c:
            continue
          elif field[sr][sc][2] == -1:
            field[r][c][2] +=1
  return field


def paintfield(stdscr, field, size, gridcolor):
  for r in range(0,size[0]):
    for c in range(0,size[1]):
      if field[r][c][2] == -1:
        stdscr.addstr(field[r][c][0], field[r][c][1], chr(10041), curses.color_pair(161))
      else:
        stdscr.addstr(field[r][c][0],field[r][c][1], str(field[r][c][2]))
         #stdscr.addstr(field[r][c][0], field[r][c][1], block, curses.color_pair(gridcolor%2+2))
      gridcolor+=1
    gridcolor+=1

def window(stdscr):
  #sets variables as height and width of screen.
  (sh,sw) = stdscr.getmaxyx()
  #setup colors
  curses.start_color()
  curses.use_default_colors()
  #initialize color pairs
  for i in range(0, curses.COLORS):
    curses.init_pair(i+1, i, -1)
  #turn off cursor, or make it invisible
  curses.curs_set(0)
  #turn off delay of the getchr function
  stdscr.nodelay(True)
  stdscr.timeout(250)

  #define colors
  size = [10,20]
  center = [sh//2,sw//2]
  gridcolor = 0
  
  field = initfield(stdscr, center,size)
  while True:
      userKey = stdscr.getch()
      if userKey == 27:
        break
      """
      for y in range(center[0]-size[0]//2,center[0]+size[0]//2):
        for x in range(center[1]-size[1], center[1]+size[1]):
          stdscr.addstr(y,x,block,curses.color_pair(gridcolor%2+2))
          gridcolor+=1
        gridcolor+=1
      """
      paintfield(stdscr, field, size, gridcolor)
      
      
  #stdscr.getch()

#wrap up window function
curses.wrapper(window)