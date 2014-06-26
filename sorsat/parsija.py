import re
from vakiot import *

class Parsija:
  def parsi_tyypit(self, rivi, funktiossa, julkisuus, sisennys):    
    alkup = rivi.jonoton
    
    rivi.jonoton = re.sub('cad ', 'String ', rivi.jonoton)
    rivi.jonoton = re.sub('cará ', 'char ', rivi.jonoton)
    rivi.jonoton = re.sub('ent ', 'int ', rivi.jonoton)
    rivi.jonoton = re.sub('sos ', 'double ', rivi.jonoton)
    rivi.jonoton = re.sub('bool ', 'boolean ', rivi.jonoton)
    rivi.jonoton = re.sub('vacío ', 'void ', rivi.jonoton)
    rivi.jonoton = re.sub(r'cad\[(.*?)\]', r'String[\1]', rivi.jonoton)
    rivi.jonoton = re.sub(r'cará\[(.*?)\]', r'char[\1]', rivi.jonoton)
    rivi.jonoton = re.sub(r'ent\[(.*?)\]', r'int[\1]', rivi.jonoton)
    rivi.jonoton = re.sub(r'sos\[(.*?)\]', r'double[\1]', rivi.jonoton)
    rivi.jonoton = re.sub(r'bool\[(.*?)\]', r'boolean[\1]', rivi.jonoton)
    #15:44 < Jupp3> kaviaari: Meillä sentään lukiossa äidinkielenopettaja kirjoitti usein rehellisesti punakynällä 
               #marginaaliin "Väärä mielipide"
    if alkup != rivi.jonoton:
      if funktiossa == False:
        if julkisuus == True:
          rivi.jonoton = sisennys.taso * " " + "public " + rivi.jonoton.lstrip()
        else:
          rivi.jonoton = sisennys.taso * " " + "private " + rivi.jonoton.lstrip()

  def parsi_julkisuus(self, rivi, julkisuus):
    if 'clase' not in rivi.jonoton:
      if 'público' in rivi.jonoton:
        julkisuus = True
        rivi.jonoton = re.sub('público', '', rivi.jonoton)
      elif 'privado' in rivi.jonoton:
        julkisuus = False
        rivi.jonoton = re.sub('privado', '', rivi.jonoton)
    else:
      julkisuus = True
    
    return julkisuus
  
  def parsi_funktiot(self,rivi, julkisuus):
    alkup = rivi.jonoton
    if julkisuus == True:
      rivi.jonoton = re.sub('det ', 'public ', rivi.jonoton)
    else:
      rivi.jonoton = re.sub('det ', 'private ', rivi.jonoton)
    
    if alkup != rivi.jonoton:
      return True
    return False
  
  def parsi_ehdot(self, rivi):
    alkup = rivi.jonoton
    
    rivi.jonoton = re.sub('demássi (.*):', 'else if (\\1) {', rivi.jonoton)
    rivi.jonoton = re.sub('si (.*):', 'if (\\1) {', rivi.jonoton)
    rivi.jonoton = re.sub('demás( )*:', 'else {', rivi.jonoton)
    
    if alkup != rivi.jonoton:
      return True
    return False
  
   