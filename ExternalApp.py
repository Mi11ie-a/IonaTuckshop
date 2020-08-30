## Example of how the endpoints of the webapp could be acssed
import json
import urllib.request
import requests

url = "http://127.0.0.1:5000/processedata"
response = requests.get(url).json()


print(response['UserCount'])
