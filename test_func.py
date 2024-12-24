from xrpl.core import keypairs
from xrpl.wallet import Wallet
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