import requests

url = "http://127.0.0.1:5000/query"
headers = {
    "Authorization": "Bearer cascadeflow_key_123",
    "Content-Type": "application/json"
}
data = {"query": "System outage yesterday"}

response = requests.post(url, headers=headers, json=data)
print(response.json())
