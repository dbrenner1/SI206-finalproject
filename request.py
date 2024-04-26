import requests
import sqlite3
import sys
import json
import random 
import time
conn = sqlite3.connect("weather_data.db")
cur = conn.cursor()


# Create the weather_data2 table if it doesn't exist
cur.execute('''CREATE TABLE IF NOT EXISTS weather_data2
               (id INTEGER PRIMARY KEY, address TEXT, days TEXT)''')

cur.execute('''CREATE TABLE IF NOT EXISTS day_data
               (weather_data_id INTEGER, datetime TEXT, temp REAL, feelslike REAL, humidity REAL, precip INTEGER, uvindex INTEGER, FOREIGN KEY (weather_data_id) REFERENCES weather_data2(id))''')

conn.commit()

key = "DDBAVR5TAUK7L7AKMGXYVDKTM"

def fetch_and_store_info():
    batch_size = 25
    items_fetched = 0
    while items_fetched < batch_size:
    
        random.seed(time.time())
        lat = -90 + (180 * random.random())
        lng = -180 + (360 * random.random())
        url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{lat}%2C%20{lng}?key={key}&contentType=json"
        response = requests.get(url)

        if response.status_code != 200:
            print('Unexpected Status code: ', response.status_code)
            sys.exit()

        info = response.json()

        address = info['resolvedAddress']

        cur.execute('INSERT OR IGNORE INTO weather_data2 (address, days) VALUES (?, ?)', (address, json.dumps(info)))

        weather_data_id = cur.lastrowid

        for day in info['days']:
            print(day)
            cur.execute('''INSERT OR IGNORE INTO day_data 
                        (weather_data_id, datetime, temp, feelslike, humidity, precip, uvindex)
                        VALUES (?, ?, ?, ?, ?, ?, ?)''',
                        (weather_data_id, day['datetime'], day['temp'], day['feelslike'], day['humidity'], day['precip'], day['uvindex']))

            conn.commit()
            items_fetched += 1
            if items_fetched >= batch_size:
                break

    print(f"Processed 25 entries")



fetch_and_store_info()
conn.close()



import sqlite3
import matplotlib.pyplot as plt

def plot_temp_vs_uvindex(db_path):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Retrieve uvindex and temp from the day_data table
    cur.execute("SELECT uvindex, temp FROM day_data ORDER BY uvindex")
    rows = cur.fetchall()

    # Close the connection to the database
    conn.close()

    # Unpack the rows into separate lists
    uvindex = [row[0] for row in rows]
    temperatures = [row[1] for row in rows]

    # Create a plot of temperature vs. uvindex
    plt.figure(figsize=(10, 5))
    plt.scatter(uvindex, temperatures, alpha=0.5, color='green') 
    
    # Add labels and title
    plt.xlabel('UV Index')
    plt.ylabel('Temperature (°F)')
    plt.title('Temperature vs. UV Index')
    plt.grid(True)
    plt.tight_layout()  # Adjust layout to fit all labels
    plt.show()

# Provide the path to your actual database file
plot_temp_vs_uvindex('weather_data.db')

