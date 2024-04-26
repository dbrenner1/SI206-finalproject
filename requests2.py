import requests
import sqlite3
import random
import time
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

conn = sqlite3.connect("weather_data.db")
cur = conn.cursor()


cur.execute('''CREATE TABLE IF NOT EXISTS geo_data
               (name TEXT, lat REAL, lng REAL, population INTEGER, country_code TEXT)''')
cur.execute('''CREATE TABLE IF NOT EXISTS country_mapping
               (country_code TEXT PRIMARY KEY, code_number INTEGER)''')

country_codes = ["US", "CA", "GB", "FR", "DE", "IT", "JP", "AU", "BR", "IN", "ES", "MX", "CN", "RU", "NL", "SE", "CH", "KR", "SG", "ID", "TH", "MY", "VN", "PH", "TW", "HK", "AR", "CL", "CO", "PE", "EC", "ZA", "EG", "NG", "KE", "MA", "SA", "AE", "IL", "TR", "GR", "FI", "DK", "NO", "CZ", "PL", "HU", "AT", "BE"]
for i, code in enumerate(country_codes, start=1):
    cur.execute("INSERT OR IGNORE INTO country_mapping (country_code, code_number) VALUES (?, ?)", (code, i))


conn.commit()


url = "https://geography4.p.rapidapi.com/apis/geography/v1/city"
headers = {
    "X-RapidAPI-Key": "262779a44dmshb169a29003312d8p1e7d3djsn897bdfe4b4a3",
    "X-RapidAPI-Host": "geography4.p.rapidapi.com"
}


def fetch_and_store_info():
    batch_size = 25
    items_fetched = 0
    while items_fetched < batch_size:
    
        random.seed(time.time())

        country_code = random.choice(country_codes)
        querystring = {
            "countryCode": country_code
        }

        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()

        for i in data:
            name = i['name']
            lat = i['latLng']['lat']
            lng = i['latLng']['lng']
            population = i['population']
            country_code = i['countryCode']

            # Get the code_number for the country code
            cur.execute("SELECT code_number FROM country_mapping WHERE country_code=?", (country_code,))
            code_number = cur.fetchone()[0]

# Check if the city already exists in geo_data
            cur.execute('SELECT name FROM geo_data WHERE name=? AND country_code=?', (name, code_number))
            existing_city = cur.fetchone()

            if existing_city:
    # Update the existing city's information
                cur.execute('UPDATE geo_data SET lat=?, lng=?, population=? WHERE name=? AND country_code=?',
                (lat, lng, population, name, code_number))
            else:
    # Insert data into geo_data with the code_number
                cur.execute('INSERT INTO geo_data (name, lat, lng, population, country_code) VALUES (?, ?, ?, ?, ?)',
                (name, lat, lng, population, code_number))
 
            conn.commit()

            items_fetched += 1
            if items_fetched >= batch_size:
                break

            
fetch_and_store_info()




def plot_population_from_db(db_path):
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # SQL query to select location names and their populations
    cur.execute("SELECT name, population FROM geo_data ORDER BY population DESC")
    rows = cur.fetchall()

    # Close the connection to the database
    conn.close()

    # Extract location names and populations from the rows
    locations = [row[0] for row in rows]
    populations = [row[1] for row in rows]

    # Create a horizontal bar chart
    plt.figure(figsize=(10, 8))
    plt.barh(locations, populations, color='hotpink')

    # Add labels and title to the chart
    plt.xlabel('Population')
    plt.ylabel('Location')
    plt.title('Population by Location')

    # Invert y-axis to have the highest population on top
    plt.gca().invert_yaxis()
    plt.tight_layout()  # Adjust layout to fit all labels
    plt.show()



plot_population_from_db('weather_data.db')

# We have to figure out how to join geo_data and day_data so that we can get average temperature by location
def plot_average_temperature_by_location(db_path):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # SQL query that joins the day_data and geo_data tables and calculates the average temperature for each location.
    # This assumes there's a logical way to join the two tables (like a shared 'name' or 'id' column).
    query = """
    SELECT g.name, AVG(d.temp) as avg_temp
    FROM geo_data g
    JOIN day_data d ON g.name = d.name
    GROUP BY g.name
    ORDER BY avg_temp DESC
    """
    cur.execute(query)
    result = cur.fetchall()

    # Close the database connection
    conn.close()

    # Unpack the result into separate lists
    locations = [row[0] for row in result]
    avg_temperatures = [row[1] for row in result]

    # Create a bar chart
    plt.figure(figsize=(10, 5))
    plt.bar(locations, avg_temperatures, color='skyblue')

    # Add labels and title
    plt.xlabel('Location')
    plt.ylabel('Average Temperature (°F)')
    plt.title('Average Temperature by Location')
    plt.xticks(rotation=45, ha='right')  # Rotate location names for better readability
    plt.tight_layout()  # Adjust layout to fit all labels
    plt.show()

# Provide the path to your actual database file
plot_average_temperature_by_location('weather_data.db')

