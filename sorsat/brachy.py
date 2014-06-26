#!/usr/bin/python3
import sys, re
from luokka import *
from rivi import *
from sisennys import *
from tiedosto import *
from parsija import *
from vakiot import *

tiedosto = Tiedosto()
parsija = Parsija()
sisennys = Sisennys()

luokat = []
rivit = []
luokkaNyt = -1
riviNum = 0
julkisuus = True
funktiossa = False
funkSisennys = 0

sisalto = tiedosto.avaa(sys.argv[1:])

for sis in sisalto:
  #print(riviNum)
  rivi = Rivi(sis)
  
  if len(rivi.koko.strip()) > 0:
    if rivi.koko.strip()[0] == '#':
      continue                    
    else:
      sisennys.laske(rivi.koko)
      riviNum += sisennys.aaltosulut(rivit)
      sisennys.laita_ero()
  
  julkisuus = parsija.parsi_julkisuus(rivi, julkisuus)
  
  if "público clase" in rivi.jonoton:
    luokNimi = re.search('(público clase (.*?)[ ]*:)|(público clase (.*?)\()', rivi.jonoton)
    if luokNimi != None:      
      luokat.append(Luokka(luokNimi.group(2), riviNum))
      luokkaNyt += 1
    
  rivi.jonoton = re.sub('público ', 'public ', rivi.jonoton)
  rivi.jonoton = re.sub('clase ', 'class ', rivi.jonoton)
  
  rivi.jonoton = re.sub(r'ent\((.*?)\)', r'Integer.parseInt(\1)', rivi.jonoton)
  
  if funkSisennys == sisennys.taso:
    funktiossa = False
  
  if parsija.parsi_funktiot(rivi, julkisuus) and not funktiossa:
    funktiossa = True
    funkSisennys = sisennys.taso
  
  parsija.parsi_tyypit(rivi, funktiossa, julkisuus, sisennys)  
  
  if parsija.parsi_ehdot(rivi):
    sisennys.lisaa()
    rivi.lisattyAaltis = True
  
  if re.search(':', rivi.jonoton) != None:
    rivi.jonoton = re.sub(':', ' {', rivi.jonoton)
    sisennys.lisaa()
    rivi.lisattyAaltis = True
  
  rivi.jonoton = re.sub('regresa', 'return', rivi.jonoton)
  rivi.jonoton = re.sub('estática', 'static', rivi.jonoton)
  rivi.jonoton = re.sub('principal', 'main', rivi.jonoton)
  rivi.jonoton = re.sub('digame', 'System.out.println', rivi.jonoton)
  rivi.jonoton = re.sub('digate', 'System.out.print', rivi.jonoton)
  rivi.jonoton = re.sub('Verdado', 'true', rivi.jonoton)
  rivi.jonoton = re.sub('Falso', 'false', rivi.jonoton)                        
  rivi.jonoton = re.sub('nuevo', 'new', rivi.jonoton)    

  if luokkaNyt >= 0:
    rivi.jonoton = luokat[luokkaNyt].lisaa_usame(rivi.jonoton)
  
  rivi.lisaa_puolipiste(sisennys.aukiSulut)
  rivi.palauta_mjonot()

  riviNum += 1
  rivit.append(rivi.koko)
  sisennys.laita_ed()
  
sisennys.aaltosulut(rivit, loppu=True)

for rivi in rivit:
  print(rivi, end="")

tiedosto.kirjoita_luokat(luokat, rivit)
