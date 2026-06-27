import requests

resp = requests.post("http://127.0.0.1:6000/remember",
                     json={"note": "We rejected OAuth last year because dependency Y wasn’t ready."})
print(resp.json())
 