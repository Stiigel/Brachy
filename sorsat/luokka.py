import re

class Luokka:
  def __init__(self, nimi, alku):
    self.nimi = nimi
    self.alku = alku  
    self.rivit = []
    self.usamet = []
    
  def lisaa_usame(self, rivi):
    if 'usame' in rivi:
      self.usamet.append(''.join(rivi.split()[1:]))
      return ''
    return rivi
   #u,:,;,b,<C-n>,<C-p>,h,j,k,l,o,t,T,O,g,f,r,R,d,/