import sys

class Sisennys:
  def __init__(self):
    self.ero = -1
    self.taso = 0
    self.ed = 0
    self.tasot = []
    self.aukiSulut = 0
    self.funkSisennys = -1
    self.riviNum = 0
    
  def laita_sisennys(self, rivi, rivit):
    self.laske(rivi)
    self.aaltosulut(rivit)
    self.laita_ero()
    
  def onko_funktiossa(self, funktiossa):
    if funktiossa:
      if self.taso <= self.funkSisennys:
        self.funkSisennys = -1
        return False
    return funktiossa
  
  def laita_funkSisennys(self):
    self.funkSisennys = self.taso
  
  def laske(self, rivi):
    if self.aukiSulut == 0:
      self.taso = len(rivi) - len(rivi.lstrip())
    self.handlaa_sulut(rivi)
  
  def laita_ed(self):
    self.ed = self.taso
    
  def laita_ero(self):
    if self.ero == -1:
      if self.taso != 0:
        self.ero = self.taso
        
  def lisaa(self):
    self.tasot.append(self.taso)
    
  def aaltosulut(self, rivit, loppu=False):
    maara = 0
    if not loppu:
      if self.taso >= self.ed:
        return 
    else:
      self.taso = 0
    
    taso = self.taso
    for i in range(int((self.ed - self.taso) / self.ero)):
      taso += self.ero
      
      valit = self.tasot[-1] * " "
      rivit.append(valit + "}\n")
      self.tasot = self.tasot[0:-1]
      
      maara += 1
      
    self.riviNum += maara
    return
  
  def handlaa_sulut(self, rivi):
    self.aukiSulut += rivi.count('(') - rivi.count(')')
    if self.aukiSulut < 0:
      print("SUREKA SUÖLUTUS")
      sys.exit()
    
    if self.aukiSulut > 0:
      return True
    return False    
    