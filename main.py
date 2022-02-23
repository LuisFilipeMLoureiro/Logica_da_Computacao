import sys



arg = []
for elements in sys.argv:
    if elements != "main.py":
        arg.append(elements)

word = "".join(arg)
word = word.replace(" ", "").strip("").strip('')


numbers = ["1", "2", "3", "4", "5", "6","7", "8","9","0"]
op = ["+","-"]
num = "0"

or_numb0 = []
or_op = []

if word[0] not in op:
    for i in word:
        if i in numbers:
            num += i  
        elif i in op:
            or_numb0.append(int(num[1:]))
            num = "0"
            or_op.append(i)
        else:
             sys.stderr.write("This is error msg1")


    
    or_numb0.append(int(num))

else:
    sys.stderr.write("This is error msg2")
            

or_numb = []

for i in or_numb0:
    if i != 0:
        or_numb.append(i)


tot = or_numb[0]
t = 0


for numero in or_numb[1:]:
    if or_op[t] == "+":
        tot += numero
        
    else:
        tot-=numero 

    if t<len(or_op)-1:
        t+=1






if len(or_numb) == 0 or len(or_op) == 0 or len(or_numb[1:]) == 0:
    sys.stderr.write("This is error msg3")
else:
    print(tot)

