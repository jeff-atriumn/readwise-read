#!/usr/bin/env python3

import requests
import json
import webbrowser
import re

response = requests.get(
    url="https://readwise.io/api/v3/list/",
    headers={"Authorization": "Token UemjhH0RW2DJqkFgOJWhYaCWe1Q0ZH7j6ffBJ0h7Hdxt4MBBb6"},
    params={
        "location": "shortlist"
    }
)

print(response.text)
data = response.json()

# print(data['results'][0]['summary'])

to_read = []

pattern = r'Comments URL:\s+(https://.+)'
for d in data['results']:
    match = re.search(pattern, d['summary'])

    if match:
        to_read.append(match.group(1))
    else:
        print("Comments URL not found in the text.")
        
        
for r in to_read[:5]:
    print(r)
    webbrowser.open_new_tab(r)
