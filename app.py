#UI for the F1 Strategy Simulator
import streamlit as st

st.title("Formula 1 Strategy Simulator")
st.subheader("Race settings: ")

col1, col2, col3 = st.columns(3, gap="medium")

lap_num = col1.text_input("How many laps in a race")
base_time = col2.text_input("Base lap time")
pit_stop = col3.text_input("How much time lost in pit stop")
warm_up_cost = col1.text_input("Enter time lost warming up tyres")
fuel_effect = col2.text_input("Enter time lost(s)")

race_button = st.button("Continoue to tyre settings")

if race_button:
    st.subheader("tyre Variables:")

    col1, col2, col3 = st.columns(3, gap="medium")

    start_compound = col1.selectbox("Starting tyre compound", ["Soft", "Medium", "Large"])
    next_tyre = col2.selectbox("Next tyre compound", ["Soft", "Medium", "Large"])
    num_stops = col3.selectbox("1 stop or 2 stop", ["1 stop", "2 stops"])



