import requests

url = "https://telesign-telesign-send-sms-verification-code-v1.p.rapidapi.com/sms-verification-code"

querystring = {"phoneNumber":"8237384898","verifyCode":"8237384898"}

payload = ""
headers = {
    'x-rapidapi-host': "telesign-telesign-send-sms-verification-code-v1.p.rapidapi.com",
    'x-rapidapi-key': "4kWxn9detWmshVzt8a2t1tXIgG5Op1dNI6OjsnRX3PnwwMBwf5",
    'content-type': "application/x-www-form-urlencoded"
    }

response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

print(response.text)