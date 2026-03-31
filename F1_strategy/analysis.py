#estimating tyre Degradation using FastF1 library
import fastf1
import numpy as np
from pathlib import Path
from scipy.optimize import curve_fit
from data_loader import load_race, get_driver_laps
import matplotlib.pyplot as plt
import pandas as pd

session = load_race(2019, 8, "R")
driver = "VER"

def tyre_deg(x, scale, deg_rate, lap_time):
    #calculation for tyre life
    return scale * np.exp(deg_rate * x) + lap_time

#stores data of tyres
results = []
compounds = ["SOFT", "MEDIUM", "HARD"]
for comp in compounds:
    laps = get_driver_laps(session, driver)
    laps = laps[laps["Compound"] == comp]

    x = laps["TyreLife"].astype(float).to_numpy()
    y = laps["LapTimeSeconds"].to_numpy()


    try:
        if len(x) == 0 or len(y) == 0:
            print(f"Skipping {comp}: no usable data")
            continue
        param, cov = curve_fit(tyre_deg, x, y, p0=(1, 0.01, np.min(y)))

        scale, deg_rate, lap_time = param
        results.append({
            "Compound": comp,
            "a": scale,
            "b": deg_rate,
            "c": lap_time,
            "Degradation_rate": deg_rate,
            "Lap_Time": lap_time
        })
    
        xfit = np.linspace(0, x.max(), 30)
        plt.scatter(x, y, label=f"{comp} data")
        plt.plot(xfit, tyre_deg(xfit, *param), label=f"{comp} fit", linestyle="--")

    except RuntimeError:
        print(f"could not fir {comp}")
        continue

    plt.title("{driver} Tyre Degradation: {round} {year}")
    plt.xlabel("Tyre Age (laps)")
    plt.ylabel("Lap Time (s)")
    plt.gca().invert_yaxis()
    plt.legend()
    plt.show()

    df_results = pd.DataFrame(results)
    outpath = Path("Tyre_Degradation_Results.csv")
    df_results.to_csv(outpath, index=False)
    print(df_results)




