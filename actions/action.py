class Action:
  def __init__(self, signer, signed, gas, nonce):
    self.signer = signer
    self.signed = signed
    self.gas = gas
    self.nonce = nonce