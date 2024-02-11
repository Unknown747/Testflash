import argparse
from time import sleep
from flashbots import flashbot
from base.wallet import Wallet
from utils import gas_calculator
from web3 import HTTPProvider, Web3
from eth_account.account import Account
from web3.exceptions import TransactionNotFound
from eth_account.signers.local import LocalAccount

# Load arguments
parser = argparse.ArgumentParser()
parser.add_argument("--fire", type=bool, required=False, help="", default=False)
parser.add_argument("--rpc", type=str, required=False, help="Ethereum RPC to be used", default="https://eth.llamarpc.com")
parser.add_argument("--target_gwei", type=int, required=True, help="Target GWEI to execute the bundle in")
parser.add_argument("--compromised_key", type=str, required=True, help="Private key for the compromised wallet, without 0x prefix")
parser.add_argument("--funding_key", type=str, required=True, help="Private key for the wallet that will be paying gas fees, without 0x prefix")
parser.add_argument("--safe_address", type=str, required=True, help="Wallet that should receive all assets at the end of execution")
args = parser.parse_args()

# Web3 and Flashbots
web3 = Web3(HTTPProvider(args.rpc))
signer: LocalAccount = Account.create()
flashbot(web3, signer)

# Wallets
funding_wallet = Wallet(web3=web3, target_gwei=args.target_gwei, private_key=args.funding_key)
compromised_wallet = Wallet(web3=web3, target_gwei=args.target_gwei, private_key=args.compromised_key)

# Actions
action_list = [
  compromised_wallet.hytopia_staking.unstake([2764], args.safe_address),
  compromised_wallet.hytopia_staking.claim(args.safe_address)
]

print("Calculating total gas for actions...")
total_gas = gas_calculator.calculate(action_list)
print(f"Total gas for actions: {total_gas}")

# Create bundle with compromised wallet funding TX
bundle = [
  {"signed_transaction": funding_wallet.native.send_token(compromised_wallet.account.address, total_gas * web3.to_wei(args.target_gwei, "gwei")).signed}
]

# Insert all actions in the bundle
for action in action_list:
  bundle.append({"signed_transaction": action.signed})

lastAttempt = 0

# Attempt sending the bundle
while True:
  block = web3.eth.block_number
  if lastAttempt == block:
    sleep(5)
    continue

  lastAttempt = block
  print(f"Trying block {block}")

  # Simulate bundle on current block
  try:
    web3.flashbots.simulate(bundle, block)
  except Exception as e:
    print(f"Exception: {e}")
    sleep(5)
    continue

  if not args.fire:
    continue

  # Send bundle targeting next block
  print(f"Sending bundle targeting block {block+1}")
  send_result = web3.flashbots.send_bundle(
    bundle,
    target_block_number=block + 1
  )

  send_result.wait()

  try:
    receipts = send_result.receipts()
    print(f"\nBundle was mined in block {receipts[0].blockNumber}\a")
    break

  except TransactionNotFound:
    print(f"Bundle not found in block {block+1}")
    continue