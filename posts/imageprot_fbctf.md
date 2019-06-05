---
layout : default
---

# FBCTF 2019
06-06-2019

Last weekend, I participated in fbctf. So here is my small writeup for ImageProt reverse engineering challenge. I wasted a lot of time on this single challenge, by not feeding a new line character to input but this mistake taught me a lot about JPEG file structure. Follow along to know more :

## ImageProt (RE)

![Branching](https://raw.githubusercontent.com/r0hanSH/r0hanSH.github.io/master/images/fbctf/desc.JPG)


This x86_64 binary was highly obfuscated with LLVM. So it's better to rely more on dynamic analysis. 

Run "strings" on this binary, you will notice some base64 encoded strings which upon decoding gives some weird(unprintable) text. 

```
Z3FcT3JfWlJfRw==
R15HWF5fQFM=
R1JURVBdRw==
WUdHRwscHFRZUl9bVF1UUkIdVVVSR1UZUlxeGEdSRltFbFpEblpdQ1RBXQ==
WUdHR0IJHBhZR0dHU1pdGV5BVBhCR1JDREAcAwAL
```

Open the binary in IDA and I see the scope of these base64 encoded strings. I found an interesting function "\_ZN9imageprot7decrypt17h56022ac7eed95389E" which takes three args. After analysing it, I found the following logic to decode these base64 encoded strings : 

```py
XOR( 'b64_encoded'.decode('base64'), '1337')
```

As you can see in the image, the args being passed to this function : 

![Branching](https://raw.githubusercontent.com/r0hanSH/r0hanSH.github.io/master/images/fbctf/2nd.JPG)

So these base64 encoded strings decodes to : 

```
Z3FcT3JfWlJfRw==    -> 		VBoxClient
R15HWF5fQFM=        -> 		vmtoolsd
R1JURVBdRw==        -> 		vagrant
WUdHRwscHFRZUl9bVF1UUkIdVVVSR1UZUlxeGEdSRltFbFpEblpdQ1RBXQ==    ->  http://challenges.fbctf.com/vault_is_intern

WUdHR0IJHBhZR0dHU1pdGV5BVBhCR1JDREAcAwAL        ->           https://httpbin.org/status/418
```

I have also found another base64 encoded string but on XORing it with '1337' gives nothing meaningful. To resume the execution, the binary connects to challenges.fbctf.com which is down so binary stops automatically.

So, we need to edit our /etc/hosts file and add the following : 

```
127.0.0.1	challenges.fbctf.com
```

Next step : 

```
localhost@red:~/Desktop/fbctf$ echo "ANYTHING" > vault_is_intern

localhost@red:~/Desktop/fbctf$ sudo python -m SimpleHTTPServer 80
Serving HTTP on 0.0.0.0 port 80 ...
127.0.0.1 - - [06/Jun/2019 02:45:14] "GET /vault_is_intern HTTP/1.1" 200 -

localhost@red:~/Desktop/fbctf$ ./imageprot
Welcome to our image verification and protection software!
This program ensures that malicious hackers cannot access our
secret images.
[+] Internal network connectivity verified.
thread 'main' panicked at '[-] Hacking tools found on this system, bailing.', src/main.rs:147:17
note: Run with `RUST_BACKTRACE=1` environment variable to display a backtrace.
```

Ok, we have bypassed one step. Next thing is to bypass this "Hacking Tools found..." thing. I used gdb to do some dynamic analysis and was able to bypass this step with some register values manipulation.

Now another thing that comes in my way is binary tries to connect to https://httpbin.org/status/418  but it was creating problems for me due to SSL(port 443). So I patched the binary by replacing the base64 encoded string "WUdHR0IJHBhZR0dHU1pdGV5BVBhCR1JDREAcAwAL" with "WUdHRwscHF9FR0NVWF0dWENUHERFUkdCQhwHBgk="  i.e. changing "https" to "http" to reduce my work load.

So, we bypassed this part too. Next thing is to decode the very big base64 encoded string but this time the XOR key was not "1337", but it's the content of "https://httpbin.org/status/418" . I got to know about this after analysing the last decrypt function using IDA and gdb.

But the real comes now, I copied the content of that webpage and XORed with that base64 encoded string, and I observed that this is a JPEG file with the help of its signature. After the completion of this XOR stuff, I got a JPG image but the corrupted one. At first I thought may be it's the challenge part and I have to recover this image. So I started doing some basic stuff to recover it and even edited it in hex editor, when I got to know it's having some problem with "Bogus Huffman table". But later I discovered my mistake of not provind a new line character to the XOR key, I don't regret for this mistake as I learnt a lot about JPEG structure in this challenge.

```py
import requests
from pwn import *

url = "http://httpbin.org/status/418"
r = requests.get(url)

key = r.text

fd = open("b64_string.txt")
data = fd.read()
fd.close()

fd = open("FLAG.jpg", "w")
fd.write( xor(key, data.decode('base64') ) )
fd.close()
``` 


![Branching](https://raw.githubusercontent.com/r0hanSH/r0hanSH.github.io/master/images/fbctf/flag.jpg)


FLAG : fb{Prot3ct_Th3_Gr4ph!1}

---
