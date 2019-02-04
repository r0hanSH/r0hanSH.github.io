---
layout : default
---

# BITSCTF 2019
05-02-2019

I played this CTF individually and ended up 6th on final scoreboard(x86)

NOTE : This will be a really quick writeup. **No time for full description**. If you have any doubts, you can mail me.

![Branching](https://raw.githubusercontent.com/r0hanSH/r0hanSH.github.io/master/images/bitsctf/scoreboard.png)


## SPIFF (Forensics)

![Branching](https://raw.githubusercontent.com/r0hanSH/r0hanSH.github.io/master/images/bitsctf/ch1.png)

```
localhost@red:~/Desktop/BITS$ file SPIFFED
SPIFFED: data

localhost@red:~/Desktop/BITS$ xxd -l 20 SPIFFED
00000000: 60fa 2c00 220b 0102 1000 023d 5e00 435c  `.,."......=^.C\
00000010: 91e4 525c 

localhost@red:~/Desktop/BITS$ strings -n7 SPIFFED | grep '\w\.\w\w\w$'
file.arj
file_0.txt
file_1.txt
file_2.txt
file_3.txt

```

Change file signature to "60ea" and got SPIFFED.arj
Then I extracted it and got 4 files (file_0.txt to file_3.txt). Read the challenge description carefully. I wasted a lot of time in this step. I misunderstood SPIF with SPIFF(Still Picture Interchange File Format) but also learnt a lot about it.
Let's google "Mr.Zeus spif github" and found this [github repo](https://github.com/MrZeusGaming/SPIF-image-encryption)

```
localhost@red:~/Desktop/BITS/SPIF-image-encryption$ python3 SPIF.py decrypt file_2.txt DETF.py 

```

![Branching](https://raw.githubusercontent.com/r0hanSH/r0hanSH.github.io/master/images/bitsctf/flag1.png)

FLAG : BITSCTF{1_L0v3_D0g5_D0_Y0u??}

---

## I want it plain (Crypto)

![Branching](https://raw.githubusercontent.com/r0hanSH/r0hanSH.github.io/master/images/bitsctf/ch2.png)

It's bifid cipher

![Branching](https://raw.githubusercontent.com/r0hanSH/r0hanSH.github.io/master/images/bitsctf/flag2.png)

FLAG : BITSCTF{differentperiodsdifferentresults}

---

## Math check (Programming)

Simple C program was given, changed it little bit and got the flag

FLAG : BITSCTF{M0DUL4R_M4G1C!}

---

## Sanity check (web)

base64 encoded string on website

FLAG : BITSCTF{w3lc0m3_70_70p_1_p3rc3n7}

---

## Easy points (web)

```
localhost@red:~/Desktop/b/easy-points-done$ url=$(dig -t txt bitsctf.cf | grep TXT | grep '"' | cut -d'"' -f2 | base64 -d);cat | curl -v https://bitsctf.cf$url | grep -i flag

```

FLAG : BITSCTF{7h15_w45_345y_dn5}

---

## I hate normal (web)

![Branching](https://raw.githubusercontent.com/r0hanSH/r0hanSH.github.io/master/images/bitsctf/ch3.png)

Visit that url and you will see "... its best viewed on latest safari on windows 10"
Change User-Agent and get the flag

![Branching](https://raw.githubusercontent.com/r0hanSH/r0hanSH.github.io/master/images/bitsctf/flag3.png)

FLAG : BITSCTF{m3551n6_4r0und_u53r_463n75}

---

## Insanity check (web)

Execute the following and get the flag

![Branching](https://raw.githubusercontent.com/r0hanSH/r0hanSH.github.io/master/images/bitsctf/ch4.png)

![Branching](https://raw.githubusercontent.com/r0hanSH/r0hanSH.github.io/master/images/bitsctf/flag4.png)


FLAG : BITSCTF{y0u_4r3_r34lly_p4713n7}

---

## Sneaky (web)

![Branching](https://raw.githubusercontent.com/r0hanSH/r0hanSH.github.io/master/images/bitsctf/ch5.png)

FLAG : BITSCTF{w0w_7h47_w45_5n34ky}

---

## Dox him (web, recon)

Challenge description says "find the author of web challenges and his youtube account's description have flag encoded in base64". I found this guy from his comment at [CTFtime](https://ctftime.org/event/745) See last comment of mehulmpt there and his twitter account have link to his youtube channel.

![Branching](https://raw.githubusercontent.com/r0hanSH/r0hanSH.github.io/master/images/bitsctf/ch6.png)

FLAG : BITSCTF{d0n7_f0r637_70_5ub5cr1b3}

---

## Me=Ur_frnd (RE)

.pyc file was provided. Use [this tool](https://github.com/Mysterie/uncompyle2) and get python code. After analysing python code, I found that we just need to decrypt the md5 hashes and I did the same.

![Branching](https://raw.githubusercontent.com/r0hanSH/r0hanSH.github.io/master/images/bitsctf/ch7.png)

FLAG : BITSCTF{unc0mpyl3_kn0w5_wh47_1_wr073_s0_s4d}

---

## Hungry For Flag (RE)

An ELF binary was given. After analysing binary, I found the flag length is 39 and the "cmp al, bl" is our target.

![Branching](https://raw.githubusercontent.com/r0hanSH/r0hanSH.github.io/master/images/bitsctf/ch8.png)

In gdb, I gave "BITSCTF{AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA}" as input and set two breakpoints at "main"  and "main+591"

FLAG : BITSCTF{B1n4r13s_533M_h4rD_Bu7_4r3_n0T}

---

