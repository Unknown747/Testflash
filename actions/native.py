from actions.action import Action
from web3.types import TxParams

class Native:
  def __init__(self, web3, wallet, target_gwei):
    self.web3 = web3
    self.wallet = wallet
    self.target_gwei = target_gwei

  def send_token(self, to, amount):
    tx: TxParams = {
      "gas": 21000,
      "chainId": 1,
      "nonce": self.wallet.nonce,
      "to": to,
      "value": amount,
      "gasPrice": self.web3.toWei(self.target_gwei, "gwei")
    }
    signed_tx = self.wallet.account.sign_transaction(tx)
    self.wallet.nonce += 1
    return Action(signer=self.wallet, signed=signed_tx.rawTransaction, gas=21000, nonce=self.wallet.nonce - 1)