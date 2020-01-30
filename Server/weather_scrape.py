import requests, json 
def weather_forecast():
    api = "f5313b63fb4204670924c86d2fd950c1"
    url = "http://api.openweathermap.org/data/2.5/weather?"
    city = input("Enter city name : ") 
    complete_url = url + "appid=" + api + "&q=" + city
    response = requests.get(complete_url) 
    print(complete_url)
    x = response.json() 
    if x["cod"] != "404":  
        print(x)
  
    else: 
        print(" City Not Found ") 
weather_forecast()