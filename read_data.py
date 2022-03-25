from datetime import datetime
from random import random, sample


code_to_desc = {
        33: 'Regular insulin dose',
        34: 'NPH insulin dose',
        35: 'UltraLente insulin dose',
        48: 'Unspecified blood glucose measurement',    
        57: 'Unspecified blood glucose measurement',
        58: 'Pre-breakfast blood glucose measurement',
        59: 'Post-breakfast blood glucose measurement',
        60: 'Pre-lunch blood glucose measurement',
        61: 'Post-lunch blood glucose measurement',
        62: 'Pre-supper blood glucose measurement',
        63: 'Post-supper blood glucose measurement',
        64: 'Pre-snack blood glucose measurement',
        65: 'Hypoglycemic symptoms',
        66: 'Typical meal ingestion',
        67: 'More-than-usual meal ingestion',
        68: 'Less-than-usual meal ingestion',
        69: 'Typical exercise activity',
        70: 'More-than-usual exercise activity',
        71: 'Less-than-usual exercise activity',
        72: 'Unspecified special event'

    }

#this is just for viewing and making sense of the data, no use otherwise
def print_code_in_english(patient_id):
    patient_id = "0"+str(patient_id) if patient_id < 10 else str(patient_id)
    patient_file = 'Diabetes-Data/data-{}'.format(patient_id)

    pf_pretty = open(patient_file+"_prettify.txt", 'w')
    
    with open(patient_file) as f:
        for line in f.readlines():
            date, time, code, value = line.split('\t')
            pf_pretty.write(date+", "+time+", "+code_to_desc[int(code)]+", "+value+'\n')

    pf_pretty.close()



"""
samples is a dictionary indexed by `dates`, second level is `time`, this is a list because there are multiple entries for `one time`

format of samples (from data-01):
{
    "04-21-1991": {
        "9:09": [
            {
                "code": 58,
                "value": 100 
            },
            {
                "code": 33,
                "value": 9 
            },
            .....
        ]
        "17:08": ...
    },
    "04-22-1991": ...

}
"""
def gen_sample(patient_id, num_samples=None):

    patient_id = "0"+str(patient_id) if patient_id < 10 else str(patient_id)
    patient_file = 'Diabetes-Data/data-{}'.format(patient_id)

    samples = {}

    with open(patient_file) as f:
        for line in f.readlines():
            date, time, code, value = line.split('\t')

            if not date in samples.keys():
                samples[date] = {}
            if time not in samples[date]:
                samples[date][time] = []

            samples[date][time].append({
                "code": int(code),
                "value": int(value.strip('\n'))
            })

    if num_samples:
        samples = random.sample(samples, num_samples)

    return samples


def read_remote_control_data(neighbour_ids, self_id):
    messages = {}

    for p_id in neighbour_ids + [self_id]:
        messages[p_id] = {}

        patient_id = "0"+str(p_id) if p_id < 10 else str(neighbour_ids)
        patient_file = 'Diabetes-Data/data-{}'.format(patient_id)

        with open(patient_file) as f:
            for line in f.readlines():
                date, time, code, value = line.split('\t')
                
                if date not in messages[p_id]:
                    messages[p_id][date] = []
               
                if int(code) in {33, 34, 35}:
                    messages[p_id][date].append({
                        "time": time,
                        "insulin_value": value.strip('\n')
                    })

    return get_most_presses(messages)


def sample_glucose_reading(glucose_sensor_msg):
    sampled_glucose_readings = glucose_sensor_msg.copy()

    for msg_ind, msg in enumerate(glucose_sensor_msg):
        print(glucose_sensor_msg[msg_ind]["time"])
        current_reading = datetime.strptime(glucose_sensor_msg[msg_ind]["time"],"%H:%M")
        if msg_ind==len(glucose_sensor_msg)-1:
            next_reading = datetime.strptime('00:00',"%H:%M")
        else:
            next_reading = datetime.strptime(glucose_sensor_msg[msg_ind+1]["time"],"%H:%M")
        
        time_diff = (next_reading-current_reading).seconds/60
        samples_generated = int(time_diff/3)
        sampled_glucose_readings.extend([glucose_sensor_msg[msg_ind] for i in range(samples_generated)])

    return sample_glucose_reading


def get_most_presses(messages):
    for p_id in messages.keys():
        msg_per_patient = messages[p_id]
        most_msg_day = max(msg_per_patient, key= lambda x: len(msg_per_patient[x]))
        messages[p_id] = {
            "insulin_dosage": msg_per_patient[most_msg_day],
            "date": most_msg_day
        }
    return messages


def read_glucose_sensor_data(self_id, most_msg_day):
    messages = []

    patient_id = "0"+str(self_id) if self_id < 10 else str(self_id)
    patient_file = 'Diabetes-Data/data-{}'.format(patient_id)

    with open(patient_file) as f:
        for line in f.readlines():
            date, time, code, value = line.split('\t')
            
            if date==most_msg_day:
                if int(code) in set(range(57, 64)).union({48}):
                    messages.append({
                        "time": time,
                        "blood_glucose": value.strip('\n')
                    })

    return messages


if __name__ == "__main__":
    #print_code_in_english(1)
    self_id = 4
    remote_control_msg = read_remote_control_data([1, 2], self_id)
    glucose_sensor_msg = read_glucose_sensor_data(self_id, remote_control_msg[self_id]["date"])
    sample_glucose_reading(glucose_sensor_msg)