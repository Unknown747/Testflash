from actions.action import Action
from utils import utils

class ERC20:
  def __init__(self, web3, wallet, target_gwei):
    self.web3 = web3
    self.wallet = wallet
    self.target_gwei = target_gwei

  def transfer(self, contract_address, to, amount):
    contract = self.web3.eth.contract(address=contract_address, abi=utils.load_abi("abi/erc20.json"))
    function = contract.functions.transfer(to, amount)
    gas = 55000#function.estimate_gas({ "from": self.wallet.account.address })
    tx = function.build_transaction({
      "nonce": self.wallet.nonce,
      "from": self.wallet.account.address,
      "gas": gas,
      "gasPrice": self.web3.to_wei(self.target_gwei, "gwei")
    })
    signed = self.wallet.account.sign_transaction(tx)
    self.wallet.nonce += 1
    return Action(signer=self.wallet, signed=signed.rawTransaction, gas=gas, nonce=self.wallet.nonce - 1)