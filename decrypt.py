import socket
import time

host = "192.168.2.83"

port = 26151

invalid = 'invalid padding\n'

data = "5468697320697320616e204956343536069242ad5ac3e289582b09ff2d30032b0e72a2004dc6d37181448f0327a2a3f3fe3280b99951c832ca8d08940716d226af1a2edddadfdbe92a5933f4d869c714e53842a369eb89a44ae1159b3b73f3d3" ## the cipher we want to decrypt, copy from CTF server terminal


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
        time.sleep(5)
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
            print("current cipher: ", c1_)
            secret_text = c1_ + c2 + " "

            s = socket.socket()
            s.connect((host, port))
            s.sendall(secret_text.encode())
            s.shutdown(socket.SHUT_WR)

            fragments = []
            while True:
                chunk = s.recv(100)
                if not chunk:
                    break
                fragments.append(chunk.decode('utf-8'))
            result = "".join(fragments)
            
            s.close()

            if result[-16:] != invalid:
                if b == c1[index : index + 2] and plain_padding == 1:
                    continue
                I = int(b, 16) ^ plain_padding ##
                Is = [I] + Is
                plain = hex(int(c1[index:index + 2], 16) ^ I)[2:] ##
                if len(plain) == 1:
                    plain = '0' + plain
                bytes_obj = bytes.fromhex(plain)
                res = bytes_obj + res
                plain_padding += 1
                index -= 2
                break
    print("current block has message: ", res)
    return res



plain_5 = attack_blocks(block5, block6)
time.sleep(5)
plain_4 = attack_blocks(block4, block5)
time.sleep(5)
plain_3 = attack_blocks(block3, block4)
time.sleep(5)
plain_2 = attack_blocks(block2, block3)
time.sleep(5)
plain_1 = attack_blocks(block1, block2)

print("The plain text is ", plain_1 + plain_2 + plain_3 + plain_4 + plain_5)
