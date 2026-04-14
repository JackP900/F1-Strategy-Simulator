# calculates the fastest strategy to use
import pandas as pd

#sets values for tyre models that are not in the lap data
default_tyre_models = {
    "SOFT": {"a": 0.0020, "b": 0.05, "c": 91.0},
    "MEDIUM": {"a": 0.0015, "b": 0.04, "c": 91.8},
    "HARD": {"a": 0.0010, "b": 0.03, "c": 92.6}
}

def lap_time(tyre_age, a, b, c, fuel_effect, warm_up_cost):
    #quadratic equation on how long lap time is based on tyre wear
    current_lap_time = a * tyre_age**2 + b * tyre_age + c
    #subtracts fuel burned multiplied by the tyre age
    current_lap_time -= fuel_effect * tyre_age

    #if the tyre is brand new they need heating up for optimal grip
    if tyre_age == 0:
        current_lap_time += warm_up_cost

    return current_lap_time


def strategy(
    total_laps,
    pit_stop_loss,
    compounds,
    pit_laps,
    tyre_models,
    warm_up_cost,
    fuel_effect
):
    
    #results array to store data
    results = []

    #declaring all the varaibles
    total_time = 0.0
    index = 0
    current_compound = compounds[index]
    tyre_age = 0

    #loops through every lap 
    for lap in range(1, total_laps + 1):
        #checks if the compound used is in the tyre model i created
        if current_compound in tyre_models:
            #if it is model = to that tyre model
            model = tyre_models[current_compound]
        else:
            #if it's not it get's the value from the default tyre model
            model = default_tyre_models[current_compound]

        #unpacking the tyre models into a, b and c
        a = model["a"]
        b = model["b"]
        c = model["c"]

        #calling the lap_time function
        current_lap_time = lap_time(
            tyre_age=tyre_age,
            a=a,
            b=b,
            c=c,
            fuel_effect=fuel_effect,
            warm_up_cost=warm_up_cost
        )

        #adds the laps time from the function to the one in this function
        total_time += current_lap_time
        used_compound = current_compound
        pitted = False

        #checks if car has pitted
        if lap in pit_laps:
            #adds the time loss for the pit stop
            total_time += pit_stop_loss
            index += 1
            if index < len(compounds):
                current_compound = compounds[index]
            #resets tyre age backt to zero
            tyre_age = 0
            #confirming that the pit happened
            pitted = True
        else:
            #if not on pit lap the tyre ages by 1
            tyre_age += 1

        #appending the results into the array
        results.append({
            "Lap": lap,
            "Compound": used_compound,
            "TyreAge": tyre_age,
            "LapTime": current_lap_time,
            "TotalTime": total_time,
            "Pitted": pitted
        })

    #displays the results on a table
    df = pd.DataFrame(results)

    return df, total_time, pit_laps


def generate_strategies(total_laps):
    #creating an array to store the strategies 
    strategies = []

    #some combinations for a 1 stop pit
    one_stop = [
        ["SOFT", "MEDIUM"],
        ["SOFT", "HARD"],
        ["MEDIUM", "HARD"]
    ]

    #some combinations for a 2 stop pit
    two_stop = [
        ["SOFT", "MEDIUM", "HARD"],
        ["SOFT", "HARD", "MEDIUM"],
        ["MEDIUM", "SOFT", "HARD"]
    ]

    #filters through my tyre combinations
    for comp in one_stop:
        #goes through all the appropriate laps
        for pit_lap in range(10, total_laps - 10, 4):
            #through every lap it appends this to strategies
            strategies.append({
                #creates the name of the pit stop
                "name": f"one-stop {'-'.join(comp)} lap {pit_lap}",
                #compounds used
                "compounds": comp,
                #a list with a single pit lap number in it
                "pit_laps": [pit_lap]
            })

    #filters through the combinations in the two stop
    for comp in two_stop:
        #filters through the appropriate laps for the first stop
        for pit1 in range(8, total_laps - 20, 6):
            #filters through the appropriate laps for a second stop
            for pit2 in range(pit1 + 10, total_laps - 5, 6):
                #appends this to the strategies
                strategies.append({
                    #creates the name for it
                    "name": f"two-stop {'-'.join(comp)} lap {pit1}, {pit2}",
                    #a list of compounds used
                    "compounds": comp,
                    #a list of the pit1 lap number and pit2 lap number
                    "pit_laps": [pit1, pit2]
                })

    return strategies


def good_strategies(total_laps, pit_stop_loss, tyre_models, warm_up_cost, fuel_effect):
    #calls all the stratgies including one stop and two stop
    candidates = generate_strategies(total_laps)
    #will store the headline numbers
    summary = []
    #will store all the lap by lap information
    results = {}

    #simulates every strategy 
    for candidate in candidates:
        strategy_df, total_time, pit_laps = strategy(
            total_laps=total_laps,
            pit_stop_loss=pit_stop_loss,
            compounds=candidate["compounds"],
            pit_laps=candidate["pit_laps"],
            tyre_models=tyre_models,
            warm_up_cost=warm_up_cost,
            fuel_effect=fuel_effect
        )

        #stores all the results from the strategies 
        summary.append({
            "Strategy": candidate["name"],
            "Compounds": "-".join(candidate["compounds"]),
            "PitLap": candidate["pit_laps"],
            "TotalTime": total_time
        })

        results[candidate["name"]] = strategy_df

    #puts all the strategies in dataframe and sorts it by total time so the fastest is at the top
    summary_df = pd.DataFrame(summary).sort_values("TotalTime").reset_index(drop=True)
    return summary_df, results