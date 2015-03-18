import re

class Rivi:
  def __init__(self, koko):
    self.koko = koko
    self.jonot = []
    self.jonoton = ""
    self.poista_mjonot()
    self.lisattyAaltis = False
  
  def sub(self, juttu, korvaus):
    self.jonoton = re.sub(juttu, korvaus, self.jonoton)
    
  def poista_mjonot(self):
    self.jonot = []
    for jono in re.finditer(r'("(.*?)")|(\'(.*?)\')', self.koko):
      self.jonot.append(jono.group(0))
  
    self.jonoton = re.sub(r'("(.*?)")|(\'(.*?)\')', r'¡Streng!', self.koko)
    
  def palauta_mjonot(self, aukiSulut):
    self.lisaa_puolipiste(aukiSulut)
    
    self.koko = self.jonoton
    for i in range(len(self.jonot)):
      self.koko = self.koko.replace('¡Streng!', self.jonot[i], 1)   
 
  def lisaa_puolipiste(self, aukiSulut):
    if not self.lisattyAaltis:
      if aukiSulut == 0:
        if self.jonoton.strip() != '':
          if self.jonoton.strip()[-1] != ';':
            erotus = len(self.jonoton) - len(self.jonoton.rstrip())
            self.jonoton = self.jonoton[:-erotus] + ';' + self.jonoton[-erotus:]
      
      
      
      