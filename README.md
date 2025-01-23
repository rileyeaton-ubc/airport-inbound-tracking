# Airport Significant Flight Tracker

This project is intended to allows enthusiast flight trackers to be notified of significant inbound/outbound flights at their local airport for viewing

Each user must acquire their own AeroAPI API key from FlightAware [here](https://www.flightaware.com/commercial/aeroapi/), and place it into an .ENV file (there is a sample in the repo).

## Quickstart

1. Configure the application's settings by editing the values found in `config.py`

- You can change the desired airport by editing the `airport` value. This is the ICAO airport code, and unlikely to be what it is known locally as (IATA). For example New York's JFK airport has the ICAO code: KJFK (the K prefix is usually used for airports in the United States)
- The `time_zone_shift` is an integer value representing the number of hours difference from UTC your current time zone is. For example, if your airport/local time zone is PST, this value would be -8.
- The `date` variable should stay as "TODAY" until the feature to change dates is implemented

2. Navigate to the root folder of the repo in your terminal, and using Python `3.12.x`, install the requirements with `python -m pip install -r requirements.txt`

3. Run the application using `python app.py`
