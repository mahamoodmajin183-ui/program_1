"""
Creates two SYNTHETIC sample files so Experiments 1 and 3 can run on a machine that does not have your lab's crime.csv.

    SAMPLE_crime_india_style.csv   - same columns as the India crime table printed in Experiment 1's output
                                      (Report Number, Date Reported, ..., Case Closed, Date Case Closed)
    SAMPLE_crime_yearly.csv        - the columns Experiment 3 plots (Year, Population, Murder, Assault, Robbery, CarTheft)

The values are RANDOM (seeded).  They are NOT the real dataset and results computed from them will not match
the lab manual.  Replace with your real crime.csv for the practical (see README).

Run:  python make_sample_crime.py
"""
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
rng = np.random.default_rng(0)

n = 2000
cities = ["Ahmedabad", "Chennai", "Ludhiana", "Pune", "Mumbai", "Srinagar", "Kolkata", "Delhi", "Bengaluru", "Hyderabad"]
descs = ["IDENTITY THEFT", "HOMICIDE", "KIDNAPPING", "BURGLARY", "VANDALISM", "TRAFFIC VIOLATION",
         "PUBLIC INTOXICATION", "COUNTERFEITING", "ILLEGAL POSSESSION"]
weapons = ["Blunt Object", "Poison", "Firearm", "Knife", "Explosives", "None", "Other"]
domains = ["Violent Crime", "Other Crime", "Traffic Fatality", "Fire Accident"]

occ = pd.Timestamp("2020-01-01") + pd.to_timedelta(rng.integers(0, 365 * 4, n), unit="D")
rep = occ + pd.to_timedelta(rng.integers(0, 2, n), unit="D") + pd.to_timedelta(rng.integers(0, 24, n), unit="h")
closed_flag = rng.choice(["Yes", "No"], n)
closed_date = [(r + pd.Timedelta(days=int(d))).strftime("%d-%m-%Y %H:%M") if f == "Yes" else np.nan
               for r, d, f in zip(rep, rng.integers(5, 200, n), closed_flag)]
india = pd.DataFrame({
    "Report Number": np.arange(1, n + 1),
    "Date Reported": rep.strftime("%d-%m-%Y %H:%M"),
    "Date of Occurrence": occ.strftime("%m-%d-%Y %H:%M"),
    "Time of Occurrence": rep.strftime("%d-%m-%Y %H:%M"),
    "City": rng.choice(cities, n),
    "Crime Code": rng.integers(100, 600, n),
    "Crime Description": rng.choice(descs, n),
    "Victim Age": rng.integers(10, 80, n),
    "Victim Gender": rng.choice(["M", "F"], n),
    "Weapon Used": rng.choice(weapons, n),
    "Crime Domain": rng.choice(domains, n, p=[.2, .6, .1, .1]),
    "Police Deployed": rng.integers(1, 20, n),
    "Case Closed": closed_flag,
    "Date Case Closed": closed_date,
})
india.to_csv(HERE / "SAMPLE_crime_india_style.csv", index=False)

m = 50
yearly = pd.DataFrame({
    "Year": rng.integers(2000, 2021, m),
    "Population": rng.integers(1_000_000, 40_000_000, m),
    "Murder": np.round(rng.uniform(0.2, 9.8, m), 1),
    "Assault": rng.integers(50, 200, m),
    "Robbery": rng.integers(22, 100, m),
    "CarTheft": rng.integers(100, 900, m),
})
yearly.to_csv(HERE / "SAMPLE_crime_yearly.csv", index=False)
print("Wrote SAMPLE_crime_india_style.csv and SAMPLE_crime_yearly.csv (synthetic, seeded).")
