

import requests
import sqlite3
import random


conn = sqlite3.connect("weather_data.db")
cur = conn.cursor()



cur.execute('''CREATE TABLE IF NOT EXISTS weather_data
               (id INTEGER PRIMARY KEY, city_name TEXT, lat REAL, lon REAL, timezone_id INTEGER)''')

cur.execute('''CREATE TABLE IF NOT EXISTS timezones
               (id INTEGER PRIMARY KEY, timezone TEXT)''')

conn.commit()

url = "https://weatherbit-v1-mashape.p.rapidapi.com/forecast/daily"
headers = {
    "X-RapidAPI-Key": "262779a44dmshb169a29003312d8p1e7d3djsn897bdfe4b4a3",
    "X-RapidAPI-Host": "weatherbit-v1-mashape.p.rapidapi.com"
}

batch_size = 25
for _ in range(batch_size):
    lat = random.uniform(-90, 90)
    lon = random.uniform(-180, 180)

    querystring = {
        "lat": lat,
        "lon": lon
    }
    try:
        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()
        if 'data' in data:
            city_name = data['city_name']
            lat = data['lat']
            lon = data['lon']
            timezone = data['timezone']

            # Check if the timezone already exists in the timezones table
            cur.execute('SELECT id FROM timezones WHERE timezone = ?', (timezone,))
            row = cur.fetchone()
            if row is None:
                # If not, insert it into the timezones table and get its id
                cur.execute('INSERT OR IGNORE INTO timezones (timezone) VALUES (?)', (timezone,))
                timezone_id = cur.lastrowid
            else:
                timezone_id = row[0]

            # Insert the weather data into the weather_data table
            cur.execute('INSERT OR IGNORE INTO weather_data (city_name, lat, lon, timezone_id) VALUES (?, ?, ?, ?)', (city_name, lat, lon, timezone_id))
    except Exception as e:
        print(f"An error occurred: {e}")

    conn.commit()

conn.close()

import sqlite3
import matplotlib.pyplot as plt
import random

def plot_cities_by_state(db_path):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # SQL query to count the number of cities for each timezone_id
    cur.execute("SELECT timezone_id, COUNT(city_name) FROM weather_data GROUP BY timezone_id")
    result = cur.fetchall()

    # Close the database connection
    conn.close()

    # Unpack the result into separate lists
    timezone_ids = [row[0] for row in result]
    city_counts = [row[1] for row in result]

    # Create a list of unique timezones
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT id, timezone FROM timezones")
    timezones = dict(cur.fetchall())
    conn.close()

    # Create a color map with a different color for each timezone
    color_map = {}
    for timezone_id in timezone_ids:
        if timezone_id not in color_map:
            color_map[timezone_id] = (random.random(), random.random(), random.random())

    # Create a bar chart with different colors for each timezone
    plt.figure(figsize=(10, 5))
    bars = plt.bar(timezone_ids, city_counts, color=[color_map[tz_id] for tz_id in timezone_ids])

    # Add legend for timezone colors
    legend_handles = [plt.Rectangle((0,0),1,1, color=color_map[tz_id]) for tz_id in timezones.keys()]
    plt.legend(legend_handles, timezones.values(), title='Timezones', loc='center left', bbox_to_anchor=(1, 0.5))

    # Add labels and title
    plt.xlabel('Timezone ID')
    plt.ylabel('Number of Cities')
    plt.title('Number of Cities by Timezone ID in Weather Data')
    plt.xticks(timezone_ids, rotation=45)  
    plt.tight_layout() 
    plt.show()

plot_cities_by_state('weather_data.db')
