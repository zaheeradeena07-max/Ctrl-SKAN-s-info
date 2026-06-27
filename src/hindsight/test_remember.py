import requests

resp = requests.post("http://127.0.0.1:6000/remember",
                     json={"note": "Ticket #1234 was resolved by applying a billing patch."})
print(resp.json())
