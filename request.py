import requests
import sqlite3
import sys
import json

# f string in URL to change lat lgn each time (like import requests)

response = requests.request("GET", "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/ann%20arbor?unitGroup=us&include=days&key=TLUHVVEGRDQLTZFK6RY3PCWY4&contentType=json")
if response.status_code!=200:
  print('Unexpected Status code: ', response.status_code)
  sys.exit()  


# Parse the results as JSON
info = response.json()
# print(info)

conn = sqlite3.connect("weather_data.db")
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS day_data')

cur.execute('''CREATE TABLE IF NOT EXISTS weather_data2
               (id INTEGER PRIMARY KEY, address TEXT, days TEXT)''')
cur.execute('''CREATE TABLE IF NOT EXISTS day_data
            (unique_id INTEGER, datetime TEXT, temp REAL, feelslike REAL, humidity REAL, precip INTEGER, uvindex INTEGER, conditions TEXT, description TEXT)''')


   
address = info.get('resolvedAddress', '')
cur.execute('INSERT INTO weather_data2 (address, days) VALUES (?, ?)', (address, json.dumps(info)))

unique_id = 0
for day in info['days']:
    unique_id += 1
    print(unique_id)
    cur.execute('''INSERT INTO day_data 
                   (unique_id, datetime, temp, feelslike, humidity, precip, uvindex, conditions, description)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                   (unique_id, day['datetime'], day['temp'], day['feelslike'], day['humidity'], day['precip'], day['uvindex'], day['conditions'], day['description']))

conn.commit()
conn.close()

