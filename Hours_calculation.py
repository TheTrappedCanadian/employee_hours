import json
import re
import csv
from collections import defaultdict
from datetime import datetime

class TimeEntryProcessor:
    def __init__(self, filename):
        self.filename = filename
        self.grouped_data = defaultdict(list)
        self.total_hours_per_person = defaultdict(float)
        self.load_hours()

    def load_hours(self):
        with open(self.filename) as file:
            self.hours = json.load(file)

    def convert_to_24hour(self, time_str):
        hour, minute, am_pm = re.findall('\d+|\w+', time_str)
        hour = int(hour)
        if am_pm == 'PM' and hour != 12:
            hour += 12
        elif am_pm == 'AM' and hour == 12:
            hour = 0
        return f'{hour:02d}:{minute}'

    def timecalc(self, timein, timeout):
        time_in_obj = datetime.strptime(timein, '%H:%M')
        time_out_obj = datetime.strptime(timeout, '%H:%M')
        time_difference = time_out_obj - time_in_obj
        return time_difference.total_seconds() / 3600

    def process_entries(self):
        for entry in self.hours:
            self.grouped_data[entry['name']].append(entry)

        for name, records in self.grouped_data.items():
            for entry in records:
                timein = self.convert_to_24hour(entry['time_in'])
                timeout = self.convert_to_24hour(entry['time_out'])
                hours = self.timecalc(timein, timeout)
                self.total_hours_per_person[name] += hours

    def write_total_hours_csv(self):
        with open('total_hours.csv', 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['Name', 'Total Hours'])
            for name, total_hours in self.total_hours_per_person.items():
                csvwriter.writerow([name, f"{total_hours:.2f}"])

    def write_detailed_hours_csv(self):
        with open('detailed_hours.csv', 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['Name', 'Day', 'Time In', 'Time Out', 'Hours Worked'])
            for entry in self.hours:
                timein_24h = self.convert_to_24hour(entry['time_in'])
                timeout_24h = self.convert_to_24hour(entry['time_out'])
                hours_worked = self.timecalc(timein_24h, timeout_24h)
                csvwriter.writerow([entry['name'], entry['day'], timein_24h, timeout_24h, f"{hours_worked:.2f}"])

    def get_processed_data(self):
        # Return a summary of processed data
        detailed_data = []
        for entry in self.hours:
            timein_24h = self.convert_to_24hour(entry['time_in'])
            timeout_24h = self.convert_to_24hour(entry['time_out'])
            hours_worked = self.timecalc(timein_24h, timeout_24h)
            detailed_data.append({
                'name': entry['name'],
                'day': entry['day'],
                'time_in': timein_24h,
                'time_out': timeout_24h,
                'hours_worked': f"{hours_worked:.2f}"
            })
        return detailed_data, dict(self.total_hours_per_person)

# Usage
processor = TimeEntryProcessor('time_entries.json')
processor.process_entries()
processor.write_total_hours_csv()
processor.write_detailed_hours_csv()



# import json
# from collections import defaultdict
# from datetime import datetime
# import re
# import csv
# # from cryptography.fernet import Fernet
#
# hours = open('time_entries.json')
# hours = json.load(hours)
#
#
# def convert_to_24hour(time_str):
#     hour, minute, am_pm = re.findall('\d+|\w+', time_str)
#     hour = int(hour)
#     if am_pm == 'PM' and hour != 12:
#         hour += 12
#     elif am_pm == 'AM' and hour == 12:
#         hour = 0
#     return f'{hour:02d}:{minute}'
#
#
# def timecalc(timein, timeout):
#     # Parse the time strings to datetime objects
#     time_in_obj = datetime.strptime(timein, '%H:%M')
#     time_out_obj = datetime.strptime(timeout, '%H:%M')
#
#     time_difference = time_out_obj - time_in_obj
#
#     return time_difference.total_seconds() / 3600
#
#
#
# grouped_data = defaultdict(list)
# total_hours_per_person = defaultdict(float)
#
# for entry in hours:
#     # print(entry)
#     grouped_data[entry['name']].append(entry)
#     # print(f'creating list for {entry["name"]}')
#
#
# for name, records in grouped_data.items():
#     print(f"records for {name}")
#     for entry in records:
#
#         timein = convert_to_24hour(entry['time_in'])
#         timeout = convert_to_24hour(entry['time_out'])
#
#         hours = timecalc(timein, timeout)
#
#         print(f"Name: {entry['name']}, Time in {timein}")
#         print(f"Name: {entry['name']}, Time out {timeout}")
#         total_hours_per_person[name] += hours
#         print(hours)
#
# for name, total_hours in total_hours_per_person.items():
#     print(f"Total hours for {name}: {total_hours:.2f} hours")
#
#
# # Writing to CSV
# with open('total_hours.csv', 'w', newline='') as csvfile:
#     csvwriter = csv.writer(csvfile)
#     # Writing the headers
#     csvwriter.writerow(['Name', 'Total Hours'])
#
#     # Writing the data
#     for name, total_hours in total_hours_per_person.items():
#         csvwriter.writerow([name, f"{total_hours:.2f}"])
#
# # Load the hours from JSON
# with open('time_entries.json') as file:
#     hours2 = json.load(file)
#
# with open('detailed_hours.csv', 'w', newline='') as csvfile:
#     csvwriter = csv.writer(csvfile)
#     # Writing the headers
#     csvwriter.writerow(['Name', 'Day', 'Time In', 'Time Out', 'Hours Worked'])
#
#     # Writing the data
#     for entry in hours2:
#         timein_24h = convert_to_24hour(entry['time_in'])
#         timeout_24h = convert_to_24hour(entry['time_out'])
#         hours_worked = timecalc(timein_24h, timeout_24h)
#         csvwriter.writerow([entry['name'], entry['day'], timein_24h, timeout_24h, f"{hours_worked:.2f}"])