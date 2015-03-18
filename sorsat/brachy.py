#!/usr/bin/python3
import sys, re, argparse, glob
from tiedosto import *
from parsija import *

tiedosto = Tiedosto()
parsija = Parsija()

if len(sys.argv) > 1:
  filut = sys.argv[1:]
   
else:
  filut = glob.glob('*.bs')
   
for sis in tiedosto.avaa(filut):
  parsija.parsi_rivi(sis)

parsija.loppuaallot()
  #print("koira")
   
if not '--eitulost' in sys.argv:
  for rivi in parsija.rivit:
    print(rivi, end="")
      
tiedosto.kirjoita_luokat(parsija.luokat, parsija.rivit)