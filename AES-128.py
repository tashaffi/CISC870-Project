from Crypto.Cipher import AES
from base64 import b64encode
from generate_message_for_trx import read_remote_control_data, gen_transmitted_msg_remote_control
import os


# iv = '09080706050403020100A2B2C2D2E2F2'
# plaintext = bytearray.fromhex("255044462d312e350a25d0d4c5d80a34")
# ciphertext = bytearray.fromhex("d06bf9d0dab8e8ef880660d2af65aa82")
# keys = open('keys.txt', 'r')

# for key in keys:
#     key = key.strip()
#     print(key)
#     cipher = AES.new(bytearray.fromhex(key), AES.MODE_CBC, bytearray.fromhex(iv))
    
#     gen_str = cipher.encrypt(plaintext)
#     if gen_str == ciphertext:
#         print('matched')
#         print(key)
#         break

# import json
# from base64 import b64encode

def enc_AES_128_ctr(rc_transmitted_msg):
    key = os.urandom(16)
    cipher = AES.new(key, AES.MODE_CTR)

    rc_enc_msg = {}

    for patient_id in rc_transmitted_msg.keys():
        rc_enc_msg[patient_id] = []

        doses = rc_transmitted_msg[patient_id]

        for dose in doses:
            enc_bt_press = []
            for button_press in dose:
            
                ct_bytes = cipher.encrypt(str.encode(button_press))
                enc_bt = b64encode(ct_bytes).decode('utf-8')
                enc_bt_press.append(enc_bt)

            rc_enc_msg[patient_id].append(enc_bt_press)

    return rc_enc_msg


if __name__ == "__main__":
    #print_code_in_english(1)
    self_id = 3
    remote_control_msg = read_remote_control_data([1, 2], self_id)
    rc_transmitted_msg = gen_transmitted_msg_remote_control(remote_control_msg)
    print(rc_transmitted_msg)
    rc_enc_msg = enc_AES_128_ctr(rc_transmitted_msg)
    print(rc_enc_msg)
