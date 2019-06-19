import json
import pandas as pd


genesis_path = "../data/cosmos_genesis_snapshot.json"


def get_accounts():
    genesis_json = json.load(open(genesis_path))
    accounts = genesis_json["app_state"]["accounts"]
    accounts_prepared = [{
            "address": account["address"],
            "amount": int(account["coins"][0]["amount"])
        }
        for account in accounts
    ]
    return accounts_prepared


def create_genesis(accounts):
    genesis_df = pd.DataFrame(accounts).set_index("address")
    return genesis_df


def save_genesis(genesis_df):
    genesis_df.to_csv("../tmp/cosmos_genesis_snapshot.csv")


if (__name__ == "__main__"):
    accounts = get_accounts()
    genesis_df = create_genesis(accounts)
    save_genesis(genesis_df)