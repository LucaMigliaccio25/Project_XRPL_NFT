from xrpl.core import keypairs
from xrpl.wallet import Wallet, generate_faucet_wallet
from xrpl.clients import JsonRpcClient
from xrpl.account import get_balance
from xrpl.models import Payment
from xrpl.transaction import sign, submit_and_wait, XRPLReliableSubmissionException
from xrpl.account import get_next_valid_seq_number
from xrpl.ledger import get_latest_validated_ledger_sequence
from xrpl.models.transactions import NFTokenMint, NFTokenCreateOffer
from xrpl.utils import str_to_hex, datetime_to_ripple_time
from datetime import datetime, timedelta

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
# TEST DELLA CREAZIONE DI UNA TRANSAZIONE DI PAGAMENTO TRA DUE WALLET
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

###################################################
# TEST DELLA CREAZIONE DI UN NFT 
###################################################

# Creazione di un wallet finanziato
minter_wallet = generate_faucet_wallet(client, debug=True)
print(f"Wallet address: {minter_wallet.classic_address}")
print(f"Wallet seed: {minter_wallet.seed}")

# Parametri dell'NFT
uri = "https://example.com/nft"  # URI dell'NFT
flags = 8  # Flag per rendere l'NFT trasferibile
transfer_fee = 0  # Nessuna tassa di trasferimento
taxon = 1  # Categoria dell'NFT

# Funzione per testare la creazione di un NFT
try:
    # Ottieni il numero di sequenza corrente per il wallet
    sequence = get_next_valid_seq_number(minter_wallet.classic_address, client)
    print(f"Sequence number for {minter_wallet.classic_address}: {sequence}")

    # Ottieni il ledger valido corrente
    current_validated_ledger = get_latest_validated_ledger_sequence(client)

    # Creazione della transazione NFTokenMint
    mint_tx = NFTokenMint(
        account=minter_wallet.classic_address,
        uri=str_to_hex(uri),
        flags=flags,
        transfer_fee=transfer_fee,
        nftoken_taxon=taxon,
        sequence=sequence,
        last_ledger_sequence=current_validated_ledger + 10,  # Valido per i prossimi 10 ledger
        fee="10",  # Tassa minima in drops
    )

    # Firma e invio della transazione
    print(f"Transaction to be submitted: {mint_tx}")
    signed_tx = sign(mint_tx, minter_wallet)
    response = submit_and_wait(signed_tx, client)
    print(f"Transaction response: {response}")

    # Verifica del risultato
    if response.result["meta"]["TransactionResult"] == "tesSUCCESS":
        print("NFT successfully minted!")
        
        # Estrai l'ID dell'NFT dal risultato
        nftoken_id = response.result["meta"]["AffectedNodes"][1]["CreatedNode"]["NewFields"]["NFTokens"][0]["NFToken"]["NFTokenID"]
        print(f"NFT Token ID: {nftoken_id}")
    else:
        print(f"Transaction failed: {response.result['meta']['TransactionResult']}")
except KeyError as e:
    print(f"Error extracting NFT Token ID: {e}")
    
except XRPLReliableSubmissionException as e:
    print(f"Transaction submission failed: {e}")

except Exception as e:
    print(f"An error occurred: {e}")

##########################################
# TEST PER LA FARE UN'OFFERTA DI VENDITA DELL'NFT
##########################################

# Creazione dell'offerta di vendita
try:
    current_time = datetime.now()
    expiration_time = datetime_to_ripple_time(current_time + timedelta(minutes=60))

    sell_offer_tx = NFTokenCreateOffer(
        account=minter_wallet.classic_address,
        nftoken_id=nftoken_id,  # ID dell'NFT creato
        amount="1000000",  # Prezzo dell'offerta in drops (1 XRP = 1,000,000 drops)
        expiration=expiration_time,  # Scadenza dell'offerta
        flags=1  # Flag per indicare che è un'offerta di vendita
    )

    # Firma e invio della transazione
    signed_sell_offer = sign(sell_offer_tx, minter_wallet)
    sell_offer_response = submit_and_wait(signed_sell_offer, client)
    print(f"Sell Offer Response: {sell_offer_response}")

    if sell_offer_response.result["meta"]["TransactionResult"] == "tesSUCCESS":
        print("Sell offer successfully created!")
        sell_offer_id = sell_offer_response.result["meta"]["offer_id"]
    else:
        print(f"Sell Offer Transaction Failed: {sell_offer_response.result['meta']['TransactionResult']}")

except XRPLReliableSubmissionException as e:
    print(f"Sell Offer Submission Failed: {e}")

except Exception as e:
    print(f"An error occurred during Sell Offer creation: {e}")