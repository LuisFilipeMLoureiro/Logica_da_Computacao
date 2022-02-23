import sys



arg = []
for elements in sys.argv:
    if elements != "main.py":
        arg.append(elements)

word = "".join(arg)
word = word.strip().strip("").strip('')

numbers = ["1", "2", "3", "4", "5", "6","7", "8","9","0"]
op = ["+","-"]
num = "0"

or_numb = []
or_op = []

if word[0] not in op:
    for i in word:
        if i in numbers:
            num += i
        elif i in op:
            or_numb.append(int(num))
            num = "0"
            or_op.append(i)
    
    or_numb.append(int(num))

else:
    sys.stderr.write("This is error msg")
            

    

tot = or_numb[0]
t = 0
for numero in or_numb[1:]:
    if or_op[t] == "+":
        tot += numero
    else:
        tot-=numero 

    if t<len(or_op)-1:
        t+=1






if len(or_numb) == 0 or len(or_op) == 0 or (len(or_numb)==1 and (len(or_op))):
    sys.stderr.write("This is error msg")
else:
    print(tot)

#for elemento in sys.argv[1]:
