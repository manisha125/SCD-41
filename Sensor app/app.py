 
from flask import Flask, render_template, jsonify 

import board 

import adafruit_scd4x 

import time 



"""================================================================================================================================================================================================================= 

10 Oct 2023, Manisha Dagar 

  

Project:  Integrating SCD 41 Sensor with Raspi and making webserver 

Flask shows real time data on server in form of chat through plotly and table 

Important considerations and struggles:  Trouble shootings on harware-raspi communication (Used SCD4X official Library),Showing real time data on server, Fixing content table and thier alignment 

  

  

  

=================================================================================================================================================================================================================""" 

  

"""===================================================================== 

Setting up flask app  

Code: Official SC4x available code 

=====================================================================""" 

app = Flask(__name__) 

  

# Starting SCD4X sensor 

try: 

    i2c = board.I2C() 

    scd4x = adafruit_scd4x.SCD4X(i2c) 

    scd4x.start_periodic_measurement() 

except (OSError, RuntimeError): 

    scd4x = None 

  

# Initializing data arrays 

timestamps = [] 

co2_data = [] 

temperature_data = [] 

humidity_data = [] 

  
# Rendering template  

@app.route('/') 

def index(): 

    return render_template('index1.1.html') 

  

  

# Seting up route 

@app.route('/data') 

def get_data(): 

    if scd4x: 

        while not scd4x.data_ready: 

            time.sleep(0.5) 

  

        co2_ppm = scd4x.CO2 

        temperature = scd4x.temperature 

        humidity = scd4x.relative_humidity 

        timestamp = time.strftime('%H:%M:%S') 

  

        # Appending Sensor data points to arrays 

        timestamps.append(timestamp) 

        co2_data.append(co2_ppm) 

        temperature_data.append(temperature) 

        humidity_data.append(humidity) 

  

        # Showing only last 15 points 

         

        max_data_points = 15 

        

        if len(timestamps) > max_data_points: 

            timestamps.pop(0) 

            co2_data.pop(0) 

            temperature_data.pop(0) 

            humidity_data.pop(0) 

  

        data = { 

            'co2_ppm': co2_ppm, 

            'temperature': temperature, 

            'humidity': humidity, 

        } 

    else: 

         

        # Error when sensor doesn't send data 

        data = { 

            'error': 'Sensor data not working', 

        } 

  

  

    return jsonify(data) 

  

# running program  h

if __name__ == '__main__': 

    app.run(debug=True, host='192.168.0.115') 

     

     



 
