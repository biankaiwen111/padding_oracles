import socket
import time

target_plaintext = '{"username": "guest", "expires": "2023-01-07", "is_admin": "true"}'

ini_2 = "0d" * 16

host = "192.168.2.83"

port = 26151

invalid = 'invalid padding\n'

ini_1 = "00010203040506070809101112131415"

def attack_blocks(block1, block2):
    ini_1 = block1
    ini_2 = block2
    res = ""
    index = 30
    pos = 1
    Is = []

    for j in range(16):
        time.sleep(5)
        padding_str = ""
        for n in range(len(Is)):
            I = Is[n]
            temp = I ^ (pos - 1) ^ pos
            p = hex(I ^ (pos - 1) ^ pos)[2:]
            Is[n] = temp
            if len(p) == 1:
                p = '0' + p
            padding_str += p

        for i in range(256):
            b = hex(i)[2:]
            if len(b) == 1:
                b = "0" + b
    
            c1_ = ini_1[ : index] + b + padding_str
            print("current cipher: ", c1_)

            secret_text = c1_ + ini_2 + " "

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
                I = int(b, 16)
                Is = [I] + Is
                pos += 1
                index -= 2
                res = secret_text
                break
    return res[:-1]

def construct_cipher(plaintext, cipher_blocks):
    padding = "10" * 16
    block1 = cipher_blocks[:32]
    block2 = cipher_blocks[32:]
    res = int(block1, 16) ^ int(padding, 16)
    cipher_text = hex(int(plaintext, 16) ^ int(hex(res)[2:], 16))[2:]
    return cipher_text + block2

def pad(s):
  return s + (16 - len(s) % 16) * chr(16 - len(s) % 16)

def convert_string_to_hex_string(s):
    res = ""
    for char in s:
        hex_char = format(ord(char), "x")
        if len(hex_char) == 1:
            hex_char = '0' + hex_char
        res += hex_char
    return res

padded_target_plain_text = pad(target_plaintext)
hex_target_plaintext = convert_string_to_hex_string(padded_target_plain_text)

target_plaintext_block1 = hex_target_plaintext[:32]
target_plaintext_block2 = hex_target_plaintext[32:64]
target_plaintext_block3 = hex_target_plaintext[64:96]
target_plaintext_block4 = hex_target_plaintext[96:128]
target_plaintext_block5 = hex_target_plaintext[128:]

raw_cipher_text_block_1_2 = attack_blocks(ini_1, ini_2)
cipher_text_block_1_2 = construct_cipher(target_plaintext_block5, raw_cipher_text_block_1_2)
print("cipher text of block 6: ", cipher_text_block_1_2[32:])
time.sleep(5)

ini_1 = "00010203040506070809101112131415"
ini_2 = cipher_text_block_1_2[:32]
raw_cipher_text_block_2_3 = attack_blocks(ini_1, ini_2)
cipher_text_block_2_3 = construct_cipher(target_plaintext_block4, raw_cipher_text_block_2_3)
print("cipher text of block 5: ", cipher_text_block_2_3[32:])
time.sleep(5)

ini_1 = "00010203040506070809101112131415"
ini_2 = cipher_text_block_2_3[:32]
raw_cipher_text_block_3_4 = attack_blocks(ini_1, ini_2)
cipher_text_block_3_4 = construct_cipher(target_plaintext_block3, raw_cipher_text_block_3_4)
print("cipher text of block 4: ", cipher_text_block_3_4[32:])
time.sleep(5)

ini_1 = "00010203040506070809101112131415"
ini_2 = cipher_text_block_3_4[:32]
raw_cipher_text_block_4_5 = attack_blocks(ini_1, ini_2)
cipher_text_block_4_5 = construct_cipher(target_plaintext_block2, raw_cipher_text_block_4_5)
print("cipher text of block 3: ", cipher_text_block_4_5[32:])
time.sleep(5)

ini_1 = "00010203040506070809101112131415"
ini_2 = cipher_text_block_4_5[:32]
raw_cipher_text_block_5_6 = attack_blocks(ini_1, ini_2)
cipher_text_block_5_6 = construct_cipher(target_plaintext_block1, raw_cipher_text_block_5_6)
print("cipher text of block 1 and 2: ", cipher_text_block_5_6)


print("your final cipher text is ", cipher_text_block_5_6 + cipher_text_block_4_5[32:] + cipher_text_block_3_4[32:] + cipher_text_block_2_3[32:] + cipher_text_block_1_2[32:])
