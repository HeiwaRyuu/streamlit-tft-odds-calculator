from numpy import random
import pandas as pd

unit_costs = [1, 2, 3, 4, 5]

shop_cost_roll_odds = {
    1:[1, 0, 0, 0, 0],
    2:[1, 0, 0, 0, 0],
    3:[0.75, 0.25, 0, 0, 0],
    4:[0.55, 0.30, 0.15, 0, 0],
    5:[0.45, 0.33, 0.20, 0.02, 0],
    6:[0.25, 0.40, 0.30, 0.05, 0],
    7:[0.20, 0.33, 0.36, 0.10, 0.01],
    8:[0.18, 0.25, 0.32, 0.22, 0.03],
    9:[0.15, 0.20, 0.25, 0.30, 0.10],
    10:[0.05, 0.10, 0.20, 0.40, 0.25],
}

unit_count = {
    1:14,
    2:13,
    3:13,
    4:12,
    5:8
}

unit_pool_size = {
    1:30,
    2:25,
    3:18,
    4:10,
    5:9,
}

def generate_single_shop_cost(level):
    odds = shop_cost_roll_odds[level]
    return random.choice(unit_costs, p=odds, size=(1))[0]

def generate_single_unit_roll(cost, target_unit_out_count, cost_unit_out_count):
    # Fetching the count of units from the given cost
    count = unit_count[cost]
    # Fetching the pool size for each unit from that cost
    pool_size = unit_pool_size[cost]

    # Fixing target unit as the first (does not matter which unit, the calculations will remain the same)
    target_unit = 1
    # Calculating the target unit pool size by removing the target units that are already out from the unit pool
    target_unit_pool_size = pool_size - target_unit_out_count
    # Calculating the total pool size for that cost
    total_pool_size = (pool_size * count) - cost_unit_out_count

    # Generating a list with all possible units from that cost
    units_list = [i for i in range(1, count+1)]
    target_unit_weight = [target_unit_pool_size/total_pool_size]
    # Creating a list of weights, where all the other weights are equal (given that this will not affect the rolls for this specific unit)
    remaining_units_weight = (1-target_unit_weight[0])/(count-1)
    units_weight = target_unit_weight + [remaining_units_weight for _ in range(target_unit+1, count+1)]

    # print(f"count: {count} | pool_size: {pool_size} | target_unit_pool_size: {target_unit_pool_size} | total_pool_size: {total_pool_size}")
    # print(f"units_list: {units_list}")
    # print(f"target_unit_weight: {target_unit_weight}")
    # print(f"units_weight: {units_weight}")

    return random.choice(units_list, p=units_weight, size=(1))[0]

def roll_shop(level, cost, gold, target_unit_out_count, cost_unit_out_count):
    shop_cost_rolls = {1:0, 2:0, 3:0, 4:0, 5:0}
    target_unit = 1
    target_unit_count = 0

    total_rolls = int(gold/2)

    for i in range(0, total_rolls):
        # This is the counter for the target unit in the same 5 shop roll
        # (if it rolls once, the next four shops in game have -1 of that unit to roll from tyhe pool)
        local_target_unit_out_count = 0
        for i in range(0,5):
            generated_cost = generate_single_shop_cost(level)
            # We only generate the unit if we have generated a slot with the cost of that unit
            generated_unit = -1 # Set it to -1 so we can have a failed comparison if the cost above was not equal to the desired unit cost
            if generated_cost == cost:
                generated_unit = generate_single_unit_roll(cost, target_unit_out_count+local_target_unit_out_count, cost_unit_out_count+local_target_unit_out_count)
            
            # Incrementing the counters
            shop_cost_rolls[generated_cost] += 1
            if generated_unit == target_unit:
                local_target_unit_out_count += 1
                target_unit_count += 1

    shop_cost_rolls["target_unit_count"] = target_unit_count
    data_dict = shop_cost_rolls.copy()
    df = pd.DataFrame(data_dict, index=[0])

    return df


def monte_carlo_shop_roll_odd(level, cost, gold, target_unit_out_count, cost_unit_out_count):
    results = []
    iterations = 1000
    for i in range(iterations):
        results.append(roll_shop(level, cost, gold, target_unit_out_count, cost_unit_out_count))
    
    df = pd.concat(results).reset_index(drop=True)
    total_shop_rolls = (gold/2) * 5 * iterations

    cost_odds = {
        1:df[1].sum()/total_shop_rolls,
        2:df[2].sum()/total_shop_rolls,
        3:df[3].sum()/total_shop_rolls,
        4:df[4].sum()/total_shop_rolls,
        5:df[5].sum()/total_shop_rolls,
    }

    at_least_x_target_champion_odds = {
        1:df[df["target_unit_count"]>=1].shape[0]/iterations,
        2:df[df["target_unit_count"]>=2].shape[0]/iterations,
        3:df[df["target_unit_count"]>=3].shape[0]/iterations,
        4:df[df["target_unit_count"]>=4].shape[0]/iterations,
        5:df[df["target_unit_count"]>=5].shape[0]/iterations,
        6:df[df["target_unit_count"]>=6].shape[0]/iterations,
        7:df[df["target_unit_count"]>=7].shape[0]/iterations,
        8:df[df["target_unit_count"]>=8].shape[0]/iterations,
        9:df[df["target_unit_count"]>=9].shape[0]/iterations
    }

    print(f"Cost Odds:\n{cost_odds}")
    print(f"At Least X Target Champion Odds:\n{at_least_x_target_champion_odds}")

    return df


def main():
    level = int(input("Enter your Level: "))
    cost = int(input("Enter unit Cost: "))
    target_unit_out_count = int(input("How many of your desired unit are out?: "))
    cost_unit_out_count = int(input("How many units of that COST are out (in total, including your desired units): "))
    gold = int(input("How much gold would you like to roll: "))

    df = monte_carlo_shop_roll_odd(level, cost, gold, target_unit_out_count, cost_unit_out_count)
    df.to_excel(f"monte_carlo_tft-level-{level}-cost-{cost}-tuco-{target_unit_out_count}-cuoc-{cost_unit_out_count}-gold-{gold}.xlsx")


if __name__ == "__main__":
    main()