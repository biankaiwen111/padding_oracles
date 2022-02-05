

import socket

host = "127.0.0.1"

port = 23556

invalid = b'invalid padding\n'

data = "5468697320697320616e20495634353676f451dfe8f3a771cfdef0a3675c3f608b00ef8672e052721691b2cfb637e58faca4b94cfe0a3abd168f71f3adbbcf5bca90e1bfff9a413789b032e1c4186f1343dcddb0e04c0ddf86412c93ad7f93c5" ## one extra ending char needed 

block1 = data[0:32]
block2 = data[32:64]
block3 = data[64:96]
block4 = data[96:128]
block5 = data[128:160]
block6 = data[160:192]

def attack_blocks(block1, block2):
    c1 = block1
    c2 = block2
    res = b""
    index = 30
    plain_padding = 1
    Is = []
    for _ in range(16):

        paddings = [hex(plain_padding  ^ I)[2:] for I in Is]
        padding_str = ""

        for I in Is:
            p = hex(plain_padding  ^ I)[2:]
            if len(p) == 1:
                p = '0' + p
            padding_str += p

        for i in range(256):
        
            b = hex(i)[2:]
            if len(b) == 1:
                b = "0" + b

            c1_ = c1[ : index] + b + padding_str
            secret_text = c1_ + c2 + " "

            s = socket.socket()
            s.connect((host, port))
            s.sendall(secret_text.encode())
            s.shutdown(socket.SHUT_WR)

            result = s.recv(2024, socket.MSG_WAITALL)

            if result[-16:] != invalid:
                if b == c1[index : index + 2] and plain_padding == 1:
                    print("warning!")
                    continue
                print("yo")
                print(c1_)
                I = int(b, 16) ^ plain_padding ##
                Is = [I] + Is
                plain = hex(int(c1[index:index + 2], 16) ^ I)[2:] ##
                if len(plain) == 1:
                    plain = '0' + plain
                bytes_obj = bytes.fromhex(plain)
                ascii_string = bytes_obj.decode("ASCII")
                res = bytes_obj + res
                plain_padding += 1
                index -= 2
                break
    return res



plain_5 = attack_blocks(block5, block6)
print(plain_5)
##plain_4 = attack_blocks(block4, block5)
# print(plain_4)
##plain_3 = attack_blocks(block3, block4)
# print(plain_3)
##plain_2 = attack_blocks(block2, block3)

##plain_1 = attack_blocks(block1, block2)
# print(plain_2)

##print(plain_1 + plain_2 + plain_3 + plain_4 + plain_5)

'''
c1 = block5
c2 = block6
res = ""
for i in range(256):
    b = hex(i)[2:]
    if len(b) == 1:
        b = "0" + b

    c1_ = c1[ : 28] + b + "1c"

    secret_text = c1_ + c2 + " "

    s = socket.socket()

    s.connect((host, port))

    s.sendall(secret_text.encode())

    s.shutdown(socket.SHUT_WR)

    result = s.recv(2024)
    
    ##print(result[-16:] == invalid)
    if result[-16:] != invalid and b != c1[-2:]:
        ##print(c1[-2:])
        plain = hex(int(c1[28:30], 16) ^ int(b, 16) ^ int("02", 16))
        print(plain)
        res = plain + res
        ##print(b)
        print(secret_text)
        ##print(block4 + block5)
'''
'''
c1 = block5
c2 = block6
res = ""
for i in range(256):
    for j in range(256):
        a = hex(i)[2:]
        b = hex(j)[2:]
        if len(a) == 1:
            a = "0" + b
        if len(b) == 1:
            b = "0" + b

        c1_ = c1[ : 28] + a + b
        secret_text = c1_ + c2 + " "

        s = socket.socket()

        s.connect((host, port))

        s.sendall(secret_text.encode('utf-8'))

        s.shutdown(socket.SHUT_WR)

        result = s.recv(2024)

    ##print(result[-16:] == invalid)
        if result[-16:] != invalid and b != c1[-2:]:
            print(secret_text)
        ##print(c1[-2:])
        ##plain = hex(int("00", 16) ^ int(b, 16) ^ int(c1[-2:], 16))
        ##print(plain)
        ##res = plain + res
        ##print(b)
            
        ##print(block4 + block5)
'''


#{"username": "gu
#est", "expires":ok
# "2000-01-07", "ok

#is_admin": "falsok


##e"}\r\r\r\r\r\r\r\r\r\r\r\r\r