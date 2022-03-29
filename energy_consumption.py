#1
def measure_energy_consumption(messages, self_id):
    trx_energy = 2.25 #2.25 micro J
    rcv_energy = .75 #.75 micro J

    rc_comm, ip_comm = 0, 0

    for patient_id in messages.keys():
        for dose in messages[patient_id]:
            for button_press in dose:
                if patient_id == self_id:
                    rc_comm += len(button_press.encode('utf-8')) * 8 * trx_energy
                    ip_comm += len(button_press.encode('utf-8')) * 8 * rcv_energy
                else:
                    device_SN_size = 6 + 36 #device_type+remote_control_SN
                    ip_comm += device_SN_size * rcv_energy

    return 0, 0, rc_comm, ip_comm 


#2
def measure_energy_consumption_enc_without_opt_without_mac(messages, self_id): 
    trx_energy = 2.25 #2.25 micro J
    rcv_energy = .75 #.75 micro J
    enc_energy = 2.13 #2.13 micro J
    dec_energy = 2.13 #2.13 micro J

    rc_comm, ip_comm, rc_computation, ip_computation = 0, 0, 0, 0 

    for patient_id in messages.keys():
        for dose in messages[patient_id]:
            for button_press in dose:
                if patient_id == self_id:
                    rc_computation += enc_energy
                    ip_computation += dec_energy
                    rc_comm += len(button_press.encode('utf-8')) * 8 * trx_energy
                    ip_comm += len(button_press.encode('utf-8')) * 8 * rcv_energy
                else:
                    device_SN_size = 6 + 36 #device_type+remote_control_SN
                    ip_comm += device_SN_size * rcv_energy

    return rc_computation, ip_computation, rc_comm, ip_comm  


#3
def measure_energy_consumption_enc_with_opt_without_mac(messages, self_id): 
    trx_energy = 2.25 #2.25 micro J
    rcv_energy = .75 #.75 micro J
    enc_energy = 2.13 #2.13 micro J
    dec_energy = 2.13 #2.13 micro J

    rc_comm, ip_comm, rc_computation, ip_computation = 0, 0, 0, 0 

    for patient_id in messages.keys():
        for dose in messages[patient_id]:
            for button_press in dose:
                if patient_id == self_id:
                    rc_computation += enc_energy
                    ip_computation += dec_energy
                    rc_comm += len(button_press.encode('utf-8')) * 8 * trx_energy
                    ip_comm += len(button_press.encode('utf-8')) * 8 * rcv_energy
                else:
                    device_SN_size = 6 + 12 #device_type+remote_control_SN
                    ip_comm += device_SN_size * rcv_energy

    ip_computation += 2*dec_energy #to account for collision due to smaller SN number size
    return rc_computation, ip_computation, rc_comm, ip_comm 


#4
def measure_energy_consumption_enc_with_opt_with_mac(messages, self_id): 
    trx_energy = 2.25 #2.25 micro J
    rcv_energy = .75 #.75 micro J
    enc_energy = 2.13 #2.13 micro J
    dec_energy = 2.13 #2.13 micro J
    mac_gen_energy = 2.14 #2.14 micro J
    mac_verify_energy = 2.16 #2.16 micro J

    rc_comm, ip_comm, rc_computation, ip_computation = 0, 0, 0, 0 

    for patient_id in messages.keys():
        for dose in messages[patient_id]:
            for button_press in dose:
                if patient_id == self_id:
                    rc_computation += (enc_energy + mac_gen_energy)
                    ip_computation += (dec_energy + mac_verify_energy)
                    rc_comm += len(button_press.encode('utf-8')) * 8 * trx_energy
                    ip_comm += len(button_press.encode('utf-8')) * 8 * rcv_energy
                else:
                    device_SN_size = 6 + 12 #device_type+remote_control_SN
                    ip_comm += device_SN_size * rcv_energy

    ip_computation += 2*dec_energy #to account for collision due to smaller SN number size
    ip_computation += 2*mac_verify_energy #to account for collision due to smaller SN number size
    return rc_computation, ip_computation, rc_comm, ip_comm 

