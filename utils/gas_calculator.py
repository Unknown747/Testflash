from typing import List
from actions.action import Action

def calculate(actions : List[Action]):
  total_gas = 0
  for action in actions:
    total_gas += action.gas
  return total_gas