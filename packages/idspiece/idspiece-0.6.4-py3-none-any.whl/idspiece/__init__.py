from .idstable import idstable

def tokenize(text):
  tokens=[]
  while text>"":
    c=text[0]
    if c in idstable:
      tokens.append(idstable[c][0:2])
      text=idstable[c][2]+text[1:]
    else:
      tokens.append(c)
      text=text[1:]
  return tokens

