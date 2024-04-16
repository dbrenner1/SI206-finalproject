import requests
import sqlite3
import sys
import json

response = requests.request("GET", "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/ann%20arbor?unitGroup=us&include=days&key=TLUHVVEGRDQLTZFK6RY3PCWY4&contentType=json")
if response.status_code!=200:
  print('Unexpected Status code: ', response.status_code)
  sys.exit()  


# Parse the results as JSON
info = response.json()
# print(info)

conn = sqlite3.connect("weather_data.db")
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS weather_data2
               (id INTEGER PRIMARY KEY, address TEXT, days TEXT)''')
cur.execute('''CREATE TABLE IF NOT EXISTS day_data
            (weather_data_id INTEGER, datetime TEXT, temp REAL, feelslike REAL, humidity REAL, precip INTEGER, uvindex INTEGER, conditions TEXT, description TEXT)''')


address = info.get('resolvedAddress', '')
cur.execute('INSERT INTO weather_data2 (address, days) VALUES (?, ?)', (address, json.dumps(info)))

weather_data_id = cur.lastrowid

for day in info['days']:
    cur.execute('''INSERT INTO day_data 
                   (weather_data_id, datetime, temp, feelslike, humidity, precip, uvindex, conditions, description)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                   (weather_data_id, day['datetime'], day['temp'], day['feelslike'], day['humidity'], day['precip'], day['uvindex'], day['conditions'], day['description']))

conn.commit()
conn.close()
