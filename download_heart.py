"""
Download the UCI *Cleveland* Heart Disease data and write datasets/heart.csv in the layout the
manual's Experiment 7 expects (14 columns, header row, '?' kept for missing ca/thal, target 0-4).

Source: https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.cleveland.data

Run once (needs internet):   python download_heart.py
Experiment_07.py calls this automatically if datasets/heart.csv is missing.
"""
import csv
import urllib.request
from pathlib import Path

URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.cleveland.data"
COLUMNS = ["age", "sex", "cp", "trestbps", "chol", "fbs", "restecg", "thalach",
           "exang", "oldpeak", "slope", "ca", "thal", "heartdisease"]
FLOAT_COLS = {"oldpeak"}

try:
    BASE_DIR = Path(__file__).resolve().parent
except NameError:
    BASE_DIR = Path.cwd()
TARGET = BASE_DIR / "datasets" / "heart.csv"


def _fmt(col, value):
    value = value.strip()
    if value == "?":
        return "?"
    number = float(value)
    if col in FLOAT_COLS:
        return repr(number)
    return str(int(number))


def download_heart_csv(target=TARGET):
    target.parent.mkdir(exist_ok=True)
    print("Downloading", URL)
    raw = urllib.request.urlopen(URL, timeout=60).read().decode("utf-8")
    rows = [r for r in csv.reader(raw.splitlines()) if r]
    if len(rows) != 303 or any(len(r) != 14 for r in rows):
        raise RuntimeError(f"Unexpected file layout ({len(rows)} rows) - not the Cleveland file?")
    with open(target, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(COLUMNS)
        for r in rows:
            writer.writerow([_fmt(c, v) for c, v in zip(COLUMNS, r)])
    print("Wrote", target, "(303 rows)")


if __name__ == "__main__":
    download_heart_csv()
