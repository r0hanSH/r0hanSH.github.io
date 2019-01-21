---
layout : default
---

# InCTF and VMware CTF Forensics
21-01-2019

I will share writeups for two forensics challenges, which I solved during InCTF quals (only 4 teams were able to solve it) and onsite VMware CTF (around 3 individuals solved it).

## InCTF challenge

![Branching](https://raw.githubusercontent.com/r0hanSH/r0hanSH.github.io/master/images/InCTF-VMware-CTF/problem-inctf.png)

Read the problem statement carefully, the victim downloaded malware. So my initial steps were :
1. Check Downloads directory
2. Find the browser present on system

So we were provided with memory dump of a computer system, and we can use **volatility** tool to analyze this memory dump.

```
C:\Users\r0hanSH\Downloads\Challenge>volatility.exe -f Challenge.raw imageinfo
Volatility Foundation Volatility Framework 2.6
INFO    : volatility.debug    : Determining profile based on KDBG search...
          Suggested Profile(s) : Win7SP1x86_23418, Win7SP0x86, Win7SP1x86
...
```

Then check processes

```
C:\Users\r0hanSH\Downloads\Challenge>volatility.exe -f Challenge.raw --profile=Win7SP1x86_23418 pslist
Volatility Foundation Volatility Framework 2.6
Offset(V)  Name                    PID   PPID   Thds     Hnds   Sess  Wow64 Start                          Exit
---------- -------------------- ------ ------ ------ -------- ------ ------ ------------------------------ ------------------------------
0x83d09c58 System                    4      0     84      496 ------      0 2018-12-02 14:26:26 UTC+0000
0x84430020 smss.exe                260      4      2       29 ------      0 2018-12-02 14:26:26 UTC+0000
0x84c3e7f8 csrss.exe               340    332      9      368      0      0 2018-12-02 14:26:31 UTC+0000
...
...
0x84ff1d20 chrome.exe             2300   1004     39      887      1      0 2018-12-02 14:32:44 UTC+0000
...
```

So we can see a lot of processes are there, but interesting one is chrome.exe . So we can assume the victim was using Chrome browser to download the malware. So what can we do ? During CTF, I dumped chrome's history files. But later I came to know volatility has chromehistory plugin available.

With filescan plugin I searched for history files of chrome and dumped onto my local machine. After checking the content of dumped files, I come across this [link](https://mega.nz/#!jj4TRK4I!GS5PWWXZpbpTaXZU5LPdOldxAlXE_UkHDjhnIbYo2ckimage/pngimage/png) which contains a file called Image.png

So now comes steganography part, I opened Image.png but it was not a picture at all, it was plain ASCII text. After analysing the content, I came to know it's in hex. Starting content was
```
504B0304
```

It's the file signature of a zip file.

```
localhost@r0hanSH:~$ xxd -r -p Image.png > file.zip
```

The file.zip was protected with password. So I tried fcrackzip to crack the password using different wordlists but nothing worked. So again, I started anaylising the memory dump. Next thought was what could be the password? Could it be the password of local user?

```
C:\Users\r0hanSH\Downloads\Challenge>volatility.exe -f Challenge.raw --profile=Win7SP1x86_23418 hashdump
Volatility Foundation Volatility Framework 2.6
Administrator:500:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
hello:1000:aad3b435b51404eeaad3b435b51404ee:a0ce834dafdfabf08cc996ba5a6bba31:::
```

Decrypting the NTLM hash of user "hello" gives zip password "inctfiseasy". After unzipping the file.zip, we got another file named "hex" which also contains plain ASCII text with starting content "474946383961" and that's the file signature of a GIF file.

```
localhost@r0hanSH:~$ xxd -r -p hex > flag.gif
```

The speed of gif was very high, so I opened it in GIMP and see individual layers and came across this.

![Branching](https://raw.githubusercontent.com/r0hanSH/r0hanSH.github.io/master/images/InCTF-VMware-CTF/first-part-of-flag.png)

So now we got first part of the flag. Let's hunt for second part. After a lot effort, I found this in environmental variables.

```
C:\Users\r0hanSH\Downloads\Challenge>volatility.exe -f Challenge.raw --profile=Win7SP1x86_23418 envars
Volatility Foundation Volatility Framework 2.6
Pid      Process              Block      Variable                       Value
-------- -------------------- ---------- ------------------------------ -----
     260 smss.exe             0x001907f0 Path                           C:\Windows\System32
     260 smss.exe             0x001907f0 SystemDrive                    C:
...
...
     340 csrss.exe            0x002c07f0 The Final Part                 6D795F7730726C645F30665F6D336D3072597D
     340 csrss.exe            0x002c07f0 The Hacker                     My NTLM can crack anything
     340 csrss.exe            0x002c07f0 TMP                            C:\Windows\TEMP
     340 csrss.exe            0x002c07f0 USERNAME                       STARK
...
```

```
localhost@r0hanSH:~$ echo 6D795F7730726C645F30665F6D336D3072597D | xxd -r -p
my_w0rld_0f_m3m0rY}
```

Finally, we got the flag **inctf{w3lcom3_t0_my_w0rld_0f_m3m0rY}**

## VMware CTF

It may seems easy but it wasn't. I don't have files available right now. So I will be explaining the methodology I followed but important thing is to learn this technique.

We were provided with a zip file say flag.zip
But it was password protected, so I cracked it using fcrackzip along with rockyou.txt . I don't remember the password right now but it was having word "rain" in it. It will help later on.

So now I got a PDF file, real hunt begins now. I tried everything I know. But outcome was 0. I noticed that word "rain" in zip file password. Why would one make a zip file password protected, when there are good hackers and everyone of them knows how to crack zip password ? So I used google to know what technique it could. After a lot of effort, I got to know about [**SNOW**](http://www.darkside.com.au/snow/) tool. So this was a Whitespace steganography challenge and used **SNOW** to get the flag.
```
./snow -C flag.pdf
```

---
