from actions.action import Action
from utils import utils

CONTRACT_ADDRESS = '0x2F53e033C55eB6C87CEa259123C0a68Ca3578426'

class HytopiaStaking:
  def __init__(self, web3, wallet, target_gwei):
    self.web3 = web3
    self.wallet = wallet
    self.target_gwei = target_gwei

  def claim(self, target):
    contract = self.web3.eth.contract(address=CONTRACT_ADDRESS, abi=utils.load_abi("abi/hytopiaStaking.json"))
    function = contract.functions.claim(target)
    gas = function.estimate_gas({ "from": self.wallet.account.address })
    tx = function.build_transaction({
      "nonce": self.wallet.nonce,
      "from": self.wallet.account.address,
      "gas": gas,
      "gasPrice": self.web3.toWei(self.target_gwei, "gwei")
    })
    signed = self.wallet.account.sign_transaction(tx)
    self.wallet.nonce += 1
    return Action(signer=self.wallet, signed=signed.rawTransaction, gas=gas, nonce=self.wallet.nonce - 1)

  def unstake(self, tokenIDs, target):
    contract = self.web3.eth.contract(address=CONTRACT_ADDRESS, abi=utils.load_abi("abi/hytopiaStaking.json"))
    function = contract.functions.unstake(tokenIDs, target)
    gas = function.estimate_gas({ "from": self.wallet.account.address })
    tx = function.build_transaction({
      "nonce": self.wallet.nonce,
      "from": self.wallet.account.address,
      "gas": gas,
      "gasPrice": self.web3.toWei(self.target_gwei, "gwei")
    })
    signed = self.wallet.account.sign_transaction(tx)
    self.wallet.nonce += 1
    return Action(signer=self.wallet, signed=signed.rawTransaction, gas=gas, nonce=self.wallet.nonce - 1)