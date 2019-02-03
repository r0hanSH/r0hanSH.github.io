---
layout : default
---

# Nullcon 2019 - CAT challenge
04-02-2019

Due to some personal reasons, I could not play the CTF for whole 36 hours. But somehow I managed to get **first blood** on "cat" challenge (Forensics).

We were given a file called "final"

```
localhost@red:~/Desktop/nullcon/cat$ file final
final: UTF-8 Unicode text, with very long lines, with no line terminators

```

Let's open the file. You will see a lot of cats. So what it is? After some research, I came to know it's an esoteric language called "unicat"

```
😻😹😸🙀😹😹😻😻🙀😹😽😼😸🙀🙀😻😹😸🙀😹😽😸🙀😹😽😼😸🙀🙀😻😹😸🙀😹😼😿🙀😹😽😼😸🙀🙀😻😹😸🙀 ...
...
```

So now the question is "how to see this content in ASCII text?". Let's see who created this language and I found a [github repo](https://github.com/gemdude46/unicat)

Let's analyse the "cat.py" file in that github repo. It converts unicat code to plain ASCII text. Here 'x' file in screenshot, contains a simple "Hello, World!" program. I will tell you why I created it.

![Branching](https://raw.githubusercontent.com/r0hanSH/r0hanSH.github.io/master/images/nullcon19/output1.png)

See the difference between both the outputs. This means "final" has something wrong with it.
Now I have two choices :
1. Learn unicat. See how "cat.py" actually works.
2. See the difference between "Hello, World!" program and "final"

I went with second choice. In "cat.py", you will see a list called "ins". Let's print its content for both the programs.
For **final**, see above picture

For **Hello, World!**

![Branching](https://raw.githubusercontent.com/r0hanSH/r0hanSH.github.io/master/images/nullcon19/output2.png)

So do you see any difference here? This is just implementing simple things like assignment, printing etc.

After some research, I got to know that 'diepgrm' tells the program to end. So you see ('diepgrm',) is present at index 1 of 'ins' list in "final". So let's change its position and run the following code.

```
import sys, random

mem={}
ins = [('inputst',1),('asgnlit', 1, 1),('asgnlit', 4, 1),('asgnlit', 10, 7),('echoval', 2),('pointer',4,4),('echoval',4),('applop+', 10, 1),('echoval',10),('asgnlit', 2, 72),('applop*', 2, 10),('echoval',2),('asgnlit', 0, 108), ('echovar', 0),('asgnlit', 0, 108), ('echovar', 0),('asgnlit', 0, 65), ('echovar', 0),('asgnlit', 0, 119), ('echovar', 0),('asgnlit', 0, 69), ('echovar', 0),('asgnlit', 0, 115), ('echovar', 0),('asgnlit', 0, 48), ('echovar', 0),('asgnlit', 0, 109), ('echovar', 0),('asgnlit', 0, 69), ('echovar', 0),('asgnlit', 0, 95), ('echovar', 0),('asgnlit', 0, 67), ('echovar', 0),('asgnlit', 0, 64), ('echovar', 0),('asgnlit', 0, 84), ('echovar', 0), ('diepgrm',)]

while True:
    mem[-1]=mem.get(-1,-1)+1
    try: it = ins[mem[-1]]
    except IndexError: it = ("asgnlit",-1,-1)
    if it[0] == "diepgrm":
        sys.exit()
    if it[0] == "pointer":
        mem[it[1]]=mem.get(mem.get(it[1],0),0)
    if it[0] == "randomb":
        mem[it[1]]=random.randint(True,False)
    if it[0] == "asgnlit":
        mem[it[1]]=it[2]
    if it[0] == "jumpif>" and mem.get(it[1],0) > 0:
        mem[-1]=it[2]
    if it[0] == "applop+":
        mem[it[1]]=mem.get(it[1],0)+mem.get(it[2],0)
    if it[0] == "applop-":
        mem[it[1]]=mem.get(it[1],0)-mem.get(it[2],0)
    if it[0] == "applop/":
        mem[it[1]]=mem.get(it[1],0)/mem.get(it[2],0)
    if it[0] == "applop*":
        mem[it[1]]=mem.get(it[1],0)*mem.get(it[2],0)
    if it[0] == "echovar":
        sys.stdout.write(unichr(mem.get(it[1],0)))
    if it[0] == "echoval":
        sys.stdout.write(str(mem.get(it[1],0)))
    if it[0] == "inputst":
        inp = sys.stdin.readline()
        for k in range(it[1],it[1]+len(inp)):
            mem[k]=ord(inp[k-it[1]])
        mem[k+1]=0
```

```
localhost@red:~/Desktop/nullcon/cat$ python cat.py 
anything
11018576llAwEs0mE_C@T
```
Remove initial '11' from output. It happened due to "('inputst',1)".

# FLAG: hackim19{018576llAwEs0mE_C@T} 

---
