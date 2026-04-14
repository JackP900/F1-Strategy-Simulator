🏎️ F1 Strategy Simulator
Ever wondered how F1 teams come up with the perfect race strategy? This app gives you a chance to try it yourself! Built with Python and Streamlit, it uses real race data (thanks to FastF1) to model tyre wear and fuel effects, then runs hundreds of simulated strategies to find which one’s fastest.

📸 What’s Inside?
You'll go through a simple 4-step wizard to create and explore race strategies:

Session Settings — pick your driver, year, race, and session type
Race Settings — set key factors like pit stop time loss, fuel impact, and tyre warm-up costs
Tyre Settings — choose your starting tyre and how many pit stops to make
Results — check out the tyre wear analysis, see how your strategy would perform lap by lap, and compare all the top strategies side by side
🚀 Let’s Get Started
What you need
Python 3.9 or newer
(Optional but recommended) a virtual environment to keep things neat
How to install
bash

Copy code
# First, clone this repository
git clone https://github.com/your-username/F1-Strategy-Simulator.git
cd F1-Strategy-Simulator

# Create and activate your virtual environment
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate

# Install everything we need
pip install -r requirements.txt
Run the app 🚦
bash

cd F1_strategy
streamlit run app.py
📦 What’s Under the Hood?
Package	What it does

streamlit	Creates the interactive web interface

fastf1	Downloads real F1 timing and telemetry data

pandas	Handles all the data wrangling

numpy	Powers numerical calculations

scipy	Fits the tyre degradation curves

matplotlib	Draws charts and graphs
You can install them all at once by running:

bash

pip install streamlit fastf1 pandas numpy scipy matplotlib
🗂️ How the Project is Organized

'''
F1-Strategy-Simulator/
│
├── F1_strategy/
│   ├── app.py            # The Streamlit interface and wizard flow
│   ├── analysis.py       # Figures out how tyres degrade over time
│   ├── strategy.py       # Runs race simulations and hunts best strategies
│   ├── data_loader.py    # Loads session and lap data from FastF1
│   └── cache/            # Automatically stores FastF1 data locally
│
└── README.md
🔬 The Science Behind It
Modelling Tyre Wear
We analyze real lap times from the data and fit them to a quadratic equation:
'''

lap_time = a × (tyre_age)² + b × tyre_age + c

c is your baseline lap time on fresh tyres

b shows how lap times get slower linearly as tyres age

a captures how degradation speeds up (tyres get more ‘tired’ the longer they run)
We do this fitting separately for Soft, Medium, and Hard tyres based on the data you load.

Simulating the Race
Each lap’s time considers:

The effect of fuel burning off, so the car gets lighter and faster as the race goes on
The fact that fresh tyres need a ‘warm-up’ lap where they’re not quite at peak grip
Pit stops cost time and reset tyre age, which the simulator accounts for.

Finding the Best Strategy
The app tries out every reasonable one- or two-stop strategy — mixing tyre compounds and varying pit stop laps — then ranks them by total predicted race time. You can easily see which strategies come out on top.

📊 What You’ll See in the Results
The results page has three tabs:

Tyre Analysis — shows how your lap times and degradation curves line up, plus the maths behind the fit coefficients
Your Strategy — a lap-by-lap graph of your personal strategy, highlighting pit stops
Best Strategies — an at-a-glance leaderboard of the fastest strategies, with full details available if you want to dive deeper
⚠️ Things to Keep in Mind
The fuel effect is linked to tyre age rather than the total laps run, which simplifies things a bit
Tyre degradation is modelled as a nice clean quadratic curve, but actual tyre wear is way more complex and influenced by lots of stuff like weather and driving style
No modeling of safety cars, weather changes, or other race interruptions — this is a pure strategy sim
To get a good fit, you need at least 5 laps on each tyre compound — otherwise it skips the fitting for that tyre

🙏 Thanks to…
FastF1 — for giving us easy access to official F1 data
Streamlit — for making it super simple to build cool interactive apps in Python

If you want to chat about strategy or have questions, just ask! Enjoy racing smarter. 🏁

Would you like me to help with anything else—like adding example screenshots or improving some code comments?
