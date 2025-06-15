import pandas as pd
import sqlite3

# Step 1: Read the cleaned CSV file
df = pd.read_csv("geneva_weather_cleaned.csv")  # CSV dosyan bu dosyayla aynı klasörde olmalı

# Step 2: Create SQLite database and write table
conn = sqlite3.connect("geneva_weather.db")
df.to_sql("weather", conn, if_exists="replace", index=False)

# Step 3: Run a test query
query = "SELECT Year, [Avg Temp (°C)], [Total Rain (mm)] FROM weather LIMIT 10"
result = pd.read_sql(query, conn)

# Show result
# print(result)
