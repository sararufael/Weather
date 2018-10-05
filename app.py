from flask import Flask, render_template, request

import requests

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/temperature', methods=['POST'])
def temperature():
    zipcode = request.form['zip']
    response = requests.get('https://api.openweathermap.org/data/2.5/weather?zip='+zipcode+',us&appid=637658b06ed3910bc1b22afd415ae4b4')
    json_object = response.json()
    temp_k = float(json_object['main']['temp'])
    temp_f = round((temp_k - 273.15) * 9/5 + 32, 2)
    return render_template('temperature.html', temp=temp_f)
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
