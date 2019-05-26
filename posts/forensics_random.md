---
layout : default
---

# Forensics Challenges
27-05-2019

While reading the writeups published by CTF team bi0s, I came across the github profile of Abhiram. There I saw [Forensics-Workshop](https://github.com/stuxnet999/Forensics-Workshop) repo, it contains 10 challenges and I managed to solve all of them. 


## Challenge 1

```
### Description

Marty thinks there is some interesting string in this image. Can you help him in finding it???

### Difficulty level

Easy
```

I got an image chall.png . It was simple just run strings on it. 

```
strings chall.png | tail -n 1 | base64 -d
```

FLAG : flag{5trings_1S_in7er3s7inG}


## Challenge 2

```
### Description

While recovering a drive, Sam found an image file. He tried to open it, but could not. Can u help him in opening it.

### Difficulty level

Easy
```

I got a PNG file which was corrupted.

```
localhost@red:~/Desktop/Forensics-Workshop/Challenge 2$ pngcheck -v chall.png 
File: chall.png (149159 bytes)
  chunk IHdR at offset 0x0000c, length 13:  first chunk must be IHDR
ERRORS DETECTED in chall.png
```

Open it in hex editor and recover the correct image.

![Branching](https://raw.githubusercontent.com/r0hanSH/r0hanSH.github.io/master/images/forensics_random/chal_2.png)

FLAG : flag{pro7ec7_y0ur_Chunk5_Dud3}


## Challenge 3

```
### Description

Jim found a file in his friend computer. He suspects that there is something hidden in it. Can you help him in finding it.

### Difficulty Level

Medium
```

I got a password protected ZIP file. Run the following command :

```
localhost@red:~/Desktop/Forensics-Workshop/Challenge 3$ strings chall.zip | tail -n 1 | cut -d':' -f2 | xxd -r -p
this_is_the_password
```

So we got the password for ZIP file. After extraction, I got chall.jpg

```
binwalk -e chall.jpg
```

Not I have another file flag.txt

```
localhost@red:~/Desktop/r$ cat flag.txt 
Sorry, no flag here. Try harder. Every thing may be useful.

©Jim - 2966a8cd9d57fe22f7f98d68d7745d4f
```

So here we have md5 hash, I cracked it using md5decrypt.net and got "{N0t_tH3_flaG_bu7_us3Ful}"

```
localhost@red:~/Desktop/Forensics-Workshop/Challenge 3$ steghide extract -sf chall.jpg -p {N0t_tH3_flaG_bu7_us3Ful}
wrote extracted data to "realflag.txt".

localhost@red:~/Desktop/Forensics-Workshop/Challenge 3$ cat realflag.txt 
flag{Y0u_L3arned_4ll_t00l5}
```

FLAG : flag{Y0u_L3arned_4ll_t00l5}


## Challenge 4


```
### Descrition
Jon found a file in his trash, he knows that something was hidden in that. Can you help him in finding what is there in it?

Difficulty Level

Medium
```


Run strings on provided file and you will see "flag.jpg". Run  binwalk on it and you will get a password protected zip file.

```
localhost@red:~/Desktop/Forensics-Workshop/Challenge 4$ strings chall.png | tail -n 1 | base64 -d
flag{w3ll_7ry_n0_flag_but_us3ful}
```

So the password is "flag{w3ll_7ry_n0_flag_but_us3ful}" and we got the flag.

FLAG : flag{D0n't_b3_s3riou5}

## Challenge 5

```
### Description
Tom and Jerry are fighing as usual. The one who gets the flag is the winner. Jerry is running to find the flag. Help him find it.

### Difficulty

Medium
```

Two files were given Jerry.jpg and flag.txt

```
localhost@red:~/Desktop/Forensics-Workshop/Challenge 5$ cat flag.txt 
Hehe , it's not that easy to get the flag :)
notflag{Y0u_c4n't_g3t_it}

localhost@red:~/Desktop/Forensics-Workshop/Challenge 5$ steghide extract -sf Jerry.jpg -p "notflag{Y0u_c4n't_g3t_it}"
wrote extracted data to "final_flag.txt".

localhost@red:~/Desktop/Forensics-Workshop/Challenge 5$ cat final_flag.txt 
NjY2YzYxNjc3YjY2Njk2ZTM0NmM2Yzc5NWY3OTMwNzU1ZjY3MzA3NDVmNzQ2ODMzNWY2NjZjMzQ2Nzdk

localhost@red:~/Desktop/Forensics-Workshop/Challenge 5$ cat final_flag.txt | base64 -d | xxd -r -p
flag{fin4lly_y0u_g0t_th3_fl4g}
```

FLAG : flag{fin4lly_y0u_g0t_th3_fl4g}


## Challenge 6

```
### Description

Just a simple challenge to find the flag.

### Difficulty

Easy
```

We got a file hacker.png

```
localhost@red:~/Desktop/Forensics-Workshop/Challenge 6$ exiftool hacker.png | grep Comment | cut -d':' -f2 | xxd -r -p | base64 -d
flag{h4ck3rs_4r3_3v3rywh3r3}
```

FLAG : flag{h4ck3rs_4r3_3v3rywh3r3}


## Challenge 7

```
### Difficulty level

Hard

### Description

You might have never seen this much obfuscation till now. Be patient to get the flag.
```

dotfiles were present. Check it with "ls -a" in linux. base64 encoded data was present in pass.txt and a password protected ZIP file was also there.

```
localhost@red:~/Desktop/Forensics-Workshop/Challenge 7$ cat Dig_deeper/pass.txt | base64 -d | cut -d':' -f2 | xxd -r -p | base64 -d
jerry_and_sons
```

So we have password for ZIP file, but the ZIP file is corrupted. Open Challenge.zip in hex editor and change the signature from "504B0506" to "504B0304" i.e. from "EoCD" to "local file header"

Open Challenge.zip in WinRAR, then repair it. Alternative is to use "zip with -FF" in linux.

Unzip Challenge.zip with password jerry_and_sons and got Challenge.png. Run strings on it and get the flag.

FLAG : flag{All_t00ls_ar3_u53ful_guys!!!}


## Challenge 8

```
### Description

My employee stole one my company's secrets and stored in this ZIP file. Can you help me finding it?

### Difficulty

Medium
```

We got a password protected ZIP file. Change the header bytes from "704b0506" to "504b0304" using any hex editor.

I tried fcrackzip to bruteforce the password but got nothing. So I tried "John"

```
localhost@red:~/Desktop/Forensics-Workshop/Challenge 8$ ~/JohnTheRipper/run/zip2john new_3_4.zip > hash.txt

localhost@red:~/Desktop/Forensics-Workshop/Challenge 8$ ~/JohnTheRipper/run/john hash.txt --wordlist=../../rockyou.txt

```

Now I have cracked password "deadlock". Unzip the file and got lock.jpg

```
localhost@red:~/Desktop/Forensics-Workshop/Challenge 8$ strings -n 10 lock.jpg | grep -i flag | cut -d'&' -f2
flag{s0m3t1m3s_brut3f0rc3_is_n33d3d}
```

FLAG : flag{s0m3t1m3s_brut3f0rc3_is_n33d3d}


## Challenge 9

```
### Description 

I find something fishy with this document, please find that out for me.

### Difficulty

Hard
```

We got a file file.docx . Author of this challenge included it in "Hard" category but the solution was really simple. So author may want us to solve this challenge in complex manner or you will see what message does the flag passes. I will solve in both ways

Easy way : 

```
localhost@red:~/Desktop/Forensics-Workshop/Challenge 9$ strings file.docx | grep -i flag
.T..flag{h0wz_the_joke_hahahha!!}.rPK
```

Intended way : 

```
localhost@red:~/Desktop/Forensics-Workshop/Challenge 9$ unzip file.docx 

Now we have a lot of files, we can use grep -Ri flag also

localhost@red:~/Desktop/Forensics-Workshop/Challenge 9/word/media$ strings image2.jpeg | tail -n1
.T..flag{h0wz_the_joke_hahahha!!}.r
```

So may be including this challenge in "Hard" category is joke to the audience at workshop.

FLAG : flag{h0wz_the_joke_hahahha!!}


## Challenge 10

```
### Description

Our Spiders are sensing something with their super cool spider sense, help them find that.

### Difficulty

Hard
```

I got a file spidey.jpg. Use binwalk and got the password protected ZIP file.

```
localhost@red:~/Desktop/Forensics-Workshop/Challenge 10$ fcrackzip -v -D -u -p ../../rockyou.txt 1.zip 
found file 'sense.txt', (size cp/uc     69/    57, flags b, chk 960d)
checking pw udehss                                  

PASSWORD FOUND!!!!: pw == spidersense5
```

So we bruteforced the password for ZIP file. Let's extract its content. Now we got another file sense.txt

```
localhost@red:~/Desktop/Forensics-Workshop/Challenge 10$ cat sense.txt | base64 -d | base64 -d
flag{Spid3y_s3nse_is_c00l!}
```

FLAG : flag{Spid3y_s3nse_is_c00l!}

---
