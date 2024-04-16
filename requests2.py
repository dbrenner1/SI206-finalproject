import requests
import sqlite3

url = "https://geography4.p.rapidapi.com/apis/geography/v1/city"

querystring = {"countryCode":"US","limit":"10"}

headers = {
	"X-RapidAPI-Key": "49d1e27d8amsh3fd4aa028fc9f55p16365ejsn450a8bb21b60",
	"X-RapidAPI-Host": "geography4.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

details = response.json()
print(details)
# TABLES 

conn = sqlite3.connect("weather_data.db")
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS geo_data
               (id TEXT, name TEXT, lat REAL, lng REAL, population INTEGER)''')



for item in details:
    id = item['id']
    name = item['name']
    lat = item['latLng']['lat']
    lng = item['latLng']['lng']
    population = item['population']
    cur.execute('INSERT INTO geo_data (id, name, lat, lng, population) VALUES (?, ?, ?, ?, ?)',
                (id, name, lat, lng, population))


conn.commit()
conn.close()

