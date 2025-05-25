import os
import json

# Construct the path to the ABI JSON file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ABI_FILE = os.path.join(BASE_DIR, 'blockchain', 'contract_abi.json')

# Load the ABI
with open(ABI_FILE) as f:
    contract_abi = json.load(f)
