from flask import Flask, render_template, request

import requests

import time

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weatherbyzip', methods=['POST'])
def weatherbyzip():
    zipcode = request.form['zip']
    # retrieving current weather data from API and creating weather dict
    current_response = requests.get('https://api.openweathermap.org/data/2.5/weather?zip='+zipcode+',us&appid=637658b06ed3910bc1b22afd415ae4b4')
    current_json = current_response.json()
    current_weather = {
        'temperature': round((float(current_json['main']['temp'])- 273.15) * 9 / 5 + 32, 2),
        'humidity': int(current_json['main']['humidity']),
        'wind': int(current_json['wind']['speed'])
    }
    # retrieving forecast data and appending 5-day forecast dicts to the forecast_weather
    forecast_response = requests.get('https://api.openweathermap.org/data/2.5/forecast?zip='+zipcode+',us&appid=637658b06ed3910bc1b22afd415ae4b4')
    forecast_json = forecast_response.json()
    forecast_list = forecast_json['list']
    forecast_weather = []
    for i, char in enumerate(forecast_list):
        forecast = {
            'dt': time.strftime('%A, %B %d %I:%M %p',time.localtime(forecast_list[i]['dt'])),
            'temperature': round((forecast_list[i]['main']['temp']- 273.15) * 9/5 + 32, 2),
            'description': forecast_list[i]['weather'][0]['description'],
            'icon': forecast_list[i]['weather'][0]['icon']
         }
        forecast_weather.append(forecast)
    return render_template('weatherbyzip.html', zipcode=zipcode, current_weather=current_weather, forecast_weather=forecast_weather)



if __name__ == '__main__':
    app.run(debug=True)
