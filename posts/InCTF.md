---
layout : default
---

# InCTF 2019
23-09-2019

## TIC_TAC_TOE (RE)

It was a 4x4 tic-tac-toe game. Even after winning the game, you don't get flag. So I analysed the disassembly and got to know if game is 
draw between you and machine, it calls an interesting function.
Enjoy the code

```py
import angr
import claripy

p = angr.Project("/bin/true")
state = p.factory.entry_state()

flag_nums = [claripy.BVS("flag_%d" % i, 64) for i in range(16)]

xor_key = '!@#sbjhdn5z6sf5gqc7kcd5mck7ld=&6'

for i in range(0, 16, 2):
	state.solver.add(flag_nums[i] >= 0xa, flag_nums[i] <= 0x19)
	state.solver.add(flag_nums[i+1] >= 0x1a, flag_nums[i] <= 0x29)

tmp1 = []
for i in flag_nums:
	tmp1.append(i*8)
	tmp1.append(i*7)

check = []
for i in range(len(xor_key)):
	check.append( ord(xor_key[i]) ^ tmp1[i] )

a1 = [0x9b, 0xcf, 0x1db, 0x1b9]
a2 = [0xf9, 0x174, 0x27f, 0x1a7]
a3  = [0xCE, 0xB1, 0xA, 0x1B]
a4 = [0xBF, 0x9B, 0x1F1, 0x7E]
a5 = [0x37, 0x5D, 0x11D, 0x14B]
a6 = [0x104, 0x1B3, 0x3A4, 0x22A]
a7 = [0xAD, 0xB7, 0x99, 0x9E]

a8 = [0xC9, 0x0E1, 0x121, 0x169, 0x1A, 0x0D, 0x0A1, 0x7F, 0x7, 0x9, 0x157, 0x116, 0x0B9, 0x0B8, 0x15D, 0x86, 0x8C, 0x0DF, 0x161, 0x0B3, 0x0FFFFFFF8, 0x0FFFFFFEF, 0x167, 0x80, 0x17, 0x0FFFFFFF6, 0x119, 0x79, 0x84, 0x82, 0x66, 0x9A]

for i in range(len(tmp1)):
	state.solver.add(tmp1[i] <= 400)

for i in range(4):
	state.solver.add(check[i]^check[i+4] == a1[i])
	
	state.solver.add(check[i+8] + check[i+8+4] == a2[i])

	state.solver.add(check[i+8*2] - check[i+ 8*2 +4] == a3[i])

	state.solver.add(check[i+8*3] ^ check[i+ 8*3 +4] == a4[i])

	state.solver.add(check[i+ 8*3 +4] ^ check[i] ^ check[i+4] == a5[i])

	state.solver.add(check[i+ 8*2 +4] + check[i+8] + check[i+8+4] == a6[i])

	state.solver.add(check[i+8] ^ check[i] ^ check[i+4] == a7[i])

flag_tiles = [state.solver.eval(i) for i in flag_nums]

print flag_tiles[::]

tmp2 = []
for i in flag_tiles:
	tmp2.append(i*8)
	tmp2.append(i*7)
flag = ""
for i in range(len(tmp2)):
	tmp3 = tmp2[i] ^ (i + a8[i])
	if tmp3 > 127:
		flag += 'X'
	else:
		flag += chr(tmp3)
	
print flag
```

Few chararcters were missing, but we can find it using ```state.solver.max()``` and test them. But while passing result of
```flag_tiles``` to program running inside debugger, it gives us flag.

![Branching](https://raw.githubusercontent.com/r0hanSH/r0hanSH.github.io/master/images/inctf-19/flag.JPG)

FLAG : inctf{w0W_Y0u_cr4ck3d_my_m3th0d}

---


