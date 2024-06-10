import requests

res = requests.get("http://127.0.01:3000/api/main")
print(res.json())