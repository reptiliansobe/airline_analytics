import pandas as pd
import sqlite3
import os

#establish paths and database connection
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "airline.db")
OUTPUT_DIR = os.path.join(BASE_DIR, "data", "outputs")

os.makedirs(OUTPUT_DIR, exist_ok=True)

conn = sqlite3.connect(DB_PATH)

#loading data from sql

flights = pd.read_sql("SELECT * FROM flights", conn)
crew = pd.read_sql("SELECT * FROM crew", conn)

conn.close()

#converting the dates
flights["flight_date"] = pd.to_datetime(flights["flight_date"])


#on time performance
flights_active = flights[flights["cancelled"] == 0]

on_time_by_origin = (
    flights_active["arrival_delay_minutes"] <= 0
).groupby(flights_active["origin"]).mean().reset_index()

on_time_by_origin.columns = ["origin", "on_time_percentage"]
on_time_by_origin["on_time_percentage"] *= 100

#monthly delay trends
flights_active["flight_month"] = flights_active["flight_date"].dt.to_period("M")

monthly_delay = (
    flights_active
    .groupby("flight_month")["arrival_delay_minutes"]
    .mean()
    .reset_index()   
)

monthly_delay["flight_month"] = monthly_delay["flight_month"].astype(str)

#find route performance

route_performance = (
    flights_active
    .groupby(["origin", "destination"])
    .agg(
        avg_arrival_delay=("arrival_delay_minutes", "mean"),
        total_flights=("flight_id", "count")
    )

    .reset_index()
)

#comparing crew hours vs delays

crew_hours_per_flight = (
    crew.groupby("flight_id")["hours_worked"]
    .mean()
    .reset_index()
)

crew_delay_analysis = pd.merge(
    flights_active,
    crew_hours_per_flight,
    on="flight_id",
    how="inner"

)[["flight_id", "arrival_delay_minutes", "hours_worked"]]

#exporting for power bi functionality

on_time_by_origin.to_csv(os.path.join(OUTPUT_DIR, "on_time_by_origin.csv"), index=False)
monthly_delay.to_csv(os.path.join(OUTPUT_DIR, "monthly_delay.csv"), index=False)
route_performance.to_csv(os.path.join(OUTPUT_DIR, "route_performance.csv"), index=False)
crew_delay_analysis.to_csv(os.path.join(OUTPUT_DIR, "crew_delay_analysis.csv"), index=False)

print("Analysis complete, power bi files created")

