---
layout : default
---

# Cisco SecCon CTF 2019
21-10-2019

After solving all the challenges in online quals of this CTF, I went to Bangalore for onsite finals. I managed to secure 5th rank but I should have done better if I had studied about RSA. So now a days, I'm working on my crypto skills. 

Quals (the scoreboard was hidden by organisers) :

![Branching](https://raw.githubusercontent.com/r0hanSH/r0hanSH.github.io/master/images/cisco/all_solved.JPG)


This challenge includes AES-CBC bit-flip attack and AES-CBC IV detection. This is one of the challenges in online quals. This is going to be my first crypto writeup. Enjoy :)

Provided script:

```py
#!/usr/bin/env python
import os
from Crypto.Cipher import AES
from Crypto.Util.number import *
from secret import FLAG

key1 = os.urandom(16)

class Unbuffered(object):
   def __init__(self, stream):
       self.stream = stream
   def write(self, data):
       self.stream.write(data)
       self.stream.flush()
   def writelines(self, datas):
       self.stream.writelines(datas)
       self.stream.flush()
   def __getattr__(self, attr):
       return getattr(self.stream, attr)

sys.stdout = Unbuffered(sys.stdout)

def pad(m):
    tmp=16-len(m)%16
    return m+chr(tmp)*tmp

def unpad(c):
    polarity = ord(c[-1])
    if polarity > 15: raise AssertionError("Incorrect Padding")
    return c[:-polarity]

def admin_decrypt(c) :
    cipher = AES.new(key1, AES.MODE_CBC, FLAG)
    return (cipher.decrypt(c))

def Encrypt(inp,iv):
    cipher = AES.new(key1, AES.MODE_CBC, iv)
    return (iv + cipher.encrypt(pad(inp))).encode('hex')

def Decrypt(c):
    c = c.decode('hex')
    iv,c = c[:16], c[16:]
    cipher = AES.new(key1, AES.MODE_CBC, iv)
    #from IPython import embed; embed()
    return unpad(cipher.decrypt(c))

def banner():
    TITLE = "Encryption/Decryption Service"
    print('=' * len(TITLE))
    print(TITLE)
    print('=' * len(TITLE))

    MENU = """
    1) Encrypt
    2) Decrypt
    3) Exit
    """
    print(MENU)


if __name__ == "__main__" :
    print(chr(27) + "[2J")
    count = 0
    while count < 3 :
        banner()
        ch = int(raw_input("Enter your choice :"))
        iv = os.urandom(16)
        if ch == 1 :
            m = raw_input("Enter the plaintext :")
            if 'admin' in m :
                print "Username can't be admin"
                continue # or break instead
            print Encrypt(m,iv)
            continue
        elif ch == 2 :
            c = raw_input("Enter the ciphertext(in hex) :")
            m = Decrypt(c)
            if m[:5] == "admin" :
                print "Welcome admin !"
                print "Admin decryption service :"
                ct= raw_input("Enter the ciphertext(in hex) :").decode('hex')
                if len(ct) > 32:
                    print("Ciphertext can't be greater than 32 bytes")
                    continue
                print admin_decrypt(ct)
            else :
                print m

        else:
            break

        count += 1
    print("See you next time!")

```

This challenge includes two things:

1. CBC bit-flip : Our goal is to find the ciphertext for plaintext "admin" to call ```admin_decrypt(ct)```. The service offers to give ciphertext of our plaintext. But we can't send "admin" as plaintext. We need to reach the "Admin decryption service" and it checks whether the first 5 bytes of decrypted plaintext is "admin". So we send "admiX" as plaintext and gets its ciphertext. Then we do XOR(cipher[4], 'X', 'n') and replace it with cipher[4]. So now we have ciphertext of plaintext "admin". 

2. CBC IV detection : So now we are admin. Next step is to find IV(Initialisation Vector) used to decrypt our ciphertext. Providing "\x00"\*16 as ciphertext gives decrypted plaintext. Now XOR(plain[:16], plain[16:]) gives the IV i.e. FLAG.  

```py
from pwn import *

r = remote('13.57.200.124', 1337)

print r.recv()
r.sendline('1')

print r.recv()
r.sendline('admiX')

enc = r.recvline().replace('\n', '')
enc = enc.split(':')[1]

print enc
tmp2 = enc

print r.recv()

r.sendline('2')
print r.recv()


enc = enc.decode('hex')

to_send = enc[:4] + xor(enc[4], 'X', 'n') + enc[5:]
to_send = to_send.encode('hex')

r.sendline(to_send)

print r.recvuntil("Enter the ciphertext(in hex) :")

# Got admin

tmp2 = '00'*32

r.sendline(tmp2)

t = r.recv()


flag = xor(t[:16], t[16:])

print "SecConCTF{" +flag + "}"
```

![Branching](https://raw.githubusercontent.com/r0hanSH/r0hanSH.github.io/master/images/cisco/flag_cbc.JPG)

FLAG: SecConCTF{U_5ur3_c4n_flip!}

---