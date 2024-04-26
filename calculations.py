import sqlite3
import csv


# Connect to the database
conn = sqlite3.connect('weather_data.db')
cursor = conn.cursor()

# Execute a query to get the average population
cursor.execute('SELECT AVG(population) FROM geo_data')

# Fetch the result
average_population = cursor.fetchone()[0]

# Print the average population
print(f'Average population: {average_population}')

# Close the connection
conn.close()

with open('average_population.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['Average Population'])
    csvwriter.writerow([average_population])

print("CSV file 'average_population.csv' has been created with the average population.")