from sisennys import *
from rivi import *

class Parsija:
  def __init__(self):
    self.luokat = []
    self.rivit = []
    self.luokkaNyt = -1
    self.julkisuus = 2
    self.funktiossa = False
    self.sisennys = Sisennys()
    
    keno = chr(92)
    self.sAlut = '(^|[' + keno + keno.join('s+*/-=[]{}()<>,') + '])'
    self.sLoput = '([' + keno + keno.join('s+*/-=[]{}()<>.,:') + ']|$)'
    
  def laita_rivi(self, rivi):
    self.rivi = Rivi(rivi)
    
  def parsi_kommentti(self, alkupMerk, korvattavaMerk):
    if self.rivi.jonoton.strip()[0] == alkupMerk:
      self.rivit.append(re.sub(alkupMerk, korvattavaMerk, self.rivi.koko + '\n', 1))
      self.sisennys.riviNum += 1
      return True
    return False