import json
import time
from cryptography.fernet import Fernet

hours = open('time_entries.json')
hours = json.load(hours)

# print(f'hours: {hours}')

for time in hours:

    print(time)

