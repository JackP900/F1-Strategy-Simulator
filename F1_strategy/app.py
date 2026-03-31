#UI for the F1 Strategy Simulator
import streamlit as st
from analysis import run_analysis
from data_loader import load_race
import matplotlib.pyplot as plt
from pathlib import Path

#create a title and subheader
st.title("Formula 1 Strategy Simulator")
st.subheader("Race settings: ")

#splitting the page into 3 columns and add data inputs
col1, col2, col3 = st.columns(3, gap="medium")

driver = col1.text_input("Enter Driver Abbreviation")
round = col2.text_input("Enter round")
session = col3.selectbox("Enter Session", ["FP1", "FP2", "FP3", "Q", "R"])


year = col1.slider("Enter year", 2018, 2025)
lap_num = col2.text_input("How many laps in a race")
base_time = col3.text_input("Base lap time")
pit_stop = col1.text_input("How much time lost in pit stop")
warm_up_cost = col2.text_input("Enter time lost warming up tyres")
fuel_effect = col3.text_input("Enter time lost(s)")

race_button = st.button("Run Analysis")
#if button is pressed then it loads the these data inputs
if race_button:
    st.subheader("tyre Variables:")
    session = load_race(year, int(round), session)
    graph, results = run_analysis(session, driver)

    st.pyplot(graph)

    outpath = Path("Tyre_Degradation_Results.csv")
    results.to_csv(outpath, index=False)
    st.dataframe(results)

    col1, col2, col3 = st.columns(3, gap="medium")

    start_compound = col1.selectbox("Starting tyre compound", ["Soft", "Medium", "Large"])
    next_tyre = col2.selectbox("Next tyre compound", ["Soft", "Medium", "Large"])
    num_stops = col3.selectbox("1 stop or 2 stop", ["1 stop", "2 stops"])




