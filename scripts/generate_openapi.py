import requests
host = "http://localhost:8000"
result = "./spec/openapi.json"

response = requests.get(host + "/openapi.json")

print(response.text)

f = open(result, "w")
f.write(response.text)
f.close()
