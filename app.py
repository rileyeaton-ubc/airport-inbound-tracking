# Import necessary libraries
import pandas as pd
import datetime as dt
from dotenv import load_dotenv, dotenv_values
load_dotenv()  # take environment variables from .env
ENV = dotenv_values(".env")

# Import the configuration file (config.py)
import config
print(f'Starting Airport Inbound Tracker\nAirport: {config.airport}\nDate: {config.date}')
# Import the helper functions from conversions.py
import helpers.conversions as convert
# Import http request helper
from helpers.http import HttpClient

# Load the aircraft database CSV into a data frame
aircraft_database = pd.read_csv("./data/aircraft_data.csv")

# Initialize the HTTP helper
http_client = HttpClient(base_url="https://aeroapi.flightaware.com/aeroapi/",
                        headers={"x-apikey": ENV["AEROAPI_KEY"]},)

# Calculate the current date in the local timezone.
current_date = dt.datetime.now() + dt.timedelta(hours=config.time_zone_shift)
# Set the start and end times to be the beginning and end of that day in UTC equivalent
current_date = current_date.replace(hour=0, minute=0, second=0)
start_time = current_date - dt.timedelta(hours=config.time_zone_shift)
current_date = current_date.replace(hour=23, minute=59, second=59)
end_time = current_date - dt.timedelta(hours=config.time_zone_shift)
# Express these times in the format:  
date_format = '%Y-%m-%dT%H:%M:%S%z'
start_time = start_time.strftime(date_format)
end_time = end_time.strftime(date_format)

#  Set the parameters, and make a request for the current flights to the given airport
params = {
    "start": start_time,
    "end": end_time,
}

# Use the HTTP client to make a GET request to the OpenWeather API
airport_results = http_client.get(endpoint=f'airports/{config.airport}/flights/scheduled_arrivals', params=params)
arrivals = []
for arrival in airport_results['scheduled_arrivals']:
    # Lookup the aircraft type
    current_aircraft = aircraft_database[aircraft_database['ICAO_Code'] == arrival["aircraft_type"].strip()]
    
    # calculate the weighted score of the aircraft based on numerous factors
    score = (
        1
    )

    # Store key aircraft metrics in a standard array
    key_aircraft_metrics = {"model": current_aircraft.Model_FAA.values[0],
                            "overall_score": score,
                            "ADG": convert.roman_numerals_to_int(current_aircraft.ADG.values[0]), 
                            "TDG": int(current_aircraft.TDG.values[0][0]), 
                            "approach_speed": float(current_aircraft.Approach_Speed_knot.values[0]), 
                            "length": float(current_aircraft.Length_ft.values[0]), 
                            "tail_height": float(current_aircraft.Tail_Height_at_OEW_ft.values[0]), 
                            "wheelbase": float(current_aircraft.Wheelbase_ft.values[0])}

    # Shift the scheduled arrival time to be in the selected time zone based on the integer shift from UTC in config
    scheduled_out = "Unknown"
    scheduled_in = "Unknown"
    if arrival["scheduled_in"]: 
        scheduled_in = dt.datetime.strptime(arrival["scheduled_in"], date_format)
        scheduled_in = scheduled_in + dt.timedelta(hours=config.time_zone_shift)
    if arrival["scheduled_out"]: 
        scheduled_out = dt.datetime.strptime(arrival["scheduled_out"], date_format)
        scheduled_out = scheduled_out + dt.timedelta(hours=config.time_zone_shift)

    # Append the arrival information to the arrivals list
    arrivalObject = {
        "ident": arrival["ident"],
        "origin": arrival["origin"]["code"],
        "origin_city": arrival["origin"]["city"],
        "scheduled_arrival_time": scheduled_in,
        "scheduled_departure_time": scheduled_out,
        "aircraft_info": key_aircraft_metrics
    }
    arrivals.append(arrivalObject)
print(arrivals)

# Find the highest ADG, TDG, approach speed, for the day
highest_ADG = -1
highest_TDG = -1
highest_approach_speed = -1
for flight in arrivals:
    if flight["aircraft_info"]["ADG"] > highest_ADG:
        highest_ADG = flight["aircraft_info"]["ADG"]
    if flight["aircraft_info"]["TDG"] > highest_TDG:
        highest_TDG = flight["aircraft_info"]["TDG"]
    if flight["aircraft_info"]["approach_speed"] > highest_approach_speed:
        highest_approach_speed = flight["aircraft_info"]["approach_speed"]

# Get all the aircraft that have the highest ADG, TDG, and approach speed
highest_ADG_TDG_aircraft = []
highest_approach_speed_aircraft = []
for flight in arrivals:
    if flight["aircraft_info"]["ADG"] == highest_ADG and flight["aircraft_info"]["TDG"] == highest_TDG:
        highest_ADG_TDG_aircraft.append(flight)
    if flight["aircraft_info"]["approach_speed"] == highest_approach_speed:
        highest_approach_speed_aircraft.append(flight)

print("-------------------------------- Results --------------------------------------")
# Print the aircraft with the highest ADG and TDG
print(f'The following aircraft arriving today at {config.airport} have the highest ADG and TDG ({highest_ADG}/6, {highest_TDG}/6):')
for flight in highest_ADG_TDG_aircraft:
    time = dt.datetime.strftime(flight["scheduled_arrival_time"], '%H:%M')
    print(f"""  ● '{flight["aircraft_info"]["model"]}' arriving from '{flight["origin_city"]}' is scheduled to land at '{time}'""")
print("-------------------------------------------------------------------------------")

# Print the aircraft with the highest approach speed
print(f'The following aircraft arriving today at {config.airport} have the highest approach speed ({highest_approach_speed} knots):')
for flight in highest_approach_speed_aircraft:
    time = dt.datetime.strftime(flight["scheduled_arrival_time"], '%H:%M')
    print(f"""  ● '{flight["aircraft_info"]["model"]}' arriving from '{flight["origin_city"]}' is scheduled to land at '{time}'""")
print("-------------------------------------------------------------------------------")