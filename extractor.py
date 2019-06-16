from google.cloud import bigquery
import pandas as pd
from tqdm import tqdm

client = bigquery.Client.from_service_account_json(
    "google-big-query-key.json"
)

sql = """
with balances_table as (
    with double_entry_book as (
        -- debits
        select to_address as address, value as value
        from `bigquery-public-data.ethereum_blockchain.traces`
        where to_address is not null
        and status = 1
        and (call_type not in ('delegatecall', 'callcode', 'staticcall') or call_type is null)
        union all
        -- credits
        select from_address as address, -value as value
        from `bigquery-public-data.ethereum_blockchain.traces`
        where from_address is not null
        and status = 1
        and (call_type not in ('delegatecall', 'callcode', 'staticcall') or call_type is null)
        union all
        -- transaction fees debits
        select miner as address, sum(cast(receipt_gas_used as numeric) * cast(gas_price as numeric)) as value
        from `bigquery-public-data.ethereum_blockchain.transactions` as transactions
        join `bigquery-public-data.ethereum_blockchain.blocks` as blocks on blocks.number = transactions.block_number
        group by blocks.miner
        union all
        -- transaction fees credits
        select from_address as address, -(cast(receipt_gas_used as numeric) * cast(gas_price as numeric)) as value
        from `bigquery-public-data.ethereum_blockchain.transactions`
    )
    select address, sum(value) as balance
    from double_entry_book
    group by address
)
select address, balance
from balances_table
where balance > 0
order by balance desc
"""

query = client.query(sql)
result = query.result()

balances = [dict(row) for row in tqdm(result, total=result.total_rows)]
balances_df = pd.DataFrame(balances)

sum_threshold = balances_df["balance"].sum() * 0.8
balances_sum = balances_df["balance"].cumsum()
balances_df = balances_df[balances_sum <= sum_threshold]

balances_df.to_csv("/tmp/balances.csv")
