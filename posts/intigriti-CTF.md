---
layout : default
---

# Intigriti CTF (Jan 2019)

The challenge was created by a great bug bounty hunter [Inti De Ceukelaire](https://twitter.com/securinti)

## Problem :
[intigriti](https://twitter.com/intigriti)

![Branching](https://raw.githubusercontent.com/r0hanSH/r0hanSH.github.io/master/images/intigriti/tweet-pic.png)


See the image in the tweet. Let's get started by downloading it.

```
localhost@r0hansh:~/Desktop/intigriti$ binwalk -e DweADlgXgAAehHh.jpg 

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             JPEG image data, JFIF standard 1.01
182           0xB6            Zip archive data, at least v2.0 to extract, compressed size: 11029, uncompressed size: 12129, name: nottheflag.pdf
65660         0x1007C         End of Zip archive
```

Open "nottheflag.pdf" and it provided a base64 encoded string. 

![Branching](https://raw.githubusercontent.com/r0hanSH/r0hanSH.github.io/master/images/intigriti/base64-decode.png)

Visit this link and downloaded data.zip which was password protected.
I tried password cracking tools like fcrackzip, john but nothing worked. I revisited that intigriti tweet and noticed that this image was not posted by them. It was [WhereIsTheFlag](https://twitter.com/WhereIsTheFlag) who uploaded it. So after some recon I come across this :

![Branching](https://raw.githubusercontent.com/r0hanSH/r0hanSH.github.io/master/images/intigriti/hidden-password.png)

The password for data.zip is F1nDBuGz_ 

Now I have a data folder which contains 441 images, namely 1_01.jpg, 1_02.jpg, ..., 1_441.jpg. Some of them were black and some were white.

After some struggle, I tried to merge them to make a new large image of 21x21 matrix. But first I renamed them by deleting 1_ prefix.

```
montage -mode concatenate -tile 21x21 $(ls | sort -n | awk -F'.' '{b=".";print $1b$2}') out.jpg
```

![Branching](https://raw.githubusercontent.com/r0hanSH/r0hanSH.github.io/master/images/intigriti/last-pic.png)

### FLAG:YOUWINTIGRITI

---
