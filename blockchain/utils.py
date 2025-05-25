from .abi import contract_abi  # store ABI in abi.py and import
import os
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

RPC_URL = os.getenv("SEPOLIA_RPC_URL")
PRIVATE_KEY = os.getenv("ADMIN_PRIVATE_KEY")
WALLET_ADDRESS = os.getenv("ADMIN_WALLET_ADDRESS")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")

# The ABI you posted earlier

web3 = Web3(Web3.HTTPProvider(RPC_URL))
contract = web3.eth.contract(
    address=Web3.to_checksum_address(CONTRACT_ADDRESS), abi=abi)


def vote_on_blockchain(election_id, candidate_ids):
    nonce = web3.eth.get_transaction_count(WALLET_ADDRESS)

    txn = contract.functions.vote(election_id, candidate_ids).build_transaction({
        'from': WALLET_ADDRESS,
        'nonce': nonce,
        'gas': 300000,
        'gasPrice': web3.to_wei('10', 'gwei')
    })

    signed_txn = web3.eth.account.sign_transaction(
        txn, private_key=PRIVATE_KEY)
    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    return web3.to_hex(tx_hash)
