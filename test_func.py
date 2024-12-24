from xrpl.core import keypairs
from xrpl.wallet import Wallet

# Test di generazione di un seed
seed = keypairs.generate_seed()
print(f"Generated seed: {seed}")

# Test per creare un wallet da un seed
wallet = Wallet.from_seed(seed)
print(f"Wallet address: {wallet.address}")