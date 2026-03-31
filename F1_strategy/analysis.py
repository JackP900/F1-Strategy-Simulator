#estimating tyre Degradation using FastF1 library
def run_analysis(session, driver):
    import fastf1
    import numpy as np
    from scipy.optimize import curve_fit
    from data_loader import load_race, get_driver_laps
    import matplotlib.pyplot as plt
    import pandas as pd

    def tyre_deg(x, scale, deg_rate, lap_time):
        #calculation for tyre life
        return scale * np.exp(deg_rate * x) + lap_time

    #stores data of tyres
    results = []
    compounds = ["SOFT", "MEDIUM", "HARD"]

    graph, ax = plt.subplots()

    for comp in compounds:
        laps = get_driver_laps(session, driver)
        laps = laps[laps["Compound"] == comp]

        x = laps["TyreLife"].astype(float).to_numpy()
        y = laps["LapTimeSeconds"].to_numpy()


        try:
            if len(x) < 5:
                print(f"Skipping {comp}: not enough data")
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
            ax.scatter(x, y, label=f"{comp} data")
            ax.plot(xfit, tyre_deg(xfit, *param), linestyle="--", label=f"{comp} fit")

        except RuntimeError as e:
            print(f"Could not fit {comp}: {e}")
            continue

        ax.set_title("Tyre Degradation Plot")
        ax.set_xlabel("Tyre Age(laps)")
        ax.set_ylabel("Lap Time (s)")
        ax.invert_yaxis()
        ax.legend()
        ax.grid=True

        df_results = pd.DataFrame(results)

        return graph, df_results




