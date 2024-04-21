from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware
import json

# Initialize Web3 connection
w3 = Web3(HTTPProvider('https://rpc.apothem.network'))  # Use Apothem Testnet if testing
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

# Load the contract's ABI
with open('abi.json', 'r') as abi_file:
    contract_abi = json.load(abi_file)
contract_address = '0xF3642CaBb1cbf5fb88af1762c93351d8cb6C5E5E'
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

def store_email_hash_on_chain(uid, email_body):
    try:
        uid = str(uid)  # Ensure UID is a string as expected by the ABI
        private_key = '1913b305c73fdd97e6565d6a2c8a0baf51030d52c29a4f847b94b79a1eca32dc'
        account = w3.eth.account.from_key(private_key)
        email_hash = w3.keccak(text=email_body)
        sender_address = account.address
        print(sender_address)

        # Retrieve account balance
        balance = w3.eth.get_balance(sender_address)
        print(f"Account balance: {w3.from_wei(balance, 'ether')} XDC")

        # Gas estimation
        gas_price = w3.eth.gas_price
        gas_limit = 300000  # You can adjust this value based on the complexity of the contract function
        total_cost = gas_price * gas_limit

        print(f"Estimated gas cost (in wei): {total_cost} (Gas price: {gas_price}, Gas limit: {gas_limit})")

        if balance < total_cost:
            return f"Error: Insufficient funds for the transaction. Required: {w3.from_wei(total_cost, 'ether')} XDC, Available: {w3.from_wei(balance, 'ether')} XDC"

        # Transaction count (nonce) for the sender's address
        nonce = w3.eth.get_transaction_count(sender_address)

        # Build the transaction
        tx = contract.functions.storeHash(uid, email_hash).build_transaction({
            'chainId': 51,  # Chain ID for XinFin MainNet, use 51 for Apothem Testnet if necessary
            'gas': gas_limit,
            'gasPrice': gas_price,
            'nonce': nonce,
        })

        # Sign the transaction with the sender's private key
        signed_tx = account.sign_transaction(tx)

        # Send the transaction
        tx_receipt = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        return f"Transaction hash: {tx_receipt.hex()}"
    except Exception as e:
        return f"Error: {str(e)}"

# Example function call
print(store_email_hash_on_chain(1, "Hello, this is a test email."))

