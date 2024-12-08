import streamlit as st
import pandas as pd
import numpy as np
from tft_prob import monte_carlo_shop_roll_odd

# Streamlit UI
st.title("TFT Shop Roll Monte Carlo Simulation - By Clib")

# Input fields
level = st.slider("Level", 1, 10, 1)
target_unit_cost = st.slider("Target Unit Cost", 1, 5, 1)
target_unit_out_count = st.number_input("Target Unit Out Count", min_value=0, value=0, step=1)
cost_unit_out_count = st.number_input("Cost Unit Out Count", min_value=0, value=0, step=1)
gold = st.number_input("Gold", min_value=2, value=10, step=2)

# Run the simulation
if st.button("Run Simulation"):
    # Call the monte_carlo_shop_roll_odd function
    df = monte_carlo_shop_roll_odd(level, target_unit_cost, gold, target_unit_out_count, cost_unit_out_count)

    # Extracting the at_least_x_target_champion_odds
    iterations = 1000
    at_least_x_target_champion_odds = {
        1: df[df["target_unit_count"] >= 1].shape[0] / iterations,
        2: df[df["target_unit_count"] >= 2].shape[0] / iterations,
        3: df[df["target_unit_count"] >= 3].shape[0] / iterations,
        4: df[df["target_unit_count"] >= 4].shape[0] / iterations,
        5: df[df["target_unit_count"] >= 5].shape[0] / iterations,
        6: df[df["target_unit_count"] >= 6].shape[0] / iterations,
        7: df[df["target_unit_count"] >= 7].shape[0] / iterations,
        8: df[df["target_unit_count"] >= 8].shape[0] / iterations,
        9: df[df["target_unit_count"] >= 9].shape[0] / iterations,
    }

    # Convert odds to a DataFrame for visualization
    odds_df = pd.DataFrame(list(at_least_x_target_champion_odds.items()), columns=["Number of Champions", "Odds"])

    # Display bar chart
    st.bar_chart(odds_df.set_index("Number of Champions"))

    # Display raw data
    st.dataframe(odds_df)