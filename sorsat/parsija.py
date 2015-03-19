import re, itertools
from rivi import *
from sisennys import *
from luokka import *
from rivi import *

class Parsija:
  def __init__(self):
    self.luokat = []
    self.rivit = []
    self.luokkaNyt = -1
    self.julkisuus = True 
    self.funktiossa = False
    self.sisennys = Sisennys()
  
  def parsi_rivi(self, rivi):
    self.rivi = Rivi(rivi)
  
    if len(self.rivi.jonoton.strip()) > 0:
      if self.rivi.jonoton.strip()[0] == '#':
        self.rivit.append(re.sub('#', '//', self.rivi.koko + '\n', 1))
        self.sisennys.riviNum += 1
        return
      self.sisennys.laita_sisennys(self.rivi.jonoton, self.rivit)
      
      self.funktiossa = self.sisennys.onko_funktiossa(self.funktiossa)
    
    if self.parsi_julkisuus():
      return
  
    if not self.rivi.jonoton.endswith('\n'):
      self.rivi.jonoton += '\n'
      
    self.lisaa_luokka()
    self.parsi_luokkajuttu()

    uusiFunktio = self.parsi_funktiot()
    if uusiFunktio and not self.funktiossa:
      self.funktiossa = True
      self.sisennys.laita_funkSisennys()
  
    self.parsi_sekalaisia()
    self.parsi_tyypit()
    self.parsi_tern()
  
    if self.parsi_silmukat():
      self.sisennys.lisaa()
      self.rivi.lisattyAaltis = True
  
    if self.parsi_demas():
      self.sisennys.lisaa()
      self.rivi.lisattyAaltis = True 
      self.rivit[-1] = self.rivit[-1].rstrip()
      self.rivi.jonoton = ' ' + self.rivi.jonoton.lstrip()
    
    if self.parsi_si():
      self.sisennys.lisaa()
      self.rivi.lisattyAaltis = True
  
    if re.search(':\s*$', self.rivi.jonoton) != None:
      self.rivi.sub(':(\s*)$', ' {\\1')
      self.sisennys.lisaa()
      self.rivi.lisattyAaltis = True
  
    self.parsi_lorslara()
  
  
    if self.luokkaNyt >= 0:
      self.rivi.jonoton = self.luokat[self.luokkaNyt].lisaa_usame(self.rivi.jonoton)
  
    self.rivi.palauta_mjonot(self.sisennys.aukiSulut)

    if uusiFunktio:
      self.kuormita()
    
    self.rivit.append(self.rivi.koko)
      
    self.sisennys.laita_ed()
  
    self.sisennys.riviNum += 1

  def loppuaallot(self):
    self.sisennys.aaltosulut(self.rivit, loppu=True)
  
  def lisaa_luokka(self):
    if "clase" in self.rivi.jonoton or "estruct" in self.rivi.jonoton:
      luokNimi = re.search('( (clase|estruct) (.*?)[ ]*:)|( (clase|estruct) (.*?)\()', self.rivi.jonoton)
      
      if luokNimi != None and 'privado' not in self.rivi.jonoton:      
        self.luokat.append(Luokka(luokNimi.group(3), self.sisennys.riviNum))
        self.luokkaNyt += 1
        self.funktiossa = False
        self.julkisuus = True if "estruct" in self.rivi.jonoton else False
      
  def parsi_luokkajuttu(self):
    self.rivi.sub('público', 'public')
    self.rivi.sub('clase', 'class')
    self.rivi.sub('estruct', 'class')
  
  
  def parsi_sekalaisia(self):
    self.rivi.sub('ent\((.*?)\)', 'Integer.parseInt(\\1)') 
    self.rivi.sub('sos\((.*?)\)', 'Double.parseDouble(\\1)')
    self.rivi.sub('Lector', 'Scanner') 
    self.rivi.sub('Sistema', 'System') 
    self.rivi.sub(' último ', ' final ')

  def parsi_tyypit(self):    
    alkup = self.rivi.jonoton
  
    tyypit = [['cad', 'String'], ['cará', 'char'], ['(?<!mi)ent', 'int'],
              ['sos', 'double'], ['bool', 'boolean'], ['vacío', 'void'],
              ['Ent', 'Integer'], ['Sos', 'Double'], ['Cará', 'Character'],
              ['Bool', 'Boolean'], ['nulo', 'null']]       
  
    keno = chr(92)
    sallitutAlut = '([' + keno + keno.join('s+*/-=[{(<') + '])'
    sallitutLoput = '([' + keno + keno.join('s+*/-=]})>') + '])'
    #sys.exit(sallitutAlut + ' ' + sallitutLoput)
    
  
    for tyyppi in tyypit:
      self.rivi.sub(sallitutAlut + tyyppi[0] + sallitutLoput, "\\1" + tyyppi[1] + "\\2")
    
    for tyyppi in tyypit:
      self.rivi.sub(tyyppi[0] + '\[(.*?)\]', tyyppi[1] + '[\\1]')

    if not self.funktiossa and self.rivi.jonoton.strip() != '':
      if 'usame' not in self.rivi.jonoton and 'class' not in self.rivi.jonoton:
        if self.julkisuus == True:
          self.rivi.jonoton = self.sisennys.taso * " " + "public " + self.rivi.jonoton.lstrip()
        else:
          self.rivi.jonoton = self.sisennys.taso * " " + "private " + self.rivi.jonoton.lstrip()

  def parsi_lorslara(self):
    jutut = [['regresa', 'return'], ['estática', 'static'], ['principal', 'main'],
              ['digame', 'System.out.println'], ['digate', 'System.out.print'],
              ['digafe', 'System.out.printf'], ['Verdado', 'true'],
              ['Falso', 'false'], ['nuevo', 'new'], ['este', 'this'],
              ['rompe', 'break'], [' no ', '!']
            ]
  
    for juttu in jutut: 
      self.rivi.sub(juttu[0], juttu[1])
  
  def parsi_julkisuus(self):  
    if self.rivi.jonoton.strip() == 'público':
      self.julkisuus = True
    elif self.rivi.jonoton.strip() == 'privado':
      self.julkisuus = False
    else:
      return False
    return True
  
  def parsi_funktiot(self):
    alkup = self.rivi.jonoton
  
    julk = 'public' if self.julkisuus else 'private'
    self.rivi.sub('(\s|^)det ', '\\1%s ' % julk)

    if alkup != self.rivi.jonoton:
      self.rivi.sub('__inic__', self.luokat[self.luokkaNyt].nimi)
      self.rivi.sub('__cad__', 'String toString')
      return True
    return False

  def kuormita(self):
    jutska = re.search('( .*?)\((.*)\)', self.rivi.koko)
    argumentit = jutska.group(2).split(',')
  
    optOsat = []
    namOsat = []
  
    for arg in jutska.group(2).split(','): 
      osat = arg.split('=')
      if len(osat) > 1:
        optOsat.append(osat)
      else:
        namOsat.append(osat)
      
      if len(optOsat) > 0:
        nArgs = ','.join([''.join(osat) for osat in namOsat])
        #print(nArgs)
        tyhja = re.sub('\((.*)\)', '()', self.rivi.jonoton)

        for i in range(len(optOsat) + 1):
          for alajutut in itertools.combinations(optOsat, i):
            oArgs = [juttu[0] for juttu in alajutut if len(juttu) > 0]          
            oArgs = ',' + ','.join(oArgs) if len(oArgs) > 0 else ''
      
            puuttuvat = [arg[1] for arg in optOsat if arg not in alajutut]         
            funktio = re.sub('\((.*)\)', '(%s%s)' % (nArgs, oArgs), tyhja)
        
            funkNimi = re.search(' (\S*?)\(', self.rivi.jonoton).group(1)
        
            #print(namOsat)
            namNimet = ','.join([osa[0].split()[1] for osa in namOsat])
        
            pohja = """{funk}{sis}{ero}this.{funkNim}({nimet}, {puuttuvat})
{sis}}}
"""
            print(pohja.format(sis=self.sisennys.taso*' ', funk=funktio, 
                                ero=self.sisennys.ero*' ', funkNim=funkNimi,
                                nimet=namNimet, puuttuvat=', '.join(puuttuvat)))
        
        
  
  

  def parsi_tietotyypit(self):
    tietotyypit = ['AL ArrayList', 'L List', 'HM HashMap',
                    'HS HashSet', 'S Set']
  
    for tyyppi in tietotyypit:
      tyyppi = tyyppi.split()
      #self.rivi.sub('%s<.*?> 
    

  def parsi_silmukat(self):
    alkup = self.rivi.jonoton
    self.rivi.sub('mientras (.*):', 'while (\\1) {')
  
    if re.search('para .*?;.*?;*?:', self.rivi.jonoton) != None:
      self.rivi.sub('para(.*?):', 'for (\\1) {')
    
    elif re.search('para .*?en intervalo\(.*?:', self.rivi.jonoton) != None:
      vali = re.search('intervalo\((.*)\)', self.rivi.jonoton)
      if vali != None:
        arvot = vali.group(1).split(',')        
        mista = '0'
        mihin = arvot[0]
      
        if len(arvot) > 1:  
          mista = arvot[0]
          mihin = arvot[1]
        
        lisays = int(arvot[2]) if len(arvot) > 2 else 1
        merkki = '<' if lisays >= 1 else '>'
        self.rivi.sub('para (.*?) (.*?) en intervalo\((.*?)\):',
                      'for (\\1 \\2 = %s; \\2 %s %s; \\2 += %i) {'
                      % (mista, merkki, mihin, lisays))
    
    elif re.search('para .*? en .*?:', self.rivi.jonoton) != None:
      self.rivi.sub('para (.*?) en (.*?):', 'for (\\1 : \\2) {')
  
    if alkup != self.rivi.jonoton:
      return True
    return False

  def parsi_tern(self):
    self.rivi.sub('(\S*) si (.*) demás (.*)', '(\\2) ? \\1 : \\3')
    #self.rivi.sub(' (.*) si (.*) demás (.*)', ' (\\2) ? \\1 : \\3')

  def parsi_demas(self):
    alkup = self.rivi.jonoton
    self.rivi.sub('demássi (.*):', 'else if (\\1) {')
    self.rivi.sub('demás\s*:', 'else {')
  
    if alkup != self.rivi.jonoton:
      return True
    return False

  def parsi_si(self):
    alkup = self.rivi.jonoton
    self.rivi.sub('si (.*):', 'if (\\1) {')
    if alkup != self.rivi.jonoton:
      return True
    return False
