import math
import requests
import json
from datetime import datetime
from zoneinfo import ZoneInfo

# https://www.sfmta.com/routes/n-judah
url = 'https://webservices.umoiq.com/api/pub/v1/agencies/sfmta-cis/routes/N/vehicles?key=0be8ebd0284ce712a63f29dcaf7798c4'
base_response_dir = 'responses/'
br = '------------------------------------------------------------------'

def pre_num(num):
    return f'[{num:04}~{num // (60 * 60)}:{((num // 60) % (60 * 60)):02}:{(num % 60):02}]'

def run_muni_req(num, curr_stamp):
    response = requests.get(url)
    if response.status_code != 200:
        return f'Request failed with status code {response.status_code}'

    data = response.json()
    if not isinstance(data, list):
        return 'Request failed, data is not a list'
    if len(data) == 0:
        return 'Request failed, data is empty'

    try:
        output_file = f'muni_{curr_stamp}.json'
        with open(f'{base_response_dir}{output_file}', 'w') as f_out:
            f_out.write(json.dumps(data, indent=4))
        return f'Data received, saved to {output_file}'
    except IOError:
        return f'Error writing to {output_file}, data not saved'

def main():
    # max_time = (60 * 60) + 1 # in seconds
    max_time = 1 # in seconds
    last_time = -1
    start_time = datetime.now(ZoneInfo('America/Los_Angeles'))
    start_timestamp = math.floor(start_time.timestamp())
    print(f'Starting MUNI data collection at {start_time.strftime("%H:%M:%S")}')
    print(br)
    while True:
        curr_timestamp = math.floor(datetime.now().timestamp())
        num = curr_timestamp - start_timestamp
        if num == last_time:
            continue

        print(f'{pre_num(num)} Requesting MUNI data at {datetime.now(ZoneInfo("America/Los_Angeles")).strftime("%H:%M:%S")}...')
        res = run_muni_req(num, curr_timestamp)
        print(f'{pre_num(num)} {res}')
        print(br)

        if (num + 1) >= max_time:
            break
        last_time = num

    print(f'Finished collecting MUNI data at {datetime.now(ZoneInfo("America/Los_Angeles")).strftime("%H:%M:%S")}')

if __name__ == "__main__":
    main()
