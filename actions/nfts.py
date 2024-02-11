from actions.action import Action
from utils import utils

class NFTs:
  def __init__(self, web3, wallet, target_gwei):
    self.web3 = web3
    self.wallet = wallet
    self.target_gwei = target_gwei

  def erc721_set_approval_for_all(self, contract_address, operator, approved):
    contract = self.web3.eth.contract(address=contract_address, abi=utils.load_abi("abi/erc721.json"))
    function = contract.functions.setApprovalForAll(operator, approved)
    gas = function.estimate_gas({ "from": self.wallet.account.address })
    tx = function.build_transaction({
      "nonce": self.wallet.nonce,
      "from": self.wallet.account.address,
      "gas": gas,
      "gasPrice": self.web3.to_wei(self.target_gwei, "gwei")
    })
    signed = self.wallet.account.sign_transaction(tx)
    self.wallet.nonce += 1
    return Action(signer=self.wallet, signed=signed.rawTransaction, gas=gas, nonce=self.wallet.nonce - 1)

  def erc721_send(self, contract_address, to, token_id):
    contract = self.web3.eth.contract(address=contract_address, abi=utils.load_abi("abi/erc721.json"))
    function = contract.functions.transferFrom(self.wallet.account.address, to, token_id)
    gas = function.estimate_gas({ "from": self.wallet.account.address })
    tx = function.build_transaction({
      "nonce": self.wallet.nonce,
      "from": self.wallet.account.address,
      "gas": gas,
      "gasPrice": self.web3.to_wei(self.target_gwei, "gwei")
    })
    signed = self.wallet.account.sign_transaction(tx)
    self.wallet.nonce += 1
    return Action(signer=self.wallet, signed=signed.rawTransaction, gas=gas, nonce=self.wallet.nonce - 1)