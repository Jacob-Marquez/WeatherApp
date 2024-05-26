import requests, json

api_key = "cf9c4ca5d56b79a82c23a0fdf05454cf"

base_url = "http://api.openweathermap.org/data/2.5/forecast?q="

city = input("Enter City: ")

api_call_url = base_url + city + "&appid=" + api_key + "&units=imperial"

response = requests.get(api_call_url)

x = response.json()

if x["cod"] != "404":

    y = x["main"]

    temp = y["temp"]

    print(temp)
else:
    print("error")
