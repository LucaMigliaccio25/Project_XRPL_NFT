from xrpl.core import keypairs
from xrpl.wallet import Wallet, generate_faucet_wallet
from xrpl.clients import JsonRpcClient
from xrpl.account import get_balance
from xrpl.models import Payment
from xrpl.transaction import sign, submit_and_wait
from xrpl.account import get_next_valid_seq_number
from xrpl.ledger import get_latest_validated_ledger_sequence

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

# Test della funzione get_balance
address = wallet.address
balance = get_balance(address, client)
print(f"Balance for {address}: {balance}")

#######################################################
# TEST DELLA CREAZIONE DI UNA TRANSAZIONE DI PAGAMENTO TRA DUE WALLET #
#######################################################

# Funzione per stampare i bilanci
def print_balances(wallets, client):
    for wallet in wallets:
        balance = get_balance(wallet.classic_address, client)
        print(f"Balance for {wallet.classic_address}: {balance} drops")

# Creazione di due wallet finanziati
sender_wallet = generate_faucet_wallet(client, debug=True)
receiver_wallet = generate_faucet_wallet(client, debug=True)

# Stampa dei bilanci iniziali
print("Initial Balances:")
print_balances([sender_wallet, receiver_wallet], client)

# Creazione della transazione di pagamento
current_validated_ledger = get_latest_validated_ledger_sequence(client)
payment_tx = Payment(
    account=sender_wallet.classic_address,
    amount="1000",  # 1000 drops di XRP (1 XRP = 1,000,000 drops)
    destination=receiver_wallet.classic_address,
    sequence=get_next_valid_seq_number(sender_wallet.classic_address, client),
    last_ledger_sequence=current_validated_ledger + 10,  # Valido per i prossimi 10 ledger
    fee="10",  # Fee minima in drops (tassa che dev'essere pagata da chi effettua la transazione)
)

# Firma e invio della transazione
signed_tx = sign(payment_tx, sender_wallet)
response = submit_and_wait(signed_tx, client)

# Output
# print(f"Payment transaction response: {response}")

# Stampa dei bilanci finali
print("\nFinal Balances:")
print_balances([sender_wallet, receiver_wallet], client)