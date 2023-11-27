import json
from collections import defaultdict
from datetime import datetime
import re
# from cryptography.fernet import Fernet

hours = open('time_entries.json')
hours = json.load(hours)

# def convert24(time):
#     # Parse the time string into a datetime object
#     t = datetime.strptime(time, '%I:%M:%S %p')
#     # Format the datetime object into a 24-hour time string
#     return t.strftime('%H:%M:%S')


def convert_to_24hour(time_str):
    hour, minute, am_pm = re.findall('\d+|\w+', time_str)
    hour = int(hour)
    if am_pm == 'pm' and hour != 12:
        hour += 12
    elif am_pm == 'am' and hour == 12:
        hour = 0
    return f'{hour:02d}:{minute}'


def timecalc(timein, timeout):
    # Parse the time strings to datetime objects
    time_in_obj = datetime.strptime(timein, '%H:%M')
    time_out_obj = datetime.strptime(timeout, '%H:%M')

    time_difference = time_out_obj - time_in_obj

    return time_difference.total_seconds() / 3600



grouped_data = defaultdict(list)

for entry in hours:
    # print(entry)
    grouped_data[entry['name']].append(entry)
    # print(f'creating list for {entry["name"]}')

phils_records = grouped_data['Phil']
fahn_records = grouped_data['Fahn']
peppers_reccs = grouped_data['Pepper']

# print(f'phils {phils_records}')
# print(f'Fahns {fahn_records}')
# print(f'Pepper {peppers_reccs}')

for name, records in grouped_data.items():
    print(f"records for {name}")
    for entry in records:
        print(entry)

        timein = convert_to_24hour(entry['time_in'])
        timeout = convert_to_24hour(entry['time_out'])

        hours = timecalc(timein, timeout)

        # (TimeInh, TimeINm) = timein.split(':')
        # (TimeOuth, TimeOutm) = timein.split(':')
        print(timein)
        print(timeout)
        print(hours)



# print(f'hours: {hours}')

# for time in hours:
#     for
#     print(time)

