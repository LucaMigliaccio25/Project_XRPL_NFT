from xrpl.core import keypairs

# Test di generazione di un seed
seed = keypairs.generate_seed()
print(f"Generated seed: {seed}")