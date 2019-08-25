---
layout : default
---

# Codefest CTF 2019 (RE)
25-08-2019

Enjoy the code with little explanation

## Linux RE 1 (300)

The binary was packed with UPX, so first unpack it.

```
upx -d run -o run_no_upx
```

It has debugger detector code in it, so we need to bypass it. To bypass debugger detection, for first ```ptrace``` function, it should return ```0``` and for second ```ptrace``` function it should return ```-1```

So after analysing ```rahasya``` function in binary, I found the key 


```py
from pwn import xor

a="P]" + chr(3) + "C" + chr(3) + "V\vn@" + chr(2) +"Z"+ chr(27) + "T" + chr(28)+ "nK" + chr(3) + "E4" + chr(6) +"\v" + chr(5) + "PXZX"

key = "1337key"

print xor(a, key)
```

```sh
localhost@red:~/Desktop/fest$ ./run_no_upx an0th3r_s1mp1e_x0r_cr4ckm3
[+] Correct Password
```

FLAG: CodefestCTF{an0th3r_s1mp1e_x0r_cr4ckm3}

## Linux RE 2 (500)

I love angr, it was a simple crackme

```py
import angr

p = angr.Project("./chall2")
state = p.factory.entry_state()
simgr = p.factory.simgr(state)

simgr.explore(find = lambda simgr: "Congratulations! Correct password!" in simgr.posix.dumps(1), avoid = lambda simgr: "Sorry! Wrong password!" in simgr.posix.dumps(1))

sol_state = simgr.found[0]
flag = sol_state.posix.dumps(0)

print flag
```

```sh
localhost@red:~/Desktop/fest$ ./chall2
shouldve_used_some_tool
Congratulations! Correct password!
```

FLAG: CodefestCTF{shouldve_used_some_tool}

## Windows RE (500)

```sh
localhost@red:~/Desktop$ file verifier.exe 
verifier.exe: PE32 executable (GUI) Intel 80386 Mono/.Net assembly, for MS Windows
```

Let's open it in dnSpy, I analysed this executable and ```Decrypt``` seems interesting. Let's see what ```Decrypt``` function returns.

![Image not found](https://raw.githubusercontent.com/r0hanSH/r0hanSH.github.io/master/images/codefest/1.JPG)

So here I found, Target[0] = 'M', Target[1] = 'Z' ... Target[128] = 'P', Target[129] = 'E'

So the executable is packed, let's unpack it. I dump the content of ```Target``` and got an unpacked executable. Simply opening it in dnSpy, revealed the password and flag.

![Image not found](https://raw.githubusercontent.com/r0hanSH/r0hanSH.github.io/master/images/codefest/2.JPG)

FLAG: CodefestCTF{51mp13_1npu7_v411d4710n_8u7_w17h_4_7w157}

---
