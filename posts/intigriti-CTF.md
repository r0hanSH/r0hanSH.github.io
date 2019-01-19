
---
layout : default
---

# Intigriti CTF (Jan 2018)

## Problem :
[intigriti](https://twitter.com/intigriti)

![Branching](https://www.r0hansh.github.io/images/intigriti/tweet-pic.png)


See the image in the tweet. Let's get started by downloading it.

```
localhost@red:~/Desktop/intigriti$ binwalk -e DweADlgXgAAehHh.jpg 

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             JPEG image data, JFIF standard 1.01
182           0xB6            Zip archive data, at least v2.0 to extract, compressed size: 11029, uncompressed size: 12129, name: nottheflag.pdf
65660         0x1007C         End of Zip archive
```

Open "nottheflag.pdf" and it provided a base64 encoded string. 


