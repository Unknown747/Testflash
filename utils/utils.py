def load_abi(path: str):
  file = open(path, mode='r')
  abi = file.read()
  file.close()
  return abi