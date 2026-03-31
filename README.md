# F1-Strategy-Simulator

🏎️ F1 Strategy Simulator. This is a Python project that analyzes, models, and predicts tyre degradation based on real Formula 1 session data from FastF1.  

📌 Overview. This project uses real F1 race data to model how tyre performance fluctuates over a stint. This is going to be a core part of race strategy engineering and one of the key elements of the model and it’s understanding how tyre wear affects lap time. The ultimate objective is to build this into a complete race strategy simulator.  

📊 Real F1 session data is streamed and loaded with FastF1.  
🧾 User inputs are done by the following key for: driver. round. session type. year.  
🛞 Filters lap data by tyre compound:  
Soft. Medium. Hard.  
⏱ Turn lap times into seconds for analysis.  
📈 Fits with tyre degradation curve using SciPy.  
📉 Simulate tyre performance with Matplotlib.  
🌐 Streamlit interactive interface.  
💾 Exports results to CSV.  

🛠️ Tech Stack. Python. Streamlit. FastF1. NumPy. Pandas. Matplotlib. SciPy.  

📂 Project Structure.  
F1_strategy/  
├── app.py  
├── analysis.py  
├── data_loader.py  
├── Tyre_Degradation_Results.csv  
└── cache/  

app.py  
Manages Streamlit user interface.  
Collects user input.  
App Flow Control with st.session_state.  
Runs the analysis.  
Displays results.  

analysis.py  
Contains the tyre degradation modelling logic.  
Retrieves lap data.  
Separates laps by compound.  
Fits a curve to each compound.  
Generates a graph.  
Returns results.  

data_loader.py  
Takes care of FastF1 data loading and preprocessing.  
Loads sessions.  
Filters valid laps.  
Converts lap times to seconds.  

🧠 How the Model Works.  
Tyre deterioration is modelled with an exponential formula:  

scale * exp(deg_rate * x) + lap_time  

Where:  
x = tyre age (laps).  
deg_rate = degradation rate.  
lap_time = baseline lap time.  

For each compound:  
Load driver lap data.  
Filter valid laps.  
Extract tyre age and lap time.  
Use curve_fit to fit curve.  
Plot real data vs fitted curve.  

🚀 How to Run.  
# Clone the repository  
git clone https://github.com/YOUR-USERNAME/F1-Strategy-Simulator.git  

cd F1-Strategy-Simulator  

# Create virtual environment  
python3 -m venv venv  
source venv/bin/activate  

# Install dependencies  
pip install -r requirements.txt  

# Run the app  
python -m streamlit run app.py  

📊 Output. The app produces:  

Tyre degradation graphs.  
Estimated degradation rates.  
Results in a CSV file.  

⚠️ Current Limitations.  
No complete race simulation yet.  
No pit stop optimisation.  
No traffic or safety car modelling.  
Limited data filtering.  

🚀 Future Improvements.  
Full race strategy simulation.  
Compare 1-stop vs 2-stop approaches.  
Include fuel and traffic modelling.  
Enhance the robustness of curve fitting.  
Multi-driver comparison.  

💡 Motivation. It blends computer science, data analysis and Formula 1 in this project. The key to this is developing a realistic, data-driven understanding of the race strategy.  

📜 License. MIT License.  

👤 Author. Jack Page. Computer Science Student. Northumbria University
