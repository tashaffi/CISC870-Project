from random import random


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



if __name__ == "__main__":
    #print_code_in_english(1)
    samples = gen_sample(1, num_samples=None)
    print(samples)