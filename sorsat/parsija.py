from sisennys import *
from rivi import *

class Parsija:
  def __init__(self):
    self.luokat = []
    self.rivit = []
    self.luokkaNyt = -1
    self.julkisuus = True
    self.funktiossa = False
    self.sisennys = Sisennys()
    
  def laita_rivi(self, rivi):
    self.rivi = Rivi(rivi)
    
  def parsi_kommentti(self, alkupMerk, korvattavaMerk):
    if self.rivi.jonoton.strip()[0] == alkupMerk:
      self.rivit.append(re.sub(alkupMerk, korvattavaMerk, self.rivi.koko + '\n', 1))
      self.sisennys.riviNum += 1
      return True
    return False