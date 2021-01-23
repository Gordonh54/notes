total=0
lowestnum = int(input("What is your lowest value?\n"))
highestnum=int(input("What will be your highest value?\n"))
while lowestnum <highestnum:
  if lowestnum%2==1:
      lowestnum+=1
  total+=lowestnum
  lowestnum+=2
print("the sum of even numbers between ",lowestnum," and ",highestnum," is equal to ",total)
  