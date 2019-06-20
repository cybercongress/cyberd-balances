import pandas as pd
import json
from config import *


def load_config():
    distribution_json = json.load(open(DISTRIBUTION_PATH))
    manual_json = json.load(open(MANUAL_DISTRIBUTION_PATH))
    genesis_json = json.load(open(GENESIS_EXAMPLE_PATH))
    return distribution_json, manual_json, genesis_json


def load_json(manual_json, part_percentage):
    balances_df = pd.DataFrame([{
        "address": key,
        "percentage": int(value) / 100
    } for key, value in manual_json.items()])    
    balances_df["cyb_balance"] = CYB_EMISSION * part_percentage * balances_df["percentage"]
    return balances_df


def load_csv(path, part_percentage):
    balances_df = pd.read_csv(path)
    balances_df["percentage"] = balances_df["balance"] / balances_df["balance"].sum()
    balances_df["cyb_balance"] = CYB_EMISSION * part_percentage * balances_df["percentage"]
    return balances_df


def get_distributions(distribution_json, manual_json):
    all_balances = []

    for distribution_type in CSV_DISTRIBUTIONS:
        part_percentage = int(distribution_json[distribution_type]) / 100
        balances_df = load_csv(CSV_DISTRIBUTIONS[distribution_type], part_percentage)
        all_balances.append(balances_df)

    for distribution_type in distribution_json.keys():
        if distribution_type not in CSV_DISTRIBUTIONS:
            part_percentage = int(distribution_json[distribution_type]) / 100
            balances_df = load_json(manual_json[distribution_type], part_percentage)
            all_balances.append(balances_df)

    return all_balances


def concatenate_balances(all_balances):
    return pd.concat(all_balances, sort=False).groupby("address")["cyb_balance"].sum().astype(int)


def save_json(genesis_json, balances):
    # TODO Estimate allowed error
    # TODO Remove 110% from genesis config
    # assert abs(balances.sum() - CYB_EMISSION) <= 10 

    genesis_json["app_state"]["accounts"] = [{
        "addr": address,
        "amt": str(balance)
    } for address, balance in balances.iteritems()]

    json.dump(
        genesis_json,
        open(GENERATED_GENESIS_PATH, "w")
    )


def generate():
    distribution_json, manual_json, genesis_json = load_config()
    all_balances = get_distributions(distribution_json, manual_json)
    cyb_balances_df = concatenate_balances(all_balances)
    save_json(genesis_json, cyb_balances_df)


if (__name__ == "__main__"):
    generate()