import requests
URL = "http://127.0.0.1:8000"

# user_credentials = {
#   "username": "thanush-2",
#   "password": "kickthebucket",
#   "role": "staff"
# }

# response = requests.post(url=URL+"/register", json = user_credentials)
# print(response.status_code)
# print(response.json())

user_credentials = {
  "username": "thanush-2",
  "password": "kickthebucket",
  "role": "staff"
}

response = requests.post(url = URL+"/login", json = user_credentials)
response_json = response.json()
access_token = response_json["access_token"]
refresh_token = response_json["refresh_token"]

header = {"token": access_token}
response = requests.get(url=URL+"/packages", headers = header)
print(response.json())

details = {
  "name": "abc",
  "destination": "abc",
  "weight": 1,
  "status": "dispatched"
}

response = requests.post(url=URL+"/packages", json = details, headers = header)
print(response.json())

response = requests.get(url = URL+"/packages/1", headers=header)
print(response.json())


details = {
    "name": "abc",
      "destination": "abc",
      "weight": 1,
      "status": "ready"
}
response = requests.patch(url = URL+"/packages/1", json=details, headers = header)
print(response.status_code)
print(response.json())

response = requests.delete(url = URL+"/packages/2", headers = header)