import requests
import sqlite3

url = "https://weatherbit-v1-mashape.p.rapidapi.com/forecast/daily"

headers = {
	"X-RapidAPI-Key": "f2d8fcd218msh6df8eb3d1d73f9ap11e9c9jsn50883ebfe3a4",
	"X-RapidAPI-Host": "weatherbit-v1-mashape.p.rapidapi.com"
}
all_data = []
lat = 0
lng = 0

all_data = []
for i in range(0, 100):
    lat += i  # or whatever initial latitude value you want
    lng += i  # or whatever initial longitude value you want
    querystring = {"lat": str(lat), "lng": str(lng)}
    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()
    print(data)
    all_data.append(data)

print(all_data)

conn = sqlite3.connect("weather_data.db")
cur = conn.cursor()

# Create table if it doesn't exist

# cur.execute('DROP TABLE IF EXISTS weather_data')
cur.execute('''CREATE TABLE IF NOT EXISTS weather_data
               (city_name TEXT, lat REAL, lng REAL, state_code TEXT, timezone TEXT)''')

for item in all_data:
    city_name = item['city_name']
    name = item['name']
    lat = item['lat']
    lng = item['lng']
    state_code = item['state_code']
    timezone = item['timezone']
    cur.execute('INSERT OR IGNORE INTO weather_data (city_name, lat, lng, state_code, timezone) VALUES (?, ?, ?, ?, ?)', (city_name, lat, lng, state_code, timezone))



# DB COMMENTED - started to make a function tryinrg to use temperature(?) 
# but there is no temperature info in the API... we can use this function on the other API. 


# Extract temperatures from database
# def extract_temperatures(weather_data):
#     temperatures = []

#     for entry in weather_data['data']:
        
#         temperatures.append(entry['temp'])

#     return temperatures

# temperatures = extract_temperatures(data)
# print(temperatures)

# import datetime

# # Calculate average temperature each day
# def average_temperatures_by_day(weather_data):
#     daily_temperatures = {}
    
#     # Extract temperatures and organize by day
#     for entry in weather_data['data']:
#         # Parse the timestamp to extract the date only
#         date = datetime.datetime.strptime(entry['timestamp_utc'], "%Y-%m-%dT%H:%M:%S").date()
#         temperature = entry['temp']
        
#         if date not in daily_temperatures:
#             daily_temperatures[date] = []
#         daily_temperatures[date].append(temperature)
    
#     # Calculate average temperature for each day
#     average_temperatures = {date: sum(temps) / len(temps) for date, temps in daily_temperatures.items()}
    
#     return average_temperatures

# DB COMMENTED


# def get_precipitation(location, date):
#     """
#     Retrieves precipitation data for a specified location and date using the Visual Crossing Weather API.

#     Args:
#     location (str): The location for which to retrieve weather data.
#     date (str): The date for which to retrieve weather data in the format 'YYYY-MM-DD'.

#     Returns:
#     float: The amount of precipitation for the given date in inches or a message indicating no data.
#     """
#     api_key = 'YOUR_API_KEY'
#     url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}/{date}?unitGroup=us&include=days&key={api_key}&contentType=json"

#     try:
#         with urllib.request.urlopen(url) as response:
#             jsonData = json.load(response)
#             # Check if 'days' data is available for the specified date
#             if 'days' in jsonData and jsonData['days']:
#                 for day_data in jsonData['days']:
#                     if day_data['datetime'] == date:
#                         precipitation = day_data.get('precip', 0.0)  
#                         return precipitation
#                 return "No precipitation data available for this date."
#             else:
#                 return "No data available for the specified location and date."

#     except urllib.error.HTTPError as e:
#         ErrorInfo = e.read().decode()
#         print('HTTP Error code:', e.code, ErrorInfo)
#         sys.exit(1)

#     except urllib.error.URLError as e:
#         ErrorInfo = e.reason
#         print('URL Error:', ErrorInfo)
#         sys.exit(1)

# # Example usage:
# location = "Ann Arbor"
# date = "2024-04-16"  # Use the format 'YYYY-MM-DD'
# precipitation = get_precipitation(location, date)
# print(f"Precipitation in {location} on {date} is: {precipitation} inches.")
