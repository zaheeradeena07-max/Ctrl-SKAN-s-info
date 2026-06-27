import requests

resp = requests.post("http://127.0.0.1:6000/query",
                     json={"query": "OAuth"})
print(resp.json())
