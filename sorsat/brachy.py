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

if len(sys.argv) > 2 and sys.argv[1] == '--s':
  for sis in sys.argv[2].split('\n'):
    parsija.parsi_rivi(sis)
else:    
  for sis in tiedosto.avaa(filut):
    parsija.parsi_rivi(sis)

parsija.loppuaallot()
   
if not '--eitulost' in sys.argv:
  for rivi in parsija.rivit:
    print(rivi, end="")

if '--eital' not in sys.argv:
  tiedosto.kirjoita_luokat(parsija.luokat, parsija.rivit)

paatteeton = os.path.splitext(filut[0])[0]
if '--javac' in sys.argv:  
  subprocess.call(['javac', paatteeton + '.java'])

if '--java' in sys.argv:
  subprocess.call(['javac', paatteeton + '.java'])
  subprocess.call(['java', paatteeton])
                  
if '--tmc' in sys.argv:
  subprocess.call(['tmc', 'su'])