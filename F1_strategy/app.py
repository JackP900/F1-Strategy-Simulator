# UI for the F1 Strategy Simulator
import streamlit as st
from analysis import run_analysis
from data_loader import load_race
import matplotlib.pyplot as plt
from pathlib import Path
from strategy import strategy, good_strategies

st.set_page_config(page_title="F1 Strategy Simulator", layout="wide")

st.title("Formula 1 Strategy Simulator")

if "stage" not in st.session_state:
    st.session_state.stage = 1

stages = ["Session", "Race Settings", "Tyre Settings", "Results"]
cols = st.columns(len(stages))

for i, (col, label) in enumerate(zip(cols, stages), start=1):
    if i < st.session_state.stage:
        col.success(f"✅ {label}")
    elif i == st.session_state.stage:
        col.info(f"→ {label}")
    else:
        col.write(f"⭕️ {label}")

st.divider()


if st.session_state.stage == 1:
    st.subheader("Session settings")
    st.caption("Choose F1 Session you want to load data from")

    col1, col2, col3 = st.columns(3, gap="medium")

    driver = col1.text_input("Enter Driver Abbreviation", placeholder="e.g. HAM")
    round_num = col2.text_input("Round Number", placeholder="e.g. 7")
    session_type = col3.selectbox("Enter Session", ["FP1", "FP2", "FP3", "Q", "R"])
    year = col2.slider("Enter year", 2018, 2025, value=2023)

    if st.button("Continue", type="primary"):
        if not driver or not round_num:
            st.error("Please fill in before continuing")
        else:
            st.session_state.stage = 2
            st.session_state.year = year
            st.session_state.round = int(round_num)
            st.session_state.driver = driver.upper()
            st.session_state.session = session_type
            st.rerun()

elif st.session_state.stage == 2:
    st.subheader("Race Settings")
    st.caption("Define the Race settings.")

    col1, col2, col3 = st.columns(3, gap="medium")

    lap_num = col1.text_input("Total Laps", placeholder="e.g. 57")
    pit_stop = col2.text_input("Pit stop time loss (s)", placeholder="e.g. 22.0")
    warm_up_cost = col3.text_input("Tyre warm up cost (s)", placeholder="e.g. 0.5")
    fuel_effect = col2.text_input("Fuel time saving per lap (s)", placeholder="e.g. 0.08")

    col_back, col_next = st.columns([1, 5])
    with col_back:
        if st.button("Back"):
            st.session_state.stage = 1
            st.rerun()
    with col_next:
        if st.button("Continue", type="primary"):
            if not lap_num or not pit_stop or not warm_up_cost or not fuel_effect:
                st.error("Please fill in all fields.")
            else:
                st.session_state.stage = 3
                st.session_state.lap_num = int(lap_num)
                st.session_state.pit_stop = float(pit_stop)
                st.session_state.warm_up_cost = float(warm_up_cost)
                st.session_state.fuel_effect = float(fuel_effect)
                st.rerun()

elif st.session_state.stage == 3:
    st.subheader("Tyre Settings")
    st.caption("Choose the strategy you want to simulate")

    col1, col2, col3 = st.columns(3, gap="medium")

    start_compound = col1.selectbox("Starting compound", ["Soft", "Medium", "Hard"])
    next_tyre = col2.selectbox("Next compound", ["Soft", "Medium", "Hard"])
    num_stops = col3.selectbox("Strategy type", ["1 stop", "2 stops"])

    col_back, col_next = st.columns([1, 5])
    with col_back:
        if st.button("Back"):
            st.session_state.stage = 2
            st.rerun()
    with col_next:
        if st.button("Run Analysis", type="primary"):
            st.session_state.stage = 4
            st.session_state.start_compound = start_compound.upper()
            st.session_state.next_tyre = next_tyre.upper()
            st.session_state.num_stops = num_stops
            st.rerun()

elif st.session_state.stage == 4:

    with st.spinner("Loading session data and fitting tyre model..."):
        session = load_race(
            st.session_state.year,
            st.session_state.round,
            st.session_state.session
        )

        graph, results, tyre_models = run_analysis(session, st.session_state.driver)

    if st.session_state.num_stops == "1 stop":
        user_compounds = [st.session_state.start_compound, st.session_state.next_tyre]
        user_pit_laps = [st.session_state.lap_num // 2]
    else:
        user_compounds = [
            st.session_state.start_compound,
            st.session_state.next_tyre,
            st.session_state.next_tyre
        ]

        user_pit_laps = [
            st.session_state.lap_num // 3,
            (2 * st.session_state.lap_num) // 3
        ]

    strategy_df, user_total_time, pit_laps = strategy(
        total_laps=st.session_state.lap_num,
        pit_stop_loss=st.session_state.pit_stop,
        compounds=user_compounds,
        pit_laps=user_pit_laps,
        tyre_models=tyre_models,
        warm_up_cost=st.session_state.warm_up_cost,
        fuel_effect=st.session_state.fuel_effect
    )

    with st.spinner("Searching all strategies..."):
        summary_df, strategy_results = good_strategies(
            total_laps=st.session_state.lap_num,
            pit_stop_loss=st.session_state.pit_stop,
            tyre_models=tyre_models,
            warm_up_cost=st.session_state.warm_up_cost,
            fuel_effect=st.session_state.fuel_effect
            )

    best_strategy = summary_df.iloc[0]
    best_total_time = best_strategy["TotalTime"]
    time_delta = user_total_time - best_total_time

    st.subheader(
        f"Results - {st.session_state.driver} ."
        f"Round {st.session_state.round} . "
        f"{st.session_state.year}"
    )

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total laps", st.session_state.lap_num)
    m2.metric("Your strategy time", f"{user_total_time:.1f} s")
    m3.metric("Best strategy time", f"{best_total_time:.1f} s")
    m4.metric(
        "Time lost vs Best",
        f"+{time_delta:.1f} s" if time_delta >= 0 else f"{time_delta:.1f} s",
        delta=f"{-time_delta:.1f} s gap" if time_delta > 0 else "You matched the best!",
        delta_color="inverse"
    )

    st.divider()

    tab1, tab2, tab3 = st.tabs(["Tyre Analysis", "Your Strategy", "Best Strategys"])

    with tab1:
        st.caption("Degradation curves fitted to real FastF1 session data.")
        st.pyplot(graph)

        st.markdown("Fitted model coefficients")
        compound_cols = st.columns(len(results))
        compound_colors = {"SOFT": "🔴", "MEDIUM": "🟡", "HARD": "⚪️"}

        for col, (_, row) in zip(compound_cols, results.iterrows()):
            comp = row["Compound"]
            icon = compound_colors.get(comp, "⚫️")
            col.metric(f"{icon} {comp}", "")
            col.write(f"**a** = {row['a']:.4f}")
            col.write(f"**b** = {row['b']:.4f}")
            col.write(f"**c** = {row['c']:.2f}")

        with st.expander("view full results table"):
            st.dataframe(results, use_container_width=True)
            outpath = Path("Tyre_Degradation_Results.csv")
            results.to_csv(outpath, index=False)
            st.caption(f"Saved to {outpath}")

    with tab2:
        stop_label = st.session_state.num_stops
        compounds_label = " → ".join(user_compounds)
        pits_label = ", ".join([f"Lap {p}" for p in pit_laps])
        st.caption(f"{stop_label} · {compounds_label} · Pit at {pits_label}")

        s1, s2, s3 = st.columns(3)
        s1.metric("Pit lap(s)", pits_label)
        s2.metric("Compounds", compounds_label)
        s3.metric("Total time", f"{user_total_time:.1f} s")

        fig, ax = plt.subplots()
        ax.plot(strategy_df["Lap"], strategy_df["LapTime"], color="#e10600")
        for pl in pit_laps:
            ax.axvline(x=pl, color="gray", linestyle="--", linewidth=0.8, label=f"pit lap {pl}")

        ax.set_title("Your Strategy — Simulated Lap Times")
        ax.set_xlabel("Lap")
        ax.set_ylabel("Lap Time (s)")
        ax.invert_yaxis()
        ax.grid(True, alpha=0.3)
        ax.legend()
        st.pyplot(fig)

        with st.expander("View lap by lap data."):
            st.dataframe(strategy_df, use_container_width=True)

    with tab3:
        st.caption("All strategies ranked by total race time.")

        st.markdown("Fastest Strategy")
        b1, b2, b3 = st.columns(3)
        b1.metric("Strategy", best_strategy["Strategy"].split(" lap")[0])
        b2.metric("Pit lap(s)", str(best_strategy["PitLap"]))
        b3.metric("Total time", f"{best_total_time:.1f} s")

        best_name = best_strategy["Strategy"]
        best_df = strategy_results[best_name]

        fig2, ax2 = plt.subplots()
        ax2.plot(best_df["Lap"], best_df["LapTime"], color="#00a550")
        for pl in best_strategy["PitLap"]:
            ax2.axvline(x=pl, color="gray", linestyle="--", linewidth=0.8)
        ax2.set_title(f"Best Strategy — {best_name}")
        ax2.set_xlabel("Lap")
        ax2.set_ylabel("Lap Time(s)")
        ax2.invert_yaxis()
        ax2.grid(True, alpha=0.3)
        st.pyplot(fig2)

        st.markdown("All strategies")
        st.caption("Sorted fastest to slowest.")
 
        top_n = min(10, len(summary_df))
        for i in range(top_n):
            row = summary_df.iloc[i]
            delta_vs_best = row["TotalTime"] - best_total_time
            with st.container(border=True):
                c1, c2, c3, c4 = st.columns([3, 2, 2, 2])
                c1.markdown(f"{i+1} {row['Strategy']}")
                c2.metric("Compounds", row["Compounds"])
                c3.metric("Pit lap(s)", str(row["PitLap"]))
                c4.metric(
                    "Total time",
                    f"{row['TotalTime']:.1f} s",
                    delta=f"+{delta_vs_best:.1f} s" if delta_vs_best > 0 else "Best",
                    delta_color="inverse"
                )

        if len(summary_df) > top_n:
            with st.expander(f"Show all {len(summary_df)} strategies"):
                st.dataframe(summary_df, use_container_width=True)

    st.divider()
    if st.button("Start Over"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
    





