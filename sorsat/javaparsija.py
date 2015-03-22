from parsija import *

class Javaparsija(Parsija):
  
  def parsi_rivi(self, rivi):
    self.laita_rivi(rivi)
    
    if len(self.rivi.jonoton.strip()) > 0:
      if self.parsi_kommentti('//', '#'):
        return
    
    
     
    
    
  
    