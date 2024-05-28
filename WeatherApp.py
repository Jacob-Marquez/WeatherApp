
from flask import Flask, render_template, request, redirect, url_for
import requests, json
import datetime

app = Flask(__name__)

def findDay(date):
    x = datetime.datetime(int(date[0:4]), int(date[5:7]), int(date[8:10]) )
    return x.strftime("%A")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        city = request.form['city']
        state = request.form['state']
        print("kys")
        return redirect(url_for('weather', city=city, state=state))
    return render_template('index.html')

@app.route("/weather/<city>/<state>")
def weather(city, state):

    api_key = "cf9c4ca5d56b79a82c23a0fdf05454cf"

    base_url = "http://api.openweathermap.org/data/2.5/forecast?q="

    api_call_url = base_url + city +"," + state + ",US" + "&appid=" + api_key + "&units=imperial"

    response = requests.get(api_call_url)

    x = response.json()

    if x["cod"] != "404":

        forecast = []

        day_data = x['list'][0]
        temp = day_data['dt_txt']
        date = findDay(day_data['dt_txt'])
        icon = day_data['weather'][0]['icon']

        base_icon_url = "http://openweathermap.org/img/wn/"
        icon_url = base_icon_url + icon + "@2x.png"
        
        forecast.append({
            'date': date,
                'temp': day_data['main']['temp'],
                'description': day_data['weather'][0]['description'],
                'icon' : icon_url
        })

        currentTime = int(temp[11:13])
        startingIndex = 0
        if(currentTime <= 15):
            startingIndex+=8

        while(currentTime != 15):
            currentTime+=3
            startingIndex+=1

        
        for i in range(startingIndex, 40, 8):
            day_data = x['list'][i]
            date = findDay(day_data['dt_txt'])
            print(day_data['dt_txt'])
            icon = day_data['weather'][0]['icon']
            icon_url = base_icon_url + icon + "@2x.png"
            print(icon_url)

            forecast.append({
                'date': date,
                'temp': day_data['main']['temp'],
                'description': day_data['weather'][0]['description'],
                'icon' : icon_url
            })

        return render_template('weather.html', city=city, state=state, forecast=forecast)
    else:
        print("error")
        return redirect(url_for('index'))


@app.route('/reset')
def reset():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
