class Tokens:
  
  tokens = None
  index = 0

  def __init__(self):
    self.tokens = [] 
    self.index = 0

  def append(self, token):
    self.tokens.append(token)

  def peek(self):
    return self.tokens[self.index]
  
  def advance(self):
    node = self.tokens[self.index]
    self.index = self.index + 1
    return node