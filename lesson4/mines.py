import curses
import math
import random
import datetime


gameover=True



#-----------------------------------------------------
#managing the field
#-----------------------------------------------------
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

def checkfield(field, size, index=0):
  bombnumber = 0
  flagnumber = 0
  safenumber =0
  #create a bomb checker
  #create a bomb counter
  for y in range(0, size[0]):
    for x in range(0, size[1]):
      if field[y][x][2] == -1:
        bombnumber+=1
        if field[y][x][3] == "blasted":
          return False
      elif field[y][x][3] == "open":
        safenumber +=1
      if field[y][x][3] == "flagged":
        flagnumber +=1
  if index == 1: 
    return True
  elif index == 2: #for number of flags
    return flagnumber
  elif index == 3: return safenumber #number of safe squares opened
  elif index == 0:
    return bombnumber

def win(field, size):
  for y in range(0, size[0]):
    for x in range(0,size[1]):
      if field[y][x][2] != -1:
        field[y][x][3] = "open"

def gameoverfunction(stdscr, colors):
  sh, sw = stdscr.getmaxyx()
  gameovermsg="haha you lose"
  stdscr.addstr(1, sw//2-len(gameovermsg)//2, gameovermsg, curses.color_pair(161))
#-----------------------------------------------------
#-----------------------------------------------------
#color
def colordict():
  return {
        "wrong": curses.color_pair(161),
        "cover": curses.color_pair(9),
        "flag": curses.color_pair(161), 
        "blasted": curses.color_pair(233),
        #"-1": curses.color_pair(16), not using this
        "-1": curses.color_pair(89),
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
#-----------------------------------------------------
#Relating to drawing on the screen
#-----------------------------------------------------
def paintfield(stdscr, field, size, colors):
    for r in range(0, size[0]):
        for c in range(0, size[1]):
            paintcell(stdscr, field[r][c], colors)
def paintcell(stdscr, cell, colors, reverse=False, show=False):
  
  # decide the cell character and cell color
  cell_ch = chr(9608)
  cell_color = colors['cover']

  # check the status of each cell.
  if cell[3] == "wrong":
    cell_ch = chr(10006)
    cell_color = colors['wrong']
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
def clearrow(stdscr, sw,y):
  space = " "
  stdscr.addstr(y,0,space*sw)
#-----------------------------------------------------
#-----------------------------------------------------
#Relating to controls
#-----------------------------------------------------
def blast(stdscr, field, size, colors): 
  for y in range(0, size[0]):
    for x in range(0, size[1]):
      if field[y][x][2] == -1:
        field[y][x][3] = "open"
        paintcell(stdscr, field[y][x], colors)
      elif field[y][x][3] == "flagged":
        field[y][x][3] = "wrong"
        paintcell(stdscr, field[y][x], colors)
        
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
    cell[3] = "blasted"
  elif cell[3] == "covered" and cell[3]!="flagged":
    cell[3]="open"
    paintcell(stdscr, cell, colors)

#currently it only opens one square
def opensurrounding(stdscr, field, row, column, size, colors):
  if field[row][column][3] != "covered" or field[row][column][3] !="flagged": 
    for r in [row-1, row, row+1]:
      for c in [column-1, column, column+1]:
        if r < 0 or r > size[0] - 1 or c < 0 or c > size[1] - 1 or field[r][c][3] == "open":
          continue # out of field, skip
        digcell(stdscr,field[r][c], field, size, colors)
        if field[r][c][2] == 0:
          opensurrounding(stdscr,field, r, c, size, colors)
        #if the square is 0, dig then opensurrounding
#-----------------------------------------------------
#-----------------------------------------------------
#Managing the leaderboard
#-----------------------------------------------------
#at beginning of game round:
#read
#put it on the game right bar or soemthing

def writeleaderboard(leaderboard, stdscr, sw):
  y = 1
  xinc = sw//4
  lbtitle = "Leaderboard:"
  stdscr.addstr(y, sw//2-len(lbtitle)//2 + xinc,lbtitle)
  
  for i in leaderboard:
    y+=2
    stdscr.addstr(y, sw//2-len(i)//2 + xinc, i)
    
#sorting function
def sortbyscore(item):
  scores = item.split()
  return int(scores[0])

def manageleaderboard(stdscr,sh,sw,newscore,leaderboard):
  #stop time and frame rate
  stdscr.nodelay(False)
  stdscr.timeout(-1)
  #ask for name
  addname = "Highscore! Enter your name:"
  stdscr.addstr(3, sw//2 - len(addname)//2, addname)
  name = ""
  blank = " "*25
  while True:
    username = stdscr.getch()
    if username == 27:
      break
    if username == 10:
      if len(name) <= 20 and len(name) > 0: 
        break
      elif len(name) == 0:
        #write something down
        continue
    if username == 263:
      name = name[0:-1]
    elif len(name) <= 20:
      name += chr(username)
    
    stdscr.addstr(4, sw//2-len(blank)//2, blank)
    nametxt = name + chr(9608)
    stdscr.addstr(4, sw//2-len(nametxt)//2, nametxt)
  if username == 27: return False
  
  userscore = str(newscore) + " " + name
  leaderboard.append(userscore)
  leaderboard.sort(key=sortbyscore)
  leaderboard.pop()
  lbtext = "\n".join(leaderboard)
  filew = open("lesson4/leaderboard", "w")
  filew.write(lbtext)
  filew.close()
  stdscr.addstr(3, sw//2-len(blank*2)//2, blank*2)
  stdscr.addstr(4, sw//2-len(blank)//2, blank)
  stdscr.addstr(5, sw//2-len(blank)//2, blank)
  stdscr.nodelay(True)
  stdscr.timeout(100)

"""
100 x
350 y
349587 u

leaderboard = [[100, "x"], [350, "y"], [349587, "u"]]

if score < leaderboard[-1][0]:
  username = function that determines your name
  yourscoure = [score, username]
  leaderboard.append(yourscoure)
  sortmethod
"""

#sorting method at end of game:
#if person's score <(time) last score on the list: 
#ask for name and make it the second item on list, first item is the score 
#append and add their score
#sort method (find on sean's replit minesweeper/sorting.py)
#pop out last one
#write to file
#-----------------------------
#-----------------------------------------------------------------------------



#
#GAME
#
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

  stdscr.nodelay(True)
  stdscr.timeout(100)


  hudenable = 0

  while True:
    stdscr.erase()
    gameover = True
    initialtime = datetime.datetime.now()
    field = initfield(center, size)
    bombnumber = checkfield(field,size)
    safenumber = math.prod(size) - bombnumber
    paintfield(stdscr, field, size, colors)
    r, c = 0, 0 #row and column coordinates
    nr, nc = 0, 0
    # paint the top left cell reverse color.
    paintcell(stdscr, field[r][c], colors, True)
    
    #stdscr.addstr(1,0,"height:{0}\n width {1}".format(sh, sw))
    
    #-------------------------------------------------------------------------------------------
    #manage the leaderboard
    #-------------------------------------------------------------------------------------------
    filer = open("lesson4/leaderboard", "r")
    filetext = filer.read()
    filer.close()
    leaderboard = filetext.split("\n")
    writeleaderboard(leaderboard, stdscr, sw)
    

    while gameover:
      flagnumber = checkfield(field,size,2)
      clearrow(stdscr,sw, 0)
      #hud
      if hudenable == 1:
        stdscr.addstr(0,0, "{0},{1},{2},{3}".format(nr,nc,field[nr][nc][2],field[nr][nc][3]))
      #flag
      stdscr.addstr(0,field[0][0][1], "{0} {1}".format(chr(9873), str(bombnumber - flagnumber)))
      #display time
      currenttime = datetime.datetime.now()
      stopwatch = currenttime-initialtime
      stdscr.addstr(0, field[0][-4][1], str(stopwatch.seconds))
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
      elif userkey in [102] and (flagnumber < bombnumber or field[r][c][3] == "flagged"):
        # flag cell
        flagcell(field[r][c])
      elif userkey in [100]:
        #dig cell, if a mine all mines are dug
        digcell(stdscr, field[r][c], field, size, colors)
        if field[r][c][2] == 0:
          opensurrounding(stdscr,field,r,c,size, colors)
      elif userkey in [32] and field[r][c][3] == "open":
        opensurrounding(stdscr, field, r,c, size, colors)
    
      #cheat keys TAB to hud and / to win
      elif userkey in  [47]:
        win(field, size)
        paintfield(stdscr, field, size, colors)
      elif userkey in [9]:
        if hudenable == 1:
          hudenable =0
        elif hudenable == 0:
          hudenable=1
        #win
      
      # paint the current cell normally 
      paintcell(stdscr, field[r][c], colors, False)
      # paint the new cell reverse color
      paintcell(stdscr, field[nr][nc], colors, True)
      # reset the current cell row and column id
      r, c = nr, nc

      gameover = checkfield(field,size, 1)
      if safenumber == checkfield(field, size, 3):
        gameover = False
      


    #ending the game

    #if not good:
    if safenumber != checkfield(field, size, 3):
      blast(stdscr, field, size, colors)
      gameoverfunction(stdscr, colors)
    #ifnot lose:
    elif safenumber == checkfield(field, size, 3):
      gamewinmsg = "you win!"
      stdscr.addstr(1, sw//2-len(gamewinmsg)//2, gamewinmsg, curses.color_pair(11))
      
      #currenttime = datetime.datetime.now()
      #stopwatch = currenttime-initialtime
      currentscore = int(stopwatch.seconds)
      #if get a highscore on the leaderboard
      scoremsg = "Score: {0}".format(currentscore)
      stdscr.addstr(2, sw//2-len(scoremsg)//2,scoremsg)

      if currentscore < int(leaderboard[-1].split()[0]):
        #execute order 66
        manageleaderboard(stdscr, sh, sw, currentscore, leaderboard)
      stdscr.addstr(3, sw//2-len(scoremsg)//2,scoremsg)
    
    newgame = "ENTER for new game, ESC or q to leave"
    stdscr.addstr(2, sw//2-len(newgame)//2,newgame)
    
    
    if userkey in [27, 133]:
      break
    while True:
      userkey = stdscr.getch()
      if userkey in [27, 133]:
        break
      if userkey == 10:
        break
    if userkey in [27, 133]:
      break
    
    for i in range(0,4):
      clearrow(stdscr,sw,i)
    

curses.wrapper(window)

#add levels (mines and size of game)
#name writing function
#leaderboard
#read and write, string split
#border