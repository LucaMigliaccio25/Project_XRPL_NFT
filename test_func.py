from xrpl.core import keypairs
from xrpl.wallet import Wallet, generate_faucet_wallet
from xrpl.clients import JsonRpcClient
from xrpl.account import get_balance
from xrpl.clients import JsonRpcClient

# Test di generazione di un seed
seed = keypairs.generate_seed()
print(f"Generated seed: {seed}")

# Test per creare un wallet da un seed
wallet = Wallet.from_seed(seed)
print(f"Wallet address: {wallet.address}")

# Test della connessione al client XRPL
client = JsonRpcClient("https://s.altnet.rippletest.net:51234")
print(f"Client connected to: {client.url}")

# Generazione di un wallet finanziato
wallet = generate_faucet_wallet(client, debug=True)
print(f"Wallet address: {wallet.address}")
print(f"Wallet seed: {wallet.seed}")