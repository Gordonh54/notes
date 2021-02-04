import random
minimum=int(input("Enter your lowest value: "))
maximum=int(input("Enter your highest value: "))
tries=int(input("Enter the number of tries you would like to give yourself: "))
correct=random.randint(minimum,maximum)
for x in range(tries):
  guess=int(input("Make a guess: "))
  if(guess==correct):
    break
  elif(guess > correct):
    print("your guess is higher. you have ",tries-(x+1)," tries left.")
  elif(guess < correct):
    print("your guess is lower. you have ",tries-(x+1)," tries left.")
if(guess==correct):
  print("you win")
if(guess!=correct):
  print("you lose. The correct number was ",correct)
