#!/usr/bin/env python3

import requests
import configparser

def load_config(file_path):
    config = configparser.ConfigParser()
    config.read(file_path)
    return config

def get_readwise_shortlist(api_token):
    try:
        response = requests.get(
            url="https://readwise.io/api/v3/list/",
            headers={"Authorization": f"Token {api_token}"},
            params={
                "location": "shortlist"
            }
        )
        return response
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while making the API request: {e}")
        return None

def process_response(response):
    if response is None:
        print("Error handling is already done in get_readwise_shortlist function.")
    elif response.status_code == 200:
        data = response.json()

        to_read = []

        pattern = r'Comments URL:\s+(https://.+)'
        for d in data['results']:
            match = re.search(pattern, d['summary'])

            if match:
                to_read.append(match.group(1))
            else:
                print("Comments URL not found in the text.")
                
        for r in to_read[:5]:
            webbrowser.open_new_tab(r)

        pass
    elif response.status_code == 500:
        print("The API returned a 500 Internal Server Error. The Readwise team has been informed. Please try again later.")
    else:
        print(f"The API returned an unexpected status code: {response.status_code}")

if __name__ == "__main__":
    config = load_config('config.ini')
    api_token = config.get('readwise', 'api_token')
    response = get_readwise_shortlist(api_token)
    process_response(response)
