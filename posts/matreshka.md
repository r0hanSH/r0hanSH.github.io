---
layout : default
---

# Matreshka (RE) CyBRICS CTF 2019
22-07-2019

I enjoyed this challenge. I don't have much time to explain everything about this challenge. So please enjoy the code :)

![Length of current folder name should be 17](https://raw.githubusercontent.com/r0hanSH/r0hanSH.github.io/master/images/cybrics/init.JPG)

```py
from Crypto.Cipher import DES


key = "matreha!"

arr = [76, -99, 37, 75, -68, 10, -52, 10, -5, 9, 92, 1, 99, -94, 105, -18]

cipherText = ""
for i in arr:
	cipherText += chr(i%256)

cipher = DES.new(key, DES.MODE_ECB)

stage2_key = cipher.decrypt(cipherText)

print "stage2_key = " + stage2_key


fd1 = open("data.bin", "rb")
data = fd1.read()
fd1.close()

cipher2 = DES.new(stage2_key[:8], DES.MODE_ECB)

elf_binary = cipher2.decrypt(data)

fd2 = open("stage2.bin", "wb")
fd2.write(elf_binary)
fd2.close()

print "Generated stage2.bin"

from os import system
print "Making stage2.bin executable"
system("chmod +x stage2.bin")


print "Reversing stage2.bin"

from pwn import *
p = process("./stage2.bin")
gdb_cmd=""
for i in range(0x11):
	gdb_cmd += "\nj *main.main+392\nc"

# yeah, you're right. I'm a lazy person :)
gdb.attach(p.pid, '''
file stage2.bin
info func
b *main.main+410
b *main.main+392
r
''' + gdb_cmd)
p.close()

print "Now we have result.pyc"
```

![Using uncompyle6](https://raw.githubusercontent.com/r0hanSH/r0hanSH.github.io/master/images/cybrics/pyc.JPG)

```py
from pwn import *
flag_format = "cybrics{"
enc = [40, 11, 82, 58, 93, 82, 64, 76, 6, 70, 100, 26, 7, 4, 123, 124, 127, 45, 1, 125, 107, 115, 0, 2, 31, 15]

def func(x, y):
	for i in range(256):
		if chr(i^x) == y:
			return i

key = ""
for j in range(len(flag_format)):
	key += chr(func(enc[j], flag_format[j]))

print "XOR key = " + key

enc = ''.join([chr(i) for i in enc])
flag = xor(enc, key)
print "flag = " + flag
```

FLAG  :  cybrics{M4TR35HK4_15_B35T}

---
