import random


def dungeonmobrandom():
  a = random.randrange(1,100)
  if a >= 40: 
    return 1
  elif 20 <= a < 40: 
    return 2
  elif 10 <= a < 20: 
    return 3
  elif 1 <= a < 10: 
    return 4
  