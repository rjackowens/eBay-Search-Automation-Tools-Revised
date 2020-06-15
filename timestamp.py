import datetime

def generate_timestamp():
    now = datetime.datetime.now()
    timestamp = str(now.strftime("%m-%d-%Y"))

    return timestamp

# print(generate_timestamp())
