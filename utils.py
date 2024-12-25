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

