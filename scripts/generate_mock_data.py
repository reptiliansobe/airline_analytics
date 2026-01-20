#this file will generate the mock data 

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

np.random.seed(42)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

#generate the flight data


#generating 500 flights with these origins and destinations
num_flights = 500
origins = ['LAS', 'LAX', 'DEN', 'PHX', 'SFO']
destinations = ['LAS', 'LAX', 'DEN', 'PHX', 'SFO']

#creating flight ids, dates, and routes
flight_ids = [f"FL{1000+i}" for i in range(num_flights)]
flight_dates = [datetime(2025, 1, 1) + timedelta(days=np.random.randint(0,180)) for _ in range(num_flights)]
origin_choices = np.random.choice(origins, num_flights)
destination_choices = np.random.choice(destinations, num_flights)

#creating random arrival delays which may be early or on-time, same with departures
#also the chance of cancelled flights at 10% cancelled
arrival_delays = np.random.normal(loc=5, scale=20, size=num_flights).astype(int)
departure_delays = np.random.normal(loc=3, scale=15, size=num_flights).astype(int)
cancelled = np.random.choice([0,1], size=num_flights, p=[0.9,0.1])

#putting all the data together
flights_df = pd.DataFrame({
    'flight_id': flight_ids,
    'flight_date': flight_dates,
    'origin': origin_choices,
    'destination': destination_choices,
    'scheduled_departure': [f"{np.random.randint(0,24):02d}:{np.random.randint(0,60):02d}" for _ in range(num_flights)],
    'actual_departure': [f"{np.random.randint(0,24):02d}:{np.random.randint(0,60):02d}" for _ in range(num_flights)],
    'arrival_delay_minutes': arrival_delays,
    'departure_delay_minutes': departure_delays,
    'cancelled': cancelled
    })

#putting all the mock data into a csv file
flights_df.to_csv(os.path.join(DATA_DIR, "flights.csv"), index=False)
print("Flight data generated.")

#also generating flight crew data

#different crew roles and 2000 total crew
crew_roles = ['Pilot', 'Attendant', 'Co-Pilot']
num_crew = 2000

#creating crew ids, flights theyre on, and hours worked

crew_ids=[f"C{1000+i}" for i in range(num_crew)]
crew_flights = np.random.choice(flight_ids, num_crew)
crew_roles_choices = np.random.choice(crew_roles, num_crew)
hours_worked = np.random.normal(loc=8, scale=2, size=num_crew).round(1)

#loading all the crew data into a data frame
crew_df = pd.DataFrame({
    'crew_id': crew_ids,
    'flight_id': crew_flights,
    'crew_role': crew_roles_choices,
    'hours_worked': hours_worked
})

crew_df.to_csv(os.path.join(DATA_DIR, "crew.csv"), index=False)
print("Crew data generated.")

