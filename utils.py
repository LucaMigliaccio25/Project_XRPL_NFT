from xrpl.account import get_balance, get_next_valid_seq_number
from xrpl.clients import JsonRpcClient
from xrpl.wallet import Wallet, generate_faucet_wallet
from xrpl.core import keypairs
from xrpl.transaction import sign, submit_and_wait, XRPLReliableSubmissionException
from xrpl.models import Payment
from xrpl.models.transactions import NFTokenMint, NFTokenCreateOffer, NFTokenAcceptOffer
from xrpl.utils import str_to_hex, datetime_to_ripple_time
from xrpl.ledger import get_latest_validated_ledger_sequence
from datetime import datetime, timedelta

client = JsonRpcClient("https://s.altnet.rippletest.net:51234")

def _generate_xrpl_wallet_seed() -> str:
    """
    Generate a random seed. Notice that if you create a wallet with this seed, it won't be a working wallet, because you need to fund it before. See https://xrpl.org/docs/concepts/accounts#creating-accounts.
    """
    return keypairs.generate_seed()

def get_wallet(seed: str | None = None) -> Wallet:
    """
    Generate a wallet.
    """
    if seed:
        wallet = Wallet.from_seed(seed)
    else:
        wallet = generate_faucet_wallet(client, debug=True)
    return wallet

def print_balances(wallets: list, client: JsonRpcClient) -> None:
    """
    Print the balances of wallets.
    """
    print("Balances:")
    for wallet in wallets:
        print(f"{wallet.address}: {get_balance(wallet.address, client)}")

def mint_nft_token(seed, uri, flags, transfer_fee, taxon):
    minter_wallet=Wallet.from_seed(seed)
    mint_tx=NFTokenMint(
        account=minter_wallet.address,
        uri=str_to_hex(uri),
        flags=int(flags),
        transfer_fee=int(transfer_fee),
        nftoken_taxon=int(taxon)
    )
    response=""
    try:
        response=submit_and_wait(mint_tx,client,minter_wallet)
        response=response.result
    except XRPLReliableSubmissionException as e:
        response=f"Submit failed: {e}"
    return response

def create_sell_offer(seed, amount, nftoken_id, expiration, destination):
    owner_wallet = Wallet.from_seed(seed)
    expiration_date = datetime.now()
    if expiration != '':
        expiration_date = datetime_to_ripple_time(expiration_date)
        expiration_date = expiration_date + int(expiration)
    sell_offer_tx=NFTokenCreateOffer(
        account=owner_wallet.address,
        nftoken_id=nftoken_id,
        amount=amount,
        destination=destination if destination != '' else None,
        expiration=expiration_date if expiration != '' else None,
        flags=1
    )
    response=""
    try:
        response=submit_and_wait(sell_offer_tx,client,owner_wallet)
        response=response.result
    except XRPLReliableSubmissionException as e:
        response=f"Submit failed: {e}"
    return response

def accept_sell_offer(seed, offer_index):
    buyer_wallet=Wallet.from_seed(seed)
    accept_offer_tx=NFTokenAcceptOffer(
       account=buyer_wallet.classic_address,
       nftoken_sell_offer=offer_index
    )
    try:
        response=submit_and_wait(accept_offer_tx,client,buyer_wallet)
        response=response.result
    except XRPLReliableSubmissionException as e:
        response=f"Submit failed: {e}"
    return response