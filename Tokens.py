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
    val = self.peek()
    self.index += 1
    return val

  def myTokens(self):
    return self.tokens

  # def pop(self):
  #   return self.tokens.pop(0)

  def peek_front_behind(self):
    return self.tokens[self.index + 1]