"""
Shared helpers for the Big Data Analytics experiments.

* paths            - BASE_DIR / DATA_DIR / OUT_DIR  (all relative to this folder)
* load_crime()     - finds crime.csv (your real file) and says loudly if it has to use a synthetic SAMPLE instead
* get_mongo_db()   - connects to a REAL MongoDB server; never fakes one (see LAB_USE_MONGOMOCK below)
* finish()         - exit code handling that works in both Jupyter and a normal Python run
"""
import os
import sys
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "datasets"
OUT_DIR = BASE_DIR / "outputs"
OUT_DIR.mkdir(exist_ok=True)

USING_MOCK = os.environ.get("LAB_USE_MONGOMOCK") == "1"

try:
    IN_NOTEBOOK = get_ipython().__class__.__name__ == "ZMQInteractiveShell"
except NameError:
    IN_NOTEBOOK = False


def finish(code=0):
    """Exit with a status code when run as a script; do nothing inside Jupyter."""
    if not IN_NOTEBOOK and code:
        sys.exit(code)


def load_crime(required_columns=(), candidates=("crime.csv",), sample="SAMPLE_crime_india_style.csv"):
    """
    Return (DataFrame, path).

    Looks for your real dataset first (datasets/<candidate>), and only uses the synthetic SAMPLE file shipped
    with this project when no suitable real file exists.  Using the SAMPLE prints a banner, because its numbers
    are random and will not match the lab manual's printed output.
    """
    problems = []
    for name in candidates:
        path = DATA_DIR / name
        if not path.exists():
            continue
        df = pd.read_csv(path)
        missing = [c for c in required_columns if c not in df.columns]
        if not missing:
            return df, path
        problems.append(f"{name} has no column(s) {missing}")

    sample_path = DATA_DIR / sample
    banner = "=" * 78
    print(banner)
    print("NOTICE: your real crime dataset was not found / does not have the needed columns.")
    for p in problems:
        print("        -", p)
    print(f"        Using the SYNTHETIC SAMPLE  datasets/{sample}  (random data, made by")
    print("        datasets/make_sample_crime.py).  Results will NOT match the manual's printed output.")
    print("        To use the real data put it at datasets/crime.csv (see README, 'Datasets').")
    print(banner)
    if not sample_path.exists():
        raise FileNotFoundError(f"{sample_path} missing - run: python datasets/make_sample_crime.py")
    return pd.read_csv(sample_path), sample_path


MONGO_START_HELP = """
MongoDB is NOT reachable at {uri}.   This experiment needs a running MongoDB server.

  Windows : start the "MongoDB Server" service  (services.msc)  or run   mongod --dbpath C:\\data\\db
  Linux   : sudo systemctl start mongod
  macOS   : brew services start mongodb-community
  Docker  : docker run -d --name mongo -p 27017:27017 mongo:7

Then run the experiment again.  (Set MONGODB_URI to use a different server.)
"""


def get_mongo_db(db_name):
    """
    Connect to MongoDB and return the database object, or None (after printing instructions) if no server is running.

    Testing only: with the environment variable LAB_USE_MONGOMOCK=1 the in-memory *mongomock* library is used instead
    of a server, and a banner says so.  It is meant for checking the Python logic on a machine without MongoDB;
    nothing is stored anywhere.  Do not use it for your real practical.
    """
    if os.environ.get("LAB_USE_MONGOMOCK") == "1":
        import mongomock
        print("#" * 78)
        print("# TEST BACKEND: using mongomock (in-memory emulation) - NOT a real MongoDB server")
        print("#" * 78)
        client = mongomock.MongoClient()
        return client[db_name]

    import pymongo
    from pymongo.errors import PyMongoError
    uri = os.environ.get("MONGODB_URI", "mongodb://localhost:27017")
    try:
        client = pymongo.MongoClient(uri, serverSelectionTimeoutMS=3000)
        client.admin.command("ping")
    except PyMongoError:
        print(MONGO_START_HELP.format(uri=uri))
        return None
    print(f"Connected to MongoDB at {uri} (server version {client.server_info()['version']})")
    return client[db_name]
