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
          luettava = open(tiedosto, 'r')
          sisalto.extend(luettava.readlines())
          luettava.close()
        except OSError:
          print(tiedosto + ' - Ei suuchia tiedostoa')
    return sisalto

  def kirjoita(self,luokka):
    tiedosto = open(luokka.nimi + ".java", 'w')
    for usame in luokka.usamet:
      tiedosto.write('import ' + usame + '\n')
      
    for rivi in luokka.rivit:
      tiedosto.write(rivi)
    tiedosto.close()
    
  def kirjoita_luokat(self, luokat, rivit):
    for i in range(len(luokat)):
      if i == len(luokat) - 1:
        luokat[i].rivit = rivit[luokat[i].alku:]
      else:
        luokat[i].rivit = rivit[luokat[i].alku: luokat[i + 1].alku]
    
      self.kirjoita(luokat[i])