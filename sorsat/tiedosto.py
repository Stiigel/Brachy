import sys

class Tiedosto:    
  def avaa(self,tiedostot):
    sisalto = []
    if len(tiedostot) < 1:
      sys.exit('¡Anna väh 1 käännettävä tiedosto')
    else:
      for tiedosto in tiedostot:
        if tiedosto[0:2] == "--":
          break
        
        try:
          with open(tiedosto, 'r') as luettava:
            sisalto.extend(luettava.read().rstrip().split('\n'))
            
        except OSError:
          print(tiedosto + ' - Ei suuchia tiedostoa')
          
    return sisalto

  def kirjoita(self,luokka):
    with open(luokka.nimi + '.java', 'w') as tiedosto:
      tiedosto.write('import java.util.*;\n')
      for usame in luokka.usamet:
        tiedosto.write('import ' + usame + ';\n')
      
      for rivi in luokka.rivit:
        tiedosto.write(rivi)
    
  def kirjoita_luokat(self, luokat, rivit):
    for i in range(len(luokat)):
      if i == len(luokat) - 1:
        luokat[i].rivit = rivit[luokat[i].alku:]
      else:
        luokat[i].rivit = rivit[luokat[i].alku: luokat[i + 1].alku]
    
      self.kirjoita(luokat[i])