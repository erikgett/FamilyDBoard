import requests

url = "https://yougile.itstrana.site/api-v2/auth/companies"

payload = {
    "login": "erik.gette@72list.ru",
    "password": "200erikgeTT",
    "name": "Страна Девелопмент"
}
headers = {"Content-Type": "application/json"}

response = requests.request("POST", url, json=payload, headers=headers)

print(response.text)
