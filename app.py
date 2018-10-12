from flask import Flask, render_template, request

import requests

import time

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/currentconditions', methods=['POST'])
def currentconditions():
    zipcode = request.form['zip']
    current_response = requests.get('https://api.openweathermap.org/data/2.5/weather?zip='+zipcode+',us&appid=637658b06ed3910bc1b22afd415ae4b4')
    forecast_response = requests.get('https://api.openweathermap.org/data/2.5/forecast?zip='+zipcode+',us&appid=637658b06ed3910bc1b22afd415ae4b4')
    current_json = current_response.json()
    forecast_json = forecast_response.json()
    forecast_list = forecast_json['list']
    forecast_weather = []
    for i, char in enumerate(forecast_list):
        weather = {
            'dt': time.strftime('%A, %B %d %I:%M %p',time.localtime(forecast_list[i]['dt'])),
            'temperature': round((forecast_list[i]['dt']- 273.15) * 9/5 + 32, 2),
            'description': forecast_list[i]['weather'][0]['description'],
            'icon': forecast_list[i]['weather'][0]['icon']
         }
        forecast_weather.append(weather)
    temp_k = float(current_json['main']['temp'])
    temp_f = round((temp_k - 273.15) * 9/5 + 32, 2)
    humidity = int(current_json['main']['humidity'])
    wind = int(current_json['wind']['speed'])
    return render_template('currentconditions.html', temp=temp_f, humidity=humidity, wind=wind, zipcode=zipcode, forecast_weather=forecast_weather)
@app.route('/tempdifference', methods=['POST'])
def tempdiffference():
    zip1 = request.form['zip1']
    zip2 = request.form['zip2']
    response1 = requests.get('https://api.openweathermap.org/data/2.5/weather?zip='+zip1+',us&appid=637658b06ed3910bc1b22afd415ae4b4')
    response2 = requests.get('https://api.openweathermap.org/data/2.5/weather?zip='+zip2+',us&appid=637658b06ed3910bc1b22afd415ae4b4')
    json_object1 = response1.json()
    json_object2 = response2.json()
    temp1_k = float(json_object1['main']['temp'])
    temp2_k = float(json_object2['main']['temp'])
    temp1_f = round((temp1_k - 273.15) * 9 / 5 + 32, 2)
    temp2_f = round((temp2_k - 273.15) * 9 / 5 + 32, 2)
    diff = round(abs(temp1_f-temp2_f),2)
    return render_template('tempdifference.html', diff=diff, zip1=zip1, zip2=zip2)


@app.route('/differnceform')
def differenceform():
    return render_template('differenceform.html')


if __name__ == '__main__':
    app.run(debug=True)
