---
layout : default
---

# Some random challenges
10-04-2019

It's not an official CTF. I just picked up some random challenges from internet to enhance my skills. As I don't have much 
time to explain the solutions in detail. Please co-operate with me this time. Challenges are not so much hard, but I learnt a lot while 
solving them.

## Challenge 1 (Network Forensics)

Download the [file](https://mega.nz/#!KaBmxBrK!O6HYpTJHrEKNHFhBapOGyT09Eod_SUN5g9TYfg_JFbQ). Analyse the file and follow the TCP stream 
from packet number 102 and you will get the following :

![Branching](https://raw.githubusercontent.com/r0hanSH/r0hanSH.github.io/master/images/random-challenges/ch1.JPG)

FLAG : flag{1M4p_1n_1Ns3cur3_m0d3_1s_s0_d4ng3roUS}

---

## Challenge 2 (Network Forensics)

Download the [file](https://mega.nz/#!CXAwHJgK!mzHMdbdfpjD3vMYxLcrvSkojDB4UzbWAF5SAmKigJCA). This challenge is an interesting challenge.
Analyse the file in WireShark. I saw some hex encoded values in the ICMP packets and this is what I got.

![Branching](https://raw.githubusercontent.com/r0hanSH/r0hanSH.github.io/master/images/random-challenges/ch2.JPG)

There are also some DNS packets. Observe the subdomains listed, so these are base64 encoded. Let's decode the first one and it gives PK 
which is the file signature of a zip file. So I got a zip file from there which was password protected and the password we already decoded
from the hex in ICMP packets.

FLAG : flag{Exf1ltr4t10n_ICMP_AnD_DNS_Tsh4rk_4_Ze_W1n}

---

## Challenge 3 (Network Forensics)

Download the [file](https://mega.nz/#!DW4QAAbb!_IcdyKe4ig7BWA1Qted5WtXRK6JnTHAmXmWGV6etmyU). Open in wireshark. See packet number 76. 
Save its content as key.pem . So I got key.pem and I see some TLS/SSL packets. So I tried to decrypt those packets and got the flag.

![Branching](https://raw.githubusercontent.com/r0hanSH/r0hanSH.github.io/master/images/random-challenges/ch3.JPG)

FLAG : ENSIBS{SSL_d3c0d1ng_1s_4w3s0me}

---

## Challenge 4 (Memory Forensics)

Download the [file](https://mega.nz/#!6LIAmIzA!-fglnfevwwGf17BW2-zQeulmax4-Lyt9GNda1HXSmy8). I analysed the memory dump with volatility.
Using the "filescan" plugin and grep the files on Desktop. I found a file named "confidential.pdf". Then I dumped that confidential.pdf
on my local computer and got the flag.

![Branching](https://raw.githubusercontent.com/r0hanSH/r0hanSH.github.io/master/images/random-challenges/ch4.JPG)

FLAG : ENSIBS{P0sT_m0rt3M_An4lyS1s_1s_s0_fUn}

---

## Challenge 5 (Network Forensics)

Download the [file](https://mega.nz/#!XCQhHTia!V2oG4kQh4gZuskM4k8MwEEIWD5KuOAk-Lu1p1Nt8uOg). Open the file in wireshark. Analyse it and 
got to know about USB protocol. See packet number 46 and we see "bstring: HID Keyboard". So we have to find the keystrokes used to 
write the flag using the keyboard. See "URB_INTERRUPT in" messages and "Leftover Capture Data field" which is 8 bytes long and I know 
which byte is for what purpose. You can learn it online. I don't remember the blog/book from where I learnt that months ago.

FLAG : ENSIBS{DucKy_k3yb04rD_c4PtUr3_w1th_l0v3}

---

## Challenge 6 (Network Forensics)

Download the [file](https://mega.nz/#!qfBjVaYA!u0nVsMph0nheYUs6AyL14EXpEPQP48VfmFXnsn5Gn6Y). Open the file in wireshark. I see ISAKMP
and ESP protocols. Follow the stream from packet number 77 to 88 and you get the following data, which is enough to decrypt these
ESP packets by adding the specific values at Edit > Preferences > Protocols > ESP and get the flag.

![Branching](https://raw.githubusercontent.com/r0hanSH/r0hanSH.github.io/master/images/random-challenges/ch6.JPG)

![Branching](https://raw.githubusercontent.com/r0hanSH/r0hanSH.github.io/master/images/random-challenges/ch6-2.JPG)

---

