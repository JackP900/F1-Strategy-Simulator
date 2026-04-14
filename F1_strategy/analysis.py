#estimating tyre Degradation using FastF1 library
def run_analysis(session, driver):
    import fastf1
    import numpy as np
    from scipy.optimize import curve_fit
    from data_loader import load_race, get_driver_laps
    import matplotlib.pyplot as plt
    import pandas as pd

    def tyre_deg(x, scale, deg_rate, lap_time):
        #useing a quadratic equation becasue tire deg isn't linear
        return scale * x**2 + deg_rate * x + lap_time
    #stores data of tyres
    results = []
    #a list of all available dry compounds
    compounds = ["SOFT", "MEDIUM", "HARD"]

    #variables that stores the graph and the axes
    graph, ax = plt.subplots()

    #call function from data loader to get driver laps
    all_laps = get_driver_laps(session, driver)

    for comp in compounds:
        #splits the laps up according to their tyres
        laps = all_laps[all_laps["Compound"] == comp]

        #declaring x variable and converting it to a datatype curve_fit can work with
        x = laps["TyreLife"].astype(float).to_numpy()
        #declaring the y varaible and adding it to an array
        y = laps["LapTimeSeconds"].to_numpy()


        try:
            #making sure i get a minimum of 5 laps so i have enough data
            if len(x) < 5:
                print(f"Skipping {comp}: not enough data")
                continue

            #finds the optimum values of a, b, c for the curve
            param, cov = curve_fit(tyre_deg, x, y, p0=(0.001, 0.05, float(np.min(y))))

            #unpacking the param variable
            scale, deg_rate, lap_time = param

            #adding the variables into my results array
            results.append({
                "Compound": comp,
                "a": scale,
                "b": deg_rate,
                "c": lap_time,
                "Degradation_rate": deg_rate,
                "Lap_Time": lap_time
            })
        
            #this plots 30 evenly spaced points perfect for a smooth curve
            xfit = np.linspace(0, x.max(), 30)
            ax.scatter(x, y, label=f"{comp} data")
            #this produces the curve for the graph to look smooth
            ax.plot(xfit, tyre_deg(xfit, *param), linestyle="--", label=f"{comp} fit")

        #outputs in terminal if an error occured
        except RuntimeError as e:
            print(f"Could not fit {comp}: {e}")
            continue

    #setup everything for the graph
    ax.set_title("Tyre Degradation Plot")
    ax.set_xlabel("Tyre Age(laps)")
    ax.set_ylabel("Lap Time (s)")
    #inverted the y axis to make it easier to read the graph
    ax.invert_yaxis()
    ax.legend()
    ax.grid(True)

    tyre_models = {}

    #takes the results array and reconstructs it into a dictionary
    for row in results:
        tyre_models[row["Compound"]] = {
            "a": row["a"],
            "b": row["b"],
            "c": row["c"]
        }

    #creates a table for all the results
    df_results = pd.DataFrame(results)

    return graph, df_results, tyre_models




