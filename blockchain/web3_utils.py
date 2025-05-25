import os
import json
from dotenv import load_dotenv
from web3 import Web3

# your abi.py should define this as `contract_abi = [...]`
from blockchain.abi import contract_abi

# Load environment variables
load_dotenv(override=True)

# Setup Web3 connection
GANACHE_RPC_URL = os.getenv("GANACHE_RPC_URL")
ADMIN_PRIVATE_KEY = os.getenv("ADMIN_PRIVATE_KEY")
ADMIN_WALLET_ADDRESS = os.getenv("ADMIN_WALLET_ADDRESS")
ADMIN_WALLET_ADDRESS = Web3.to_checksum_address(ADMIN_WALLET_ADDRESS)
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")

w3 = Web3(Web3.HTTPProvider(GANACHE_RPC_URL))
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=contract_abi)





def send_vote_transaction(election_id, candidate_ids):
    """
    Sends a vote transaction using the admin wallet.
    """
    print("Loaded ENV:")


    print("GANACHE_RPC_URL:", GANACHE_RPC_URL)
    print("ADMIN_WALLET_ADDRESS:", ADMIN_WALLET_ADDRESS)
    print("CONTRACT_ADDRESS:", CONTRACT_ADDRESS)

    print(f"Connected to contract at {CONTRACT_ADDRESS}")
    print(f"Is connected: {w3.is_connected()}")
    print(f"Contract functions: {contract.all_functions()}")
    balance = w3.eth.get_balance(ADMIN_WALLET_ADDRESS)
    print(f"Wallet balance: {w3.from_wei(balance, 'ether')} ETH")

    if not w3.is_connected():
        raise Exception("Web3 provider is not connected.")


    # --- Debugging: simulate the transaction first ---
    try:
        contract.functions.storeVote(election_id, candidate_ids).call({
        'from': ADMIN_WALLET_ADDRESS})


    except Exception as e:
        print("Simulated call error:", e)
        raise


    nonce = w3.eth.get_transaction_count(ADMIN_WALLET_ADDRESS)

    tx = contract.functions.storeVote(election_id, candidate_ids).build_transaction({
        'from': ADMIN_WALLET_ADDRESS,
        'nonce': nonce,
        'gas': 300000,
        'gasPrice': w3.to_wei('2', 'gwei')
        
    })

    signed_tx = w3.eth.account.sign_transaction(
        tx, private_key=ADMIN_PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)  # capital T

    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print("Transaction succeeded", receipt)

    if receipt.status != 1:
        raise Exception("Transaction failed on chain")

    return receipt


def get_all_votes():
    votes_count = contract.functions.getVotesCount().call()
    all_votes = []
    for i in range(votes_count):
        vote = contract.functions.getVote(i).call()
        all_votes.append(vote)  # (electionId, candidateIds)
    return all_votes
