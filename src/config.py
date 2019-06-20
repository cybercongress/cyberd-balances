# For cosmos snapshot
COSMOS_GENESIS_PATH = "./data/cosmos_genesis_snapshot.json"
COSMOS_GENESIS_PATH_CSV = "./data/cosmos_genesis_snapshot.csv"

# For ethereum snapshot
DEFAULT_ETHEREUM_BLOCK = 10000000
GOOGLE_KEY_PATH = "google-big-query-key.json"
ETHEREUM_GENESIS_PATH_CSV = "./data/ethereum_genesis_snapshot.csv"

# For genesis generator
CYB_EMISSION = 1000000000000000.0
CSV_DISTRIBUTIONS = {
    "ethereum_drop": ETHEREUM_GENESIS_PATH_CSV,
    "cosmos_drop": COSMOS_GENESIS_PATH_CSV
}
DISTRIBUTION_PATH = "./data/cyber_distribution.json"
MANUAL_DISTRIBUTION_PATH = "./data/manual_distribution.json"
GENESIS_EXAMPLE_PATH = "./data/network_genesis.json"
GENERATED_GENESIS_PATH = "./data/genesis.json"