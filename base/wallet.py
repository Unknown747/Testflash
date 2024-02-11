from eth_account import Account
from actions.erc20 import ERC20
from actions.hytopia_migrated_claim import HytopiaMigratedClaim
from actions.hytopia_staking import HytopiaStaking
from actions.nfts import NFTs
from actions.native import Native
from actions.mass_transferrer import MassTransferrer
from actions.mass_transferrer_with_recipients import MassTransferrerWithRecipients

class Wallet:
  def __init__(self, web3, target_gwei, private_key):
    self.account = Account.from_key(private_key)
    self.erc20 = ERC20(web3=web3, wallet=self, target_gwei=target_gwei)
    self.nonce = web3.eth.get_transaction_count(self.account.address)
    self.nfts = NFTs(web3=web3, wallet=self, target_gwei=target_gwei)
    self.native = Native(web3=web3, wallet=self, target_gwei=target_gwei)
    self.hytopia_staking = HytopiaStaking(web3=web3, wallet=self, target_gwei=target_gwei)
    self.hytopia_migrated_claim = HytopiaMigratedClaim(web3=web3, wallet=self, target_gwei=target_gwei)
    self.mass_transferrer = MassTransferrer(web3=web3, wallet=self, target_gwei=target_gwei)
    self.mass_transferrer_with_recipients = MassTransferrerWithRecipients(web3=web3, wallet=self, target_gwei=target_gwei)
    pass