from actions.action import Action
from utils import utils

CONTRACT_ADDRESS = '0x570653fe84925cdC5662f6a05C9a0CC964ae7766'

class MassTransferrerWithRecipients:
  def __init__(self, web3, wallet, target_gwei):
    self.web3 = web3
    self.wallet = wallet
    self.target_gwei = target_gwei

  def setup(self, contract_address):
    contract = self.web3.eth.contract(address=contract_address, abi=utils.load_abi("abi/erc721.json"))
    function = contract.functions.setApprovalForAll(CONTRACT_ADDRESS, True)
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
  
  def execute(self, transfers):
    contract = self.web3.eth.contract(address=CONTRACT_ADDRESS, abi=utils.load_abi("abi/massTransferrerWithRecipients.json"))
    function = contract.functions.execute(transfers, self.wallet.account.address)
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