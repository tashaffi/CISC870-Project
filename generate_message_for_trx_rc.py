import random
import os
from Crypto.Cipher import AES
from Crypto.Hash import CMAC
from base64 import b64encode
from struct import pack
from crccheck.crc import Crc8Wcdma
from read_data import read_remote_control_data


"""
1. usual communication
2. encryption 
3. encryption + optimization 
4. encryption + optimization + mac

Possibe options:
Todo: 
5. encryption + mac
6. usual + mac
7. usual + optimization + mac
"""


def gen_rc_SN(num_neighbour, opt=False):
    serial_nums = {}
    for i in range(num_neighbour+1):
        if opt:
            serial_nums[i+1] = random.getrandbits(12)
        else:
            serial_nums[i+1] = random.getrandbits(36)

    return serial_nums


def get_button_mapping(opt=False):
    button_mapping = {}
    for i in range(11):
        if opt:
            button_mapping[i] = random.getrandbits(8)
        else:
            button_mapping[i] = random.getrandbits(12)

    return button_mapping


num_neighbours = 2
rc_device_type = random.getrandbits(6)
rc_device_type_opt = random.getrandbits(4)
rc_SNs = gen_rc_SN(num_neighbours)
rc_SNs_opt = gen_rc_SN(num_neighbours, opt=True)
button_mapping = get_button_mapping()
button_mapping_opt = get_button_mapping(opt=True)


def gen_transmitted_msg_remote_control(remote_control_msg, enc=False, opt=False):
    rc_transmitted_msg = {}

    for rc_id in remote_control_msg.keys():
        rc_transmitted_msg[rc_id] = []

        insulin_dosage = remote_control_msg[rc_id]["insulin_dosage"]
        for ctr, dose in enumerate(insulin_dosage):
            # trx_dose = construct_message_rc(dose, rc_id, 3*ctr)
            # trx_dose = construct_message_rc_enc_without_opt_without_mac(dose, rc_id, 3*ctr)
            # trx_dose = construct_message_rc_enc_with_opt_without_mac(dose, rc_id, 3*ctr)
            trx_dose = construct_message_rc_enc_with_opt_with_mac(dose, rc_id, 3*ctr)
            rc_transmitted_msg[rc_id].append(trx_dose)

    return rc_transmitted_msg

#1
def construct_message_rc(message, rc_id, ctr):
    msg_button_press = []

    dev_SN = rc_SNs[rc_id]
    insulin_val = message['insulin_value']

    for cnt, button in enumerate(insulin_val):
    
        dig_button = button_mapping[int(button)]
        ctr_bits = '{0:012b}'.format(ctr+cnt)

        packet = str(rc_device_type) + str(dev_SN) + str(dig_button) + ctr_bits
        CRC = Crc8Wcdma.calc(str.encode(packet))
        CRC = '{0:012b}'.format(CRC)
        packet += CRC

        msg_button_press.append(packet)

    return msg_button_press


#2
def construct_message_rc_enc_without_opt_without_mac(message, rc_id, ctr):
    key = os.urandom(16)
    cipher = AES.new(key, AES.MODE_CTR)

    msg_button_press = []

    dev_SN = rc_SNs[rc_id]
    insulin_val = message['insulin_value']

    for cnt, button in enumerate(insulin_val):
    
        dig_button = button_mapping[int(button)]
        ctr_bits = '{0:016b}'.format(ctr+cnt)

        ct_bytes = cipher.encrypt(str.encode(str(rc_device_type) + str(dig_button)))
        enc_bt = b64encode(ct_bytes).decode('utf-8')

        packet = str(dev_SN) + enc_bt + ctr_bits
        CRC = Crc8Wcdma.calc(str.encode(packet))
        CRC = '{0:012b}'.format(CRC)
        packet += CRC

        msg_button_press.append(packet)

    return msg_button_press


#3
def construct_message_rc_enc_with_opt_without_mac(message, rc_id, ctr):
    key = os.urandom(16)
    cipher = AES.new(key, AES.MODE_CTR)

    msg_button_press = []

    dev_SN = rc_SNs_opt[rc_id]
    insulin_val = message['insulin_value']

    for cnt, button in enumerate(insulin_val):
    
        dig_button = button_mapping_opt[int(button)]
        ctr_bits = '{0:016b}'.format(ctr+cnt)

        ct_bytes = cipher.encrypt(str.encode(str(rc_device_type_opt) + str(dig_button)))
        enc_bt = b64encode(ct_bytes).decode('utf-8')

        packet = str(dev_SN) + enc_bt + ctr_bits
        CRC = Crc8Wcdma.calc(str.encode(packet))
        CRC = '{0:012b}'.format(CRC)
        packet += CRC

        msg_button_press.append(packet)

    return msg_button_press


#4
def construct_message_rc_enc_with_opt_with_mac(message, rc_id, ctr):
    key_enc = os.urandom(16)
    key_mac = os.urandom(16)
    cobj = CMAC.new(key_mac, ciphermod=AES, update_after_digest=True)
    cipher = AES.new(key_enc, AES.MODE_CTR)

    msg_button_press = []

    dev_SN = rc_SNs_opt[rc_id]
    insulin_val = message['insulin_value']

    for cnt, button in enumerate(insulin_val):
    
        dig_button = button_mapping_opt[int(button)]
        ctr_bits = '{0:016b}'.format(ctr+cnt)

        ct_bytes = cipher.encrypt(str.encode(str(rc_device_type_opt) + str(dig_button)))
        enc_bt = b64encode(ct_bytes).decode('utf-8')

        packet = str(dev_SN) + enc_bt + ctr_bits
        cobj.update(str.encode(packet))
        packet += cobj.hexdigest()
        
        msg_button_press.append(packet)

    return msg_button_press


if __name__ == "__main__":
    #print_code_in_english(1)
    self_id = 3
    remote_control_msg = read_remote_control_data([1, 2], self_id)
    print(remote_control_msg)

    rc_transmitted_msg = gen_transmitted_msg_remote_control(remote_control_msg)
    print(rc_transmitted_msg)