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
  box = [
    [3,3],
    [sh-3 , sw-3]
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
  #drawing the snake
  for point in snake:
    stdscr.addstr(point[0], point[1], snake_chr)

  #define the apple coordinates
  apple = [sh//2, (sw//4)*3, 161]
  #drawing the apple
  stdscr.addstr(apple[0], apple[1], snake_chr, curses.color_pair(161))

  #define the direction for the snake to move
  direction=curses.KEY_RIGHT
  
  while True:
    #collect user input
    key = stdscr.getch()
    if key==27: break

    #current head
    head = snake[0]
    #tail coordinates
    tail = snake[-1]
    #decide direction
    if key == curses.KEY_UP:
      direction = key
    elif key == curses.KEY_DOWN:
      direction = key
    elif key == curses.KEY_RIGHT:
      direction = key
    elif key == curses.KEY_LEFT:
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
      stdscr.addstr(new_head[0],new_head[1],snake_chr)
      #erasing the tail
      stdscr.addstr(tail[0],tail[1],' ')
      #update snake, add new head, remove snake tail variable
      snake.insert(0, new_head)
      
      
    
    #if snake head touches, create an apple at a new location
    if snake[0][0] == apple[0] and snake[0][1] == apple[1]:
      apple[0]=random.randint(4,sh-4)
      apple[1]=random.randint(4,sw-4)
      stdscr.addstr(apple[0],apple[1],snake_chr,curses.color_pair(161))
    else:
      #pop function removes last item of a list
      snake.pop()
    
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
        gameover="game over"
        stdscr.addstr(sh//2, sw//2-len(gameover)//2, gameover)
        stdscr.nodelay(0)
        stdscr.getch()
        break


curses.wrapper(window)