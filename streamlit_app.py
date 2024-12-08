import streamlit as st
import pandas as pd
import altair as alt
from tft_prob import monte_carlo_shop_roll_odd

# Streamlit UI
st.title("TFT Shop Roll Monte Carlo Simulation - By Clib")

# Input fields
level = st.slider("Level", 1, 10, 1)
target_unit_cost = st.slider("Target Unit Cost", 1, 5, 1)
target_unit_out_count = st.number_input("Number of copies of the desired Unit already out of the pool:", min_value=0, value=0, step=1)
cost_unit_out_count = st.number_input("Number of units of the same cost already out of the pool:", min_value=0, value=0, step=1)
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

    # Create a bar chart with Altair
    chart = (
        alt.Chart(odds_df)
        .mark_bar()
        .encode(
            x=alt.X("Number of Champions:O", title="Number of Champions"),
            y=alt.Y("Odds:Q", title="Probability"),
            tooltip=["Number of Champions", "Odds"]
        )
        .properties(
            title="Chances to Roll at Least X of Your Desired Champion",
            width=600,
            height=400
        )
    )

    # Display the chart
    st.altair_chart(chart, use_container_width=True)

    # Display raw data
    st.dataframe(odds_df)
