import streamlit as st
import pandas as pd
import altair as alt
from tft_prob import monte_carlo_shop_roll_odd_optimized

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
    # df, at_least_x_target_champion_odds = monte_carlo_shop_roll_odd_optimized(level, target_unit_cost, gold, target_unit_out_count, cost_unit_out_count)
    odds_dict = monte_carlo_shop_roll_odd_optimized(level, target_unit_cost, gold, target_unit_out_count, cost_unit_out_count)

    # Convert odds to a DataFrame for visualization
    #odds_df = pd.DataFrame(list(at_least_x_target_champion_odds.items()), columns=["Number of Champions", "Odds"])
    odds_df = pd.DataFrame(list(odds_dict.items()), columns=["Number of Champions", "Odds"])
    pctg_df = odds_df.copy()
    decimals = 2
    pctg_df["Odds"] = (pctg_df['Odds']*100).apply(lambda x: round(x, decimals)).astype("str") + "%"

    # Create a horizontal bar chart with Altair
    chart = (
        alt.Chart(odds_df)
        .mark_bar()
        .encode(
            y=alt.Y("Number of Champions:O", title="Number of Champions", sort="x"),
            x=alt.X("Odds:Q", title="Probability"),
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
    # Center and display the table with fixed width
    table_html = pctg_df.to_html(index=False)  # Convert DataFrame to HTML
    st.markdown(
        f"""
        <div style="display: flex; justify-content: center;">
            <div>
                {table_html}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
