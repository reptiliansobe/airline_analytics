import pandas as pd
import sqlite3
import os

#find file paths for data
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

#load the csv files
flights = pd.read_csv(os.path.join(DATA_DIR, "flights.csv"))
crew = pd.read_csv(os.path.join(DATA_DIR, "crew.csv"))

#create the sql database
conn = sqlite3.connect(os.path.join(BASE_DIR, "airline.db"))

#load tables into sql
flights.to_sql("flights", conn, if_exists="replace", index=False)
crew.to_sql("crew", conn, if_exists="replace", index=False)

print("Tables loaded into SQLite database")


#sql queries

#this query will find the average delay in minutes per route
query_avg_delay = """

SELECT
    origin,
    destination,
    AVG(arrival_delay_minutes) AS avg_arrival_delay
FROM flights
WHERE cancelled = 0
GROUP BY origin, destination
ORDER BY avg_arrival_delay DESC;
"""
avg_delay_df = round(pd.read_sql(query_avg_delay, conn), 0)
print("\nAverage Delay Per Route:")
print(avg_delay_df.head(), " minutes")



#this query will find the cancellation rate per route
query_cancel_rate = """
SELECT
    origin,
    destination,
    AVG(cancelled) AS cancellation_rate
FROM flights
GROUP BY origin, destination
ORDER BY cancellation_rate DESC;
"""

cancel_rate_df = pd.read_sql(query_cancel_rate, conn)
print("\nCancellation Rate Per Route:")
print(round(cancel_rate_df.head(), 2), " percent")

conn.close()

