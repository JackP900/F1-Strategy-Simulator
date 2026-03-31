#loads a Formula 1 race
import fastf1
import pandas as pd


#Makes data load faster after first run
fastf1.Cache.enable_cache("F1_startegy/cache")

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