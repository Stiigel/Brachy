#!/usr/bin/python3
import sys, re, argparse, glob, subprocess, os
from tiedosto import *
from braparsija import *
from javaparsija import *

tiedosto = Tiedosto()
parsija = Javaparsija() if '--javapars' in sys.argv else BraParsija()

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

paatteeton = os.path.splitext(filut[0])[0]

if '--javac' in sys.argv:  
  subprocess.call(['javac', paatteeton + '.java'])

if '--java' in sys.argv:
  subprocess.call(['javac', paatteeton + '.java'])
  subprocess.call(['java', paatteeton])
                  
