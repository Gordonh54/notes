import curses
import math
import random


gameover=True


# paint field function.
def initfield(center, size):
  
  field = []

  r, c = 0, 0
  for y in range(center[0] - size[0] // 2, center[0] + size[0] // 2):
    field.append([])
    for x in range(center[1] - size[1], center[1] + size[1], 2):
      #stdscr.addstr(y, x, chr(9608))
      field[r].append([y,x,0,"covered"])

    r = r + 1
    # reset column Index

  #generate bombs
  i = 0
  while i < math.prod(size) // 7:
    rand = random.randint(0, math.prod(size) - 1)
    row = rand // size[1]
    column = rand - row * size[1]
    if field[row][column][2] == -1:
      continue
    else:
      field[row][column][2] = -1
      i += 1

  # calc the number of bombs around a square.
  for r in range(0, size[0]):
      for c in range(0, size[1]):
          # if current cell is bomb.
          if field[r][c][2] == -1:
              continue # skip
          for sr in [r -1, r, r + 1]:
              for sc in [c - 1, c, c + 1]:
                  #check if out of range
                  if sr < 0 or sr > size[0] - 1 or sc < 0 or sc > size[1] - 1:
                      continue # out of field, skip
                  elif sr == r and sc == c:
                      continue # skip
                  elif field[sr][sc][2] == -1:
                      field[r][c][2] = field[r][c][2] + 1

  return field

def paintfield(stdscr, field, size, colors):

    for r in range(0, size[0]):
        for c in range(0, size[1]):
            paintcell(stdscr, field[r][c], colors)

def colordict():
  return {
        "cover": curses.color_pair(9),
        "flag": curses.color_pair(161), 
        "blasted": curses.color_pair(233),
        #"-1": curses.color_pair(16), not using this
        "-1": curses.color_pair(161),
        "0": curses.color_pair(1),
        "1": curses.color_pair(34), #
        "2": curses.color_pair(77), # 
        "3": curses.color_pair(12), #
        "4": curses.color_pair(166), # 
        "5": curses.color_pair(209), # 
        "6": curses.color_pair(172), # 
        "7": curses.color_pair(2), # 
        "8": curses.color_pair(8), #
  }

def paintcell(stdscr, cell, colors, reverse=False, show=False):
  
  # decide the cell character and cell color
  cell_ch = chr(9608)
  cell_color = colors['cover']

  # check the status of each cell.
  if cell[3] == "flagged":
    cell_ch = chr(9873)
    cell_color = colors['flag']
  if cell[3] == "blasted":
    cell_ch = chr(10041)
    cell_color = colors["blasted"]
  if cell[3] == "open":
    if cell[2] == -1:
      cell_ch = chr(10041)
      cell_color = colors["-1"]
    else:
      cell_ch = str(cell[2])
      cell_color = colors[str(cell[2])]

  if reverse:
    cell_color = curses.A_REVERSE

  stdscr.addstr(cell[0], cell[1], cell_ch, cell_color)

def gameoverfunction(stdscr, colors):
  sh, sw = stdscr.getmaxyx()
  gameovermsg="haha you lose"
  stdscr.addstr(1, sw//2-len(gameovermsg)//2, gameovermsg, curses.color_pair(161))

#open all mines
def blast(stdscr, field, size, colors): 
  for y in range(0, size[0]):
    for x in range(0, size[1]):
      if field[y][x][2] == -1:
        field[y][x][3] = "open"
        paintcell(stdscr, field[y][x], colors)
  gameoverfunction(stdscr, colors)
        

def flagcell(cell):
  if cell[3] == "flagged":
    cell[3] = "covered"
  elif cell[3] == "covered":
    cell[3] = "flagged"


"""
current method; might replace later """
#simplify
def digcell(stdscr, cell, field, size, colors):
  if cell[2] == -1 and cell[3]!="flagged":
    #move bottom
    cell[3] = "blasted"
    blast(stdscr, field, size, colors)
    return False
  elif cell[3] == "covered" and cell[3]!="flagged":
    cell[3]="open"
    paintcell(stdscr, cell, colors)
    return True
  else: return True

#currently it only opens one square
def opensurrounding(stdscr, field, row, column, size, colors):
  if field[row][column][3] == "covered" or field[row][column][3]=="flagged":
    return True
  for r in [row-1, row, row+1]:
    for c in [column-1, column, column+1]:
      g=True
      if r < 0 or r > size[0] - 1 or c < 0 or c > size[1] - 1 or field[r][c][3] == "open":
        continue # out of field, skip
      
      g = digcell(stdscr,field[r][c], field, size, colors)
      if field[r][c][2] == 0:
        g= opensurrounding(stdscr,field, r, c, size, colors)
        if g == False: 
          return g
      #if the square is 0, dig then opensurrounding
  return g
      
  return False

def checkfield(field, size, index):
  bombnumber = 0
  #create a bomb checker
  #create a bomb counter
  for y in range[0, size[0]]:
    for x in range[0, size[1]]:
      
      return 0

def window(stdscr):
  #initialize color pairs
  curses.start_color()
  curses.use_default_colors()
  for i in range(0, curses.COLORS):
    if i==232:
      curses.init_pair(i+1, i, curses.COLOR_RED)
    else:
      curses.init_pair(i + 1, i , -1)
  #remove cursor
  curses.curs_set(0)
  #activate sh and sw, find center of board, and create a list for colors
  sh, sw = stdscr.getmaxyx()
  center = [sh // 2, sw // 2]
  colors = colordict()

  # set this a list [row, column]
  size = [10, 20]

  while True:
    gameover = True
    field = initfield(center, size)
    paintfield(stdscr, field, size, colors)
    r, c = 0, 0 #row and column coordinates
    nr, nc = 0, 0
    # paint the top left cell reverse color.
    paintcell(stdscr, field[r][c], colors, True)
    stdscr.addstr(1,sw//3,"                                                  ")
    
    while gameover:
      userkey = stdscr.getch()
      # 27 ESC, 113 is q
      if userkey in [27, 113]:
        break;
      elif userkey in [curses.KEY_RIGHT]:
        if c < size[1] - 1:
          nc = c + 1
      elif userkey in [curses.KEY_LEFT]:
        if c > 0:
          nc = c - 1
      elif userkey in [curses.KEY_DOWN]:
        if r < size[0] - 1:
          nr = r + 1
      elif userkey in [curses.KEY_UP]:
        if r > 0:
          nr = r - 1
      elif userkey in [102]:
        # flag cell
        flagcell(field[r][c])
      elif userkey in [100]:
        #dig cell, if a mine all mines are dug
        gameover = digcell(stdscr, field[r][c], field, size, colors)
      elif userkey in [32]:
        gameover = opensurrounding(stdscr, field, r,c, size, colors)


      stdscr.addstr(0,0,"                                             ")
      stdscr.addstr(0,0, "{0},{1},{2},{3}".format(nr,nc,field[nr][nc][2],field[nr][nc][3]))
      # paint the current cell normally 
      paintcell(stdscr, field[r][c], colors, False)
      # paint the new cell reverse color
      paintcell(stdscr, field[nr][nc], colors, True)
      # reset the current cell row and column id
      r, c = nr, nc
    if userkey in [27, 133]:
      break
    userkey = stdscr.getch()
    if userkey in [27, 133]:
      break
    

curses.wrapper(window)

#clean digcell and open surrounding
#^fix space not ending game
#stopwatch
#bomb counter
#give message to tell people to make screen bigger or else
#Xs on the wrong flags
#highlight triggered bombs
#border (last priority)
