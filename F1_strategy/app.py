#UI for the F1 Strategy Simulator
import streamlit as st
from analysis import run_analysis
from data_loader import load_race
import matplotlib.pyplot as plt
from pathlib import Path

#create a title and subheader
st.title("Formula 1 Strategy Simulator")
st.subheader("Session settings: ")

if "stage" not in st.session_state:
    st.session_state.stage = 1
if st.session_state.stage == 1:
    st.subheader("Session settings: ")

    #splitting the page into 3 columns and add data inputs
    col1, col2, col3 = st.columns(3, gap="medium")

    driver = col1.text_input("Enter Driver Abbreviation")
    round = col2.text_input("Enter round")
    session = col3.selectbox("Enter Session", ["FP1", "FP2", "FP3", "Q", "R"])
    year = col2.slider("Enter year", 2018, 2025)

    if st.button("Continue"):
        st.session_state.stage = 2
        st.session_state.year = year
        st.session_state.round = int(round)
        st.session_state.driver = driver
        st.session_state.session = session


elif st.session_state.stage == 2:
    st.subheader("Race Settings:")

    col1, col2, col3 = st.columns(3, gap="medium")

    lap_num = col1.text_input("How many laps in a race")
    base_time = col2.text_input("Base lap time")
    pit_stop = col3.text_input("How much time lost in pit stop")
    warm_up_cost = col1.text_input("Enter time lost warming up tyres")
    fuel_effect = col2.text_input("Enter time lost(s)")


#if button is pressed then it loads the these data inputs
    if st.button("Tyre Settings"):
        st.session_state.stage = 3

elif st.session_state.stage == 3:
        st.subheader("tyre Settings:")

        col1, col2, col3 = st.columns(3, gap="medium")

        start_compound = col1.selectbox("Starting tyre compound", ["Soft", "Medium", "Large"])
        next_tyre = col2.selectbox("Next tyre compound", ["Soft", "Medium", "Large"])
        num_stops = col3.selectbox("1 stop or 2 stop", ["1 stop", "2 stops"])

        if st.button("Run Analysis"):
            st.session_state.stage = 4

elif st.session_state.stage == 4:
    session = load_race(st.session_state.year, 
                        st.session_state.round, 
                        st.session_state.session)
            
    graph, results = run_analysis(session, st.session_state.driver)

    st.pyplot(graph)

    outpath = Path("Tyre_Degradation_Results.csv")
    results.to_csv(outpath, index=False)
    st.dataframe(results)


             

    





