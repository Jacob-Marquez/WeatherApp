from flask import Flask, render_template, request, redirect, url_for
import requests
import datetime

app = Flask(__name__)

# Replace with your OpenWeatherMap API key
API_KEY = 'cf9c4ca5d56b79a82c23a0fdf05454cf'

# route to home page
@app.route('/')
def index():
    return render_template('index.html')

# Find necessary information and route to forecast page
@app.route('/forecast', methods=['POST'])
def forecast():
    city = request.form['city']
    state = request.form['state']
    
    # Use openWeatherMap API to retrieve weather forecast data
    api_key = "cf9c4ca5d56b79a82c23a0fdf05454cf"
    base_url = "http://api.openweathermap.org/data/2.5/forecast?q="
    api_call_url = base_url + city +"," + state + ",US" + "&appid=" + api_key + "&units=imperial"
    response = requests.get(api_call_url)
    data = response.json()

    # check if response works
    if response.status_code == 200:
        forecasts = data['list']
        prediction = []
        
        base_icon_url = "http://openweathermap.org/img/wn/"

        # From the 40 3-hour predictions take one from each day
        for i in range(0, 40, 8):
            day_data = forecasts[i]
            date = day_data['dt_txt']
            
            # change from date to day of the week
            x = datetime.datetime(int(date[0:4]), int(date[5:7]), int(date[8:10]) )
            date = x.strftime("%A")
            
            # icon image url
            icon = day_data['weather'][0]['icon']
            icon_url = base_icon_url + icon + "@2x.png"
            
            prediction.append({
                'date': date,
                'temp': day_data['main']['temp'],
                'description': day_data['weather'][0]['description'],
                'icon' : icon_url
                })
        
        # pass to forecast.html to display 
        return render_template('forecast.html', city=city, state=state, prediction=prediction)
    else:
        error_message = data.get('message', 'An error occurred while fetching the data.')
        return render_template('index.html', error=error_message)

if __name__ == '__main__':
    app.run(debug=True)
