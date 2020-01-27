---
layout : default
---

# Cipher Combat HackerEarth 2020
26-01-2020

This CTF was far better than the last year's cipher combat. Thanks to HackerEarth team for organizing such CTFs.
I don't have much time to explain everything about all the challenges. I will only discuss two challenges, but leave brief info about other remaining challenges so that you can solve them on your own. For any queries, you can contact me on twitter or e-mail.


## Lost Cred

We need to form a raw request on our own, it required some guess work :)

![HE1](https://raw.githubusercontent.com/r0hanSH/r0hanSH.github.io/master/images/hackerearth-cipher-combat/he1.JPG)

FLAG: HE{eCC82cC8CB5fef277401a0A787d1CE1b9f65644F4ef956d5AEfC9fa63A21c842}


That's it we got the flag. It's not over yet. I was not able to solve "Bruted" challenge. As it was unsolvable without knowing the **secret**. The source code was completely secure. One thing I noticed that all web challenges were hosted on same server machine. So I thought of doing some unintentional.

See below, I was trying to exploit "Bruted" challenge using the XXE vuln of "Lost Cred". I was also able to ping my own server. I had an idea of hosting a malicious DTD on my server and then getting Remote Code Execution on system, but in that case we need to escape from docker container.

![HE2](https://raw.githubusercontent.com/r0hanSH/r0hanSH.github.io/master/images/hackerearth-cipher-combat/he2.JPG)

I was able to leak some AWS related info. I could try to exploit it further and leak admin credentials. But I think Amazon have already patched their services (you can read about it [here](https://aws.amazon.com/blogs/security/defense-in-depth-open-firewalls-reverse-proxies-ssrf-vulnerabilities-ec2-instance-metadata-service/)) and also it's against the rules of this CTF. So I skipped that part.

![HE3](https://raw.githubusercontent.com/r0hanSH/r0hanSH.github.io/master/images/hackerearth-cipher-combat/he3.JPG)

---

## Reverse Master

I reverse engineered first 3 binaries and found out following pattern: 

```
6000C9  Operation (add, sub or xor)
6000CC  cmp with result
```

You could use pwntools to write well-optimized code. I did it with objdump and pure python.

```py
fd = open("ll")
l = fd.readlines()
fd.close()

flag = ""

for i in range(0, len(l),2):
	tmp = l[i]
	intval1 = int(l[i].split(',')[1], 16)
	cmpval1 = int(l[i+1].split(',')[1], 16)
	if "add" in tmp:
		flag += chr(cmpval1 - intval1)
	elif "sub" in tmp:
		flag += chr((cmpval1 + intval1)%256)
	else: # xor
		flag += chr(cmpval1 ^ intval1)

print flag
```

![HE4](https://raw.githubusercontent.com/r0hanSH/r0hanSH.github.io/master/images/hackerearth-cipher-combat/he4.JPG)

FLAG: HE{6586C7Fdbae82C4877f57f0A7386f578ACc69737fF8293Ab1F851BA0b6Ee0C74}

---

Brief info about other challenges:

### Three-words

```
root@localhost:/threewords# export racker=talkative
root@localhost:/threewords# ./threewords mainstream
congrats!! you got your 3 words

HE{talkative_racker_mainstream}
```

### Shifter

```py
given = "rf.bo'b/$ke"
for i in range(1,0xc):
	f += chr(i+ord(given[i-1]))
print f
'sh1ft-i7-up'
```

HE{sh1ft-i7-up}


### 2FA-Trouble

Leak source code using ```/index.php/php://filter/convert.base64-encode/resource=vault```

Found SQLi and enumerated further to find valid username:
```
X-Forwarded-For: 208.88.84.1
Authorization: Basic bmFtZScgb3IgJzEnPScyJyBVTklPTiBTRUxFQ1QgJ0phbTNzQjBuZCcsJzVmNGRjYzNiNWFhNzY1ZDYxZDgzMjdkZWI4ODJjZjk5Jy0tOnBhc3N3b3Jk
```

HE{wh4t_y0u_br0k3_Da_vAuLt_4ga1n}


### Braden

Use **StegSolve** (Red Plane 0), you will see another image. Save that image and then use OCR to dump the content in text format. The esoteric language was **ReverseFuck**, run the code and get the flag.

HE{br4inst3gogr4phed}


### My Fav Song

Used Audacity to analyse the file. Found morse code and translated it to ASCII. Found a pastebin link (https://pastebin.com/QZZAUGPZ)

HE{4ud10_fil3s_c4n_h1d3_d4t4}


### Merge-Me

```cat `ls` > x.pcap```

Open x.pcap in wireshark, analyse FTP communication.

HE{$up3r$3cr3Tu$3R}


### Lame Virus

Given exe was UPX-compressed. Decompress it using official upx decompressor. Then analyse decompressed exe and get the flag.

HE{an0th3er_cl4ssic_m4lwar3}


### Crack Network

```aircrack-ng -w rockyou.txt crack-the-network.cap```

Found password: budaksetan

HE{budaksetan}


### NoTe

```mv challenge.odt challenge.zip; 7z x challenge.zip```

Go to Pictures folder and found jpg image having base64 encoded flag.

HE{h1dd1ng_1nf0_1n_s3cr3t_pl@c3}


### Scroll-Dispatched

Thanks to organizers for releasing last minute hint (Use CrypTool). Initially, I knew it's scytale cipher but was not able to decipher it. I tried all possible keys from 1 to 28 but found nothing.

Use CrypTool -> Scytale Cipher with number of turns=5, you will get another base64 encoded string.

```
root@localhost:~# echo SEV7aTdfbjNWZXJfZzN0c18wbGR9 | base64 -d
HE{i7_n3Ver_g3ts_0ld}
```

---
