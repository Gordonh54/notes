x,y=0,1 #this is a way to define multiple variables
line=str()
count=int(input("How many numbers do you want? "))
i=0
while i<count:
  z=str(x)
  if i+1==10:
    line+=z+",\n"
  elif i==count-1:
    line+=z
  else:
   line+=z+", "
  x,y=y,y+x#x is now equal to y and y adds itself to x
  i+=1
print(line)