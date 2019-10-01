---
layout : default
---

# FLARE-ON 6
30-09-2019

This was my first year participating in flare-on CTF. I'm really thankful to FireEye for organising this lovely CTF. It taught me a lot of new techniques. I had mid-terms, projects so couldn't give it proper time but I was able to solve 9 challenges out of 12 and hope I will do better next year.


## 1 - Memecat Battlestation

Run the executable and it will ask for weapon codes. 

```
localhost@red:~/Desktop$ file MemeCatBattlestation.exe
MemeCatBattlestation.exe: PE32 executable (GUI) Intel 80386 Mono/.Net assembly, for MS Windows
```

This challenge was a .NET executable, so let's decompile it using ```dnspy```.

Analyse the ```Main()``` function and you will see it checks two weapon codes and if both of them are correct then it will give you the flag using the code "XOR(weapon_code2 + weapon_code1, a pre-defined array)"

For Stage1, check function ```FireButton_Click``` of ```Stage1Form```

![Image not found](https://raw.githubusercontent.com/r0hanSH/r0hanSH.github.io/master/images/flareon/ch-1-stage1.JPG)

It's clear that first weapon code is "RAINBOW". Now let's analyse ```isValidWeaponCode``` function of ```Stage2Form```.

![Image not found](https://raw.githubusercontent.com/r0hanSH/r0hanSH.github.io/master/images/flareon/ch-1-stage2.JPG)

```py
from pwn import xor
print xor('\x03 &$-\x1e\x02 //./', 'A')
```

So the second weapon code is "Bagel_Cannon" and we got the flag.

![Image not found](https://raw.githubusercontent.com/r0hanSH/r0hanSH.github.io/master/images/flareon/ch-1-flag.JPG)

FLAG : Kitteh_save_galixy@flare-on.com

## 2 - Overlong

I solved it in few seconds, oh not me actually Cutter(radare2 GUI version) solved it :)
Let's open it in Cutter with Analysis mode enabled and then check ```Strings``` and we got the flag.

![Image not found](https://raw.githubusercontent.com/r0hanSH/r0hanSH.github.io/master/images/flareon/ch-2-flag.JPG)

FLAG : I_a_M_t_h_e_e_n_C_o_D_i_n_g@flare-on.com

## 3 - Flarebear

A .apk file was provided, I decompiled it using apktool. The ```FlareBearActivity.java``` at "com\fireeye\flarebear" contains juicy stuff. I analysed the code statically and ```setMood``` performs the checks to call ```danceWithFlag()```.

```java
 public final void setMood() {
        if (isHappy()) {
            ((ImageView) _$_findCachedViewById(C0272R.C0274id.flareBearImageView)).setTag("happy");
            if (isEcstatic()) {
                danceWithFlag();
                return;
            }
            return;
        }
        ((ImageView) _$_findCachedViewById(C0272R.C0274id.flareBearImageView)).setTag("sad");
    }
```

This ```setMood``` is called inside ```clean``` function. 

```java
    public final void clean(@NotNull View view) {
        Intrinsics.checkParameterIsNotNull(view, "view");
        saveActivity("c");
        removePoo();
        cleanUi();
        changeMass(0);
        changeHappy(-1);
        changeClean(6);
        setMood();
    }
```

See the args of "change\*" functions are static, we have three buttons(feed, play, clean) when we run this apk in android. I analysed the code and got to know that each time we click one of these buttons, it changes the value of three states namely mass, happy and clean. The function ```isEcstatic``` checks these three values and if ```isEcstatic``` returns true, we will get the flag.

```java
   public final boolean isEcstatic() {
        int state = getState("mass", 0);
        int state2 = getState("happy", 0);
        int state3 = getState("clean", 0);
        if (state == 72 && state2 == 30 && state3 == 0) {
            return true;
        }
        return false;
```

So rather than writing mathematical equation, I started with hit and trial method. I opened my notebook started calculating values by keeping in mind that the last click should be on ```clean``` button because ```clean``` function calls the ```setMood``` function.

Now let's see how the functions feed(), play() and clean() changes the value of 3 states (mass, happy and clean)

```
function  mass    happy    clean

feed()    +10      +2       -1

play()    -2       +4       -1

clean()    0       -1       +6
```

To make mass=72, happy=30 and clean=0, how many times should these functions be called ? It's simple maths and I found calling feed() 8 times then call play() 4 times and call clean() 2 times and we got the flag

FLAG: th4t_was_be4rly_a_chall3nge@flare-on.com 


## 4 - Dnschess

We got ChessUI, ChessAI.so and capture.pcap. ChessAI was a linux binary, I ran it and it utilised ChessAI.so to maintain the game scenario. My first thought was that we need to win in this game and it will reveal the flag. But I was wrong even after winning the game, it didn't gave us the flag. So what else it wants us to do, let's analyse.

I analysed it and it was making requests to subdomains of "game-of-thrones.flare-on.com", but these requests depends on our chess moves. For e.g. If I move a "pawn" from "a2" to "a3", then it will make request to "pawn-a2-a3.game-of-thrones.flare-on.com" and then it process the resolved IP address for flag.

While analysing the binary, I found out the format of correct IP addresses:

```
127.XOR_key.moveNumber_start_from_0.0
```

Now let's collect the resolved IPs of those subdomains, I made request to those subdomains and all were down. And then I remember, we also have another file (capture.pcap). Open it in wireshark and you will see the resolved IPs to some of the subdomains.

![Image not found](https://raw.githubusercontent.com/r0hanSH/r0hanSH.github.io/master/images/flareon/ch-4-ips.JPG)

Let's go back to analyse the binary. I found that we will get the flag, if we follow the specific moves in a sequence. Now I edited the ```/etc/hosts``` file with following content:

```
127.53.0.0	pawn-d2-d4.game-of-thrones.flare-on.com
127.215.1.0	pawn-c2-c4.game-of-thrones.flare-on.com
127.159.2.0	knight-b1-c3.game-of-thrones.flare-on.com
127.182.3.0	pawn-e2-e4.game-of-thrones.flare-on.com
127.252.4.0	knight-g1-f3.game-of-thrones.flare-on.com
127.217.5.0	bishop-c1-f4.game-of-thrones.flare-on.com
127.89.6.0	bishop-f1-e2.game-of-thrones.flare-on.com
127.230.7.0	bishop-e2-f3.game-of-thrones.flare-on.com
127.108.8.0	bishop-f4-g3.game-of-thrones.flare-on.com
127.34.9.0	pawn-e4-e5.game-of-thrones.flare-on.com
127.25.10.0	bishop-f3-c6.game-of-thrones.flare-on.com
127.49.11.0	bishop-c6-a8.game-of-thrones.flare-on.com
127.200.12.0	pawn-e5-e6.game-of-thrones.flare-on.com
127.99.13.0	queen-d1-h5.game-of-thrones.flare-on.com
127.141.14.0	queen-h5-f7.game-of-thrones.flare-on.com
```

Follow these moves i.e. the first move is "pawn from d2 to d4" and so on and we got the flag.

![Image not found](https://raw.githubusercontent.com/r0hanSH/r0hanSH.github.io/master/images/flareon/ch-4-flag.JPG)


Now the final flag script is:

```py
from pwn import xor

a = "795AB8BCECD3DFDD99A5B6AC1536858D090877524D71547DA7A70816FDD7".decode('hex')

ip_addr_1 = [53, 53, 215, 215, 159, 159, 182, 182, 252, 252, 217, 217, 89, 89, 230, 230, 108, 108, 34, 34, 25, 25, 49, 49, 200, 200, 99, 99, 141, 141]

key = ''.join(chr(i) for i in ip_addr_1)

flag = xor(a, key)
print flag + "@flare-on.com"
```

We got the flag :)

FLAG : LooksLikeYouLockedUpTheLookupZ@flare-on.com

## 5 - demo

I found out the solution in few minutes. The binary is compressed with crinkler v2.1, as the header of binary was MZ21PE, here 21 means version 2.1
Since the exe is using DirectX9, we can dump 3D models and textures. So I searched for some tools to do the same. I used ```ninjaripper``` to dump those stuff.

Open 4k.exe using ```nijaripper``` and then press ```F10```, now you will have .RIP files. Now we need to read the content of those .RIP files. I used ```noesis``` for the same. First we need to copy fmt_ninjaripper_rip.py from ninjaripper1.7.1\tools\noesis_importer to noesisv4406\plugins\python and then load .RIP files in noesis. Click on .RIP file and you get the flag.

![Image not found](https://raw.githubusercontent.com/r0hanSH/r0hanSH.github.io/master/images/flareon/ch-5-flag.JPG)


FLAG: moar_pouetry@flare-on.com

## 6 - bmphide

A .NET exe was provided, so I decompiled it using dnSpy. It takes 3 arguments arg[0]= given.bmp, arg[1]=keyFile , arg[2]=output.bmp
Program.Init() was used to update values of some variables and anti-debugging checks(indirectly).
I started analysing Main() from bottom, so first analyse function i()

```
public static void i(Bitmap bm, byte[] data)
{
    int num = Program.j(103);
    for (int i = Program.j(103); i < bm.Width; i++)
    {
        for (int j = Program.j(103); j < bm.Height; j++)
        {
            bool flag = num > data.Length - Program.j(231);
            if (flag)
            {
                break;
            }
            Color pixel = bm.GetPixel(i, j);
            int red = ((int)pixel.R & Program.j(27)) | ((int)data[num] & Program.j(228));
            int green = ((int)pixel.G & Program.j(27)) | (data[num] >> Program.j(230) & Program.j(228));
            int blue = ((int)pixel.B & Program.j(25)) | (data[num] >> Program.j(100) & Program.j(230));
            Color color = Color.FromArgb(Program.j(103), red, green, blue);
            bm.SetPixel(i, j, color);
            num += Program.j(231);
        }
    }
}
```
I calculated the values that j() returns. For red, Program.j(27)=248 and Program.j(228)=7, what things we know are pixel.R, static values and we have two unknowns data[num] and red. How to find them, we have only one equation and two unknown variables and our main goal is to find data[num]. If you look closely, you will see only "last 3 bits of data[num]" matters for red. Green and blue will give the other bits of data[num], so now we have data[num].

Now let's analyse function h(), it contains four functions f(), a(), e() and c(). And if you see there other functions like g(), b(), d() which were never used in program. So why those functions are present. I analysed them USED function do encryption stuff and UNUSED function do decryption stuff. So we don't need to reverse these functions and just need to change the flow to call those functions.

After doing so, I ran my script and got another .BMP file. Then again running script on the output.bmp gives flag file.

![Image not found](https://raw.githubusercontent.com/r0hanSH/r0hanSH.github.io/master/images/flareon/ch-6-flag.JPG)

FLAG: d0nT_tRu$t_vEr1fy@flare-on.com

## 7 - wopr

The exe was packed with PyInstaller, we can unpack it using ```pyinstxtractor```. I don't know whether it was packed or not, but PyInstaller's basic work is to convert .py file to .exe

![Image not found](https://raw.githubusercontent.com/r0hanSH/r0hanSH.github.io/master/images/flareon/ch-7-unpack.JPG)

This tool also tells the possible entry point, I used uncompyle6 to decompile ```pyiboot02_cleanup.pyc```
I read the output.py(decompiled code), but still it wasn't the real code? I don't see any strings that I see when I run the exe. So let's analyse output.py further. It had some weird functions, fire(), eye() etc. I found something interesting i.e. the functionality of print() and exec() was exchanged. i.e. if I call print(A) then will be exec(A). I also opened the decompiled code in a hex editor and saw there were "09" and "20" i.e. tab and space which was used to create the actual code. So last code block in decompiled code was

```
for i in range(256):
    try:
        print(lzma.decompress(fire(eye(__doc__.encode()), bytes([i]) + BOUNEC)))
    except Exception:
        pass
```

Change it to

```
for i in range(256):
    try:
        exec(lzma.decompress(fire(eye(__doc__.encode()), bytes([i]) + BOUNCE))) # is actually exec(same_stuff)
    except Exception:
        cntt+=1        
        pass
```

It will print the actual code. Oh the game is not over yet. We need to analyse the original code. After some hours, I found the basic behaviour of Pyinstaller packed executables. When we run them, we get "\_MEIXXXXXX" folder in "%TEMP%", and this \_MEIXXXXXX folder contains "\_\_init\_\_.py" file. Set the breakpoint on "CreateProcessW". When the exe was running I edited this \_\_init\_\_.py file and added wrong() function and some extra code to get the desired array(list)

![Image not found](https://raw.githubusercontent.com/r0hanSH/r0hanSH.github.io/master/images/flareon/ch-7-init.JPG)

![Image not found](https://raw.githubusercontent.com/r0hanSH/r0hanSH.github.io/master/images/flareon/ch-7-list.JPG)

If you see the original code, it does some XORing to get the real launch code. We need to find a launch code which satisfies the constraints of that XORing routine. I wrote an angr script for the same and got the launch code 
"5C0G7TY2LWI2YXMB"

Run exe and pass this launch code and get the flag :)

![Image not found](https://raw.githubusercontent.com/r0hanSH/r0hanSH.github.io/master/images/flareon/ch-7-flag.JPG)


FLAG: L1n34R_4L93bR4_i5_FuN@flare-on.com

## 8 - snake

.NES file was provided, I used FCEUX to run it. Wow it's a snake game. Few things I noticed using hex editor of FCEUX are

```
0x25 = Score (inc by 1)
0x28 = Speed of Snake

0x17 = x co-ordinate of eatable stuff
0x18 = y co-ordinate of eatable stuff

0x4 and 0x5 == 0 for right, 1 for left, 2 for up and 3 for down

0xa and 0xb == increment by 5 when snake take one eatable

0x1c and 0x1d == snake movement
0x1c == x-coordinate
0x1d == y-coordinate
```

I thought our main goal is to make a very high score but it wasn't that. I set a very high score but nothing happened, I didn't got the flag. Then I read disassembled code and in hex editor, at offset 0x25 set R-W breakpoints and see debugger, it adds 1 to score and compare with 0x33, if it's equal it increases the speed of snake i.e. next level. So 0x28 is now 0x2 and again we change 0x25 to 0x32 and again it compares with 0x33 after adding 0x1. So now speed 0x8, we change speed to 0x1 and score to 0x32 and get one point to get the flag.

![Image not found](https://raw.githubusercontent.com/r0hanSH/r0hanSH.github.io/master/images/flareon/ch-8-flag.JPG)

FLAG: NARPAS-SWORD@FLARE-ON.COM

## 9 - reloadered

This challenge becomes too easy, if you know one basic anti-anti-debugging technique. This exe have some anti-debug checks. I analysed the binary and observed the XOR routine which gives key "RoT3rHeRinG", but it gave me fake flag.

![Image not found](https://raw.githubusercontent.com/r0hanSH/r0hanSH.github.io/master/images/flareon/ch-9-fakeflag.JPG)

I analysed the binary and got to know that these anti-debug checks are present only before asking for key input. So I ran exe and used IDA debugger to attach to this process, saw the content of XOR stuff is changed. The binary also checks that result of XOR(changed stuff, KEY) contains "@flare-on.com". As we know, "@flare-on.com" occurs at the end of the flag.

```
from pwn import xor

that_stuff = "7a 17 08 34 17 31 3b 25 5b 18 2e 3a 15 56 0e 11 3e 0d 11 3b 24 21 31 06 3c 26 7c 3c 0d 24 16 3a 14 79 01 3a 18 5a 58 73 2e 09 00 16 00 49 22 01 40 08 0a 14".replace(' ','').decode('hex')

flag_format = "@flare-on.com"

key = xor(flag_format, that_stuff[-len(flag_format):])
print "xor key = ", key

flag = xor(c,key)
print flag
```

![Image not found](https://raw.githubusercontent.com/r0hanSH/r0hanSH.github.io/master/images/flareon/ch-9-flag.JPG)


FLAG: I_mUsT_h4vE_leFt_it_iN_mY_OthEr_p4nTs?!@flare-on.com
