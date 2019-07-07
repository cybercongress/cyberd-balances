import pandas as pd
import json
from config import *


def load_config():
    distribution_json = json.load(open(DISTRIBUTION_PATH))
    manual_json = json.load(open(MANUAL_DISTRIBUTION_PATH))
    genesis_json = json.load(open(GENESIS_EXAMPLE_PATH))
    return distribution_json, manual_json, genesis_json


def get_emission(genesis_json):
    return float(genesis_json["app_state"]["staking"]["pool"]["not_bonded_tokens"])


def preprocess_balances(balances_df, emission, part_percentage, start_number):
    balances_df["cyb_balance"] = emission * part_percentage * balances_df["percentage"]
    balances_df["number"] = range(0, balances_df.shape[0])
    balances_df["number"] += start_number + 1


def load_json(emission, manual_json, part_percentage, start_number):
    balances_df = pd.DataFrame([{
        "address": key,
        "percentage": float(value) / 100
    } for key, value in manual_json.items()])
    preprocess_balances(balances_df, emission, part_percentage, start_number)    
    return balances_df


def load_csv(emission, path, part_percentage, start_number):
    balances_df = pd.read_csv(path)
    balances_df["percentage"] = balances_df["balance"] / balances_df["balance"].sum()
    preprocess_balances(balances_df, emission, part_percentage, start_number)    
    return balances_df


def get_start_number(all_balances):
    if all_balances:
        return all_balances[-1]["number"].max()
    else:
        return 0

def get_distributions(emission, distribution_json, manual_json):
    all_balances = []

    for distribution_type in distribution_json.keys():
        if distribution_type not in CSV_DISTRIBUTIONS:
            part_percentage = float(distribution_json[distribution_type]) / 100
            start_number = get_start_number(all_balances)
            balances_df = load_json(emission, manual_json[distribution_type], part_percentage, start_number)
            all_balances.append(balances_df)

    for distribution_type in CSV_DISTRIBUTIONS:
        part_percentage = float(distribution_json[distribution_type]) / 100
        start_number = get_start_number(all_balances)
        balances_df = load_csv(emission, CSV_DISTRIBUTIONS[distribution_type], part_percentage, start_number)
        all_balances.append(balances_df)

    return all_balances


def concatenate_balances(all_balances):
    balances_df = pd.concat(all_balances, sort=False).groupby("address").agg({
        "cyb_balance": "sum",
        "number": "min"
    })
    balances_df["cyb_balance"] = balances_df["cyb_balance"].astype(int)
    return balances_df


def save_json(emission, genesis_json, balances):
    assert (emission - balances["cyb_balance"].sum()) <= 1000

    genesis_json["app_state"]["accounts"] = [{
        "addr": address,
        "amt": str(row["cyb_balance"]),
        "nmb": str(row["number"])
    } for address, row in balances.sort_values("number").iterrows()]

    json.dump(
        genesis_json,
        open(GENERATED_GENESIS_PATH, "w")
    )


def generate():
    distribution_json, manual_json, genesis_json = load_config()
    emission = get_emission(genesis_json)
    all_balances = get_distributions(emission, distribution_json, manual_json)
    cyb_balances_df = concatenate_balances(all_balances)
    save_json(emission, genesis_json, cyb_balances_df)


if (__name__ == "__main__"):
    generate()
