import requests
import json


def send_to_cloud(e):
    api_url = "https://4wdtvg72lf.execute-api.us-east-1.amazonaws.com/test/submittimes/upload"
    headers = {"Content-Type": "application/json"}

    # Read the time_entries.json file
    with open('time_entries.json', 'r') as file:
        detailed_data = json.load(file)

    # Convert detailed_data to the required format if necessary
    payload = json.dumps(detailed_data)
    print(f'payload {payload}')

    try:
        response = requests.post(api_url, data=payload, headers=headers)
        if response.status_code == 200:
            print("Data successfully sent to the cloud.")
        else:
            print(f"Failed to send data. Status code: {response.status_code}")
    except Exception as ex:
        print(f"An error occurred: {ex}")
