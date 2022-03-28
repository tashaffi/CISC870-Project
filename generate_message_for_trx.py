import random
from struct import pack
from crccheck.crc import Crc8Wcdma
from read_data import read_remote_control_data


def gen_rc_SN(num_neighbour):
    serial_nums = {}
    for i in range(num_neighbour+1):
        serial_nums[i+1] = random.getrandbits(36)

    return serial_nums


def get_button_mapping():
    button_mapping = {}
    for i in range(11):
        button_mapping[i] = random.getrandbits(12)

    return button_mapping


num_neighbours = 2
rc_device_type = random.getrandbits(6)
rc_SNs = gen_rc_SN(num_neighbours)
button_mapping = get_button_mapping()


def gen_transmitted_msg_remote_control(remote_control_msg):
    rc_transmitted_msg = {}

    for rc_id in remote_control_msg.keys():
        rc_transmitted_msg[rc_id] = []

        insulin_dosage = remote_control_msg[rc_id]["insulin_dosage"]
        for ctr, dose in enumerate(insulin_dosage):
            trx_dose = construct_message_rc(dose, rc_id, 3*ctr)
            rc_transmitted_msg[rc_id].append(trx_dose)

    return rc_transmitted_msg


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


if __name__ == "__main__":
    #print_code_in_english(1)
    self_id = 3
    remote_control_msg = read_remote_control_data([1, 2], self_id)
    print(remote_control_msg)

    rc_transmitted_msg = gen_transmitted_msg_remote_control(remote_control_msg)