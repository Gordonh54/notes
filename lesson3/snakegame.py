import curses
import random 
from curses import textpad 

def window(stdscr):
  #turn off cursor, or make it invisible
  curses.curs_set(0)
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
  

  welcome_message = "Welcome to the Snake Game!"
  stdscr.addstr(1, sw//2-len(welcome_message)//2, welcome_message)
  #define the rectangle boks
  borderindent=3
  box = [
    [borderindent,borderindent],
    [sh-borderindent, sw-borderindent]
  ]
  #draw border
  textpad.rectangle(stdscr, box[0][0],box[0][1], box[1][0], box[1][1]) 

  #define the body, chr(9608) is a block
  snake = [
    #head
    [sh//2,sw//2+1],
    #body
    [sh//2, sw//2],
    #tail
    [sh//2,sw//2-1]
  ]
  snake_chr = chr(9608)
  #define the apple coordinates
  apple = [sh//2, (sw//4)*3, 161]
  #define the initial direction for the snake to move
  direction=curses.KEY_RIGHT

  #default snake and apple colors
  snakecolor=3
  applecolor=0
  applelist = [
    125,161,203,227,191,47,22,100,55,54,95
  ]

  #score counter
  score = 0
  highscore = 0

  #full game looping starts here
  while True:
    score = 0
    #redrawing everything
    stdscr.erase()
    stdscr.nodelay(True)
    stdscr.timeout(250)
    #draw border
    textpad.rectangle(stdscr, box[0][0],box[0][1], box[1][0], box[1][1])
    snake = [
    #head
    [sh//2,sw//2+1],
    #body
    [sh//2, sw//2],
    #tail
    [sh//2,sw//2-1]
    ]
    snake_chr = chr(9608)
    #define the apple coordinates
    apple = [sh//2, (sw//4)*3, 161]
    stdscr.addstr(0, sw//2-len(welcome_message)//2, welcome_message)
    direction=curses.KEY_RIGHT

    while True: #color picker menu
      key=stdscr.getch()
      if key==10 or key ==27: break
      #left/right arrow keys
      elif key==260:
        if snakecolor == 2:
          snakecolor=16
        else:
          snakecolor -= 1
      elif key==261:
        if snakecolor == 16:
          snakecolor=2
        else:
          snakecolor +=1
      #up/down arrow keys 
      elif key==259:
        if applecolor==(len(applelist)-1):
          applecolor=0
        else: 
          applecolor += 1
      elif key==258:
        if applecolor==0:
          applecolor=len(applelist)-1
        else:
          applecolor -= 1

      #draw the snake and arrows around it
      for point in snake:
        stdscr.addstr(point[0], point[1], snake_chr, curses.color_pair(snakecolor))
      stdscr.addstr(snake[0][0], snake[0][1]+2, ">")
      stdscr.addstr(snake[0][0], snake[2][1]-2, "<")
      #drawing the apple and arrows around it
      stdscr.addstr(apple[0], apple[1], snake_chr, curses.color_pair(applelist[applecolor]))
      stdscr.addstr(apple[0]-1, apple[1], "^")
      stdscr.addstr(apple[0]+1, apple[1],"v")
      #print controls
      controlmsg = "Arrow keys to change colors, ENTER to continue, ESC to leave"
      stdscr.addstr(1, sw//2-len(controlmsg)//2, controlmsg)

    if key==27:break
    #remove the arrows
    stdscr.addstr(snake[0][0], snake[0][1]+2, " ")
    stdscr.addstr(snake[0][0], snake[2][1]-2, " ")
    stdscr.addstr(apple[0]-1, apple[1], " ")
    stdscr.addstr(apple[0]+1, apple[1]," ")
    stdscr.addstr(1,sw//2-len(controlmsg)//2, " "*len(controlmsg))

    while True: #gameplay loop
      #collect user input
      key = stdscr.getch()
      if key==27: break

      #current head
      head = snake[0]
      #tail coordinates
      tail = snake[-1]

      #decide direction
      if key == curses.KEY_UP and direction != curses.KEY_DOWN:
        direction = key
      elif key == curses.KEY_DOWN and direction != curses.KEY_UP:
        direction = key
      elif key == curses.KEY_RIGHT and direction != curses.KEY_LEFT:
        direction = key
      elif key == curses.KEY_LEFT and direction != curses.KEY_RIGHT:
        direction = key
      if direction == curses.KEY_UP:
        new_head = [head[0]-1, head[1]]
      elif direction == curses.KEY_DOWN:
        new_head = [head[0]+1, head[1]]
      elif direction == curses.KEY_RIGHT:
        new_head = [head[0], head[1]+1]
      elif direction == curses.KEY_LEFT:
        new_head = [head[0], head[1]-1]

      if new_head!=head:
        #moving the cell by adding the head
        stdscr.addstr(new_head[0],new_head[1],snake_chr, curses.color_pair(snakecolor))
        #erasing the tail
        stdscr.addstr(tail[0],tail[1],' ')
        #update snake, add new head, remove snake tail variable
        snake.insert(0, new_head)
      scoremsg = "Score: {0} Highscore: {1}".format(score, highscore)
      stdscr.addstr(1,sw//2-len(scoremsg)//2,scoremsg)
      controlmsg = "Arrow keys to move, ESC to leave"
      stdscr.addstr(2, sw//2-len(controlmsg)//2, controlmsg)
      #if snake head touches, create an apple at a new location
      if snake[0][0] == apple[0] and snake[0][1] == apple[1]:
        apple[0]=random.randint(borderindent+1,sh-(borderindent+1))
        apple[1]=random.randint(borderindent+1,sw-borderindent-1)
        stdscr.addstr(apple[0],apple[1],snake_chr,curses.color_pair(applelist[applecolor]))
        score += 1
      else:
        #pop function removes last item of a list
        snake.pop()
      
      #check if the snake hits itself
      dum = 0
      for bodybarrier in snake[1:]:
        if snake[0] == bodybarrier:
          dum =1

      #if head of snake touches the border or any part of itself (or its body)
      if (snake[0][0] == box[0][0] or 
        snake[0][0] == box[1][0] or 
        snake[0][1] == box[0][1] or
        snake[0][1] == box[1][1] or
        dum ==1):
        if score > highscore:
          highscore = score
        scoremsg = "Score: {0} Highscore: {1}".format(score, highscore)
        gameover="game over"
        stdscr.addstr(snake[0][0],snake[0][1],snake_chr,curses.color_pair(int(89)))
        stdscr.addstr(sh//2, sw//2-len(gameover)//2, gameover)
        stdscr.addstr(sh//2+1,sw//2-len(scoremsg)//2,scoremsg)
        stdscr.addstr(1,sw//2-len(scoremsg)//2,scoremsg)
        controlmsg = "Any key to continue, ESC to leave"
        stdscr.addstr(sh//2+2, sw//2-len(controlmsg)//2, controlmsg)
        stdscr.nodelay(0)
        key = stdscr.getch()
        break
    if key == 27: break
    


curses.wrapper(window)