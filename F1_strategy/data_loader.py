#loads a Formula 1 race
import fastf1
import pandas as pd
from pathlib import Path


#Makes data load faster after first run
#(cache lives next to this file and is created if missing, so it works locally and on Streamlit Cloud)
CACHE_DIR = Path(__file__).resolve().parent / "cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)
fastf1.Cache.enable_cache(str(CACHE_DIR))

#loads the race
def load_race(year, grand_prix, session):
    session = fastf1.get_session(year, grand_prix, session)
    session.load()
    return session

#loads the drivers laps
def get_driver_laps(session, driver):
    laps = session.laps.pick_drivers(driver).copy()

    #cleans the Lap times with no real recorded lap time
    laps = laps[laps["LapTime"].notna()].copy()

    #turns lap time into seconds
    laps["LapTimeSeconds"] = laps["LapTime"].dt.total_seconds()
    return laps