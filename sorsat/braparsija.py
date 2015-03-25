import re, itertools
from rivi import *
from sisennys import *
from luokka import *
from rivi import *
from parsija import *

class BraParsija(Parsija):
  
  def parsi_rivi(self, rivi):
    self.laita_rivi(rivi)
      
    if len(self.rivi.jonoton.strip()) > 0:
      if self.parsi_kommentti('#', '//'):
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
    if any(jut in self.rivi.jonoton for jut in ['clase', 'estruct', 'interfaz']):
      luokNimi = re.search('( (clase|estruct|interfaz) (.*?)[: ])', self.rivi.jonoton)
      
      if luokNimi != None and 'privado' not in self.rivi.jonoton:      
        self.luokat.append(Luokka(luokNimi.group(3), self.sisennys.riviNum))
        self.luokkaNyt += 1
        self.funktiossa = False
        
        if 'clase' in self.rivi.jonoton: self.julkisuus = 'private'
        elif 'estruct' in self.rivi.jonoton: self.julkisuus = 'public'
        elif 'interfaz' in self.rivi.jonoton: self.julkisuus = ''
      
  
  def parsi_lista(self, lista):
    for alkio in lista:
      osat = alkio.split()
      self.rivi.sub(self.sAlut + osat[0] + self.sLoput, "\\1" + osat[1] + "\\2")
      
  def parsi_luokkajuttu(self):
    jutut = ['público public', 'clase class', 'estruct class',
             'interfaz interface', 'herramienta implements',
             'extenda extends', 'abstracto abstract']
    self.parsi_lista(jutut)

  def parsi_tyypit(self):    
    alkup = self.rivi.jonoton    
    tyypit = ["cad String", "cará char", "ent int", "sos double",
              "bool boolean", "vacío void", "Ent Integer", "Sos Double",
              "Cará Character", "Bool Boolean", "nulo null"]
    
    self.rivi.sub(self.sAlut + 'ent\((.*?)\)', '\\1Integer.parseInt(\\2)') 
    self.rivi.sub(self.sAlut + 'sos\((.*?)\)', '\\2Double.parseDouble(\\2)')

    self.parsi_lista(tyypit)
    
    if not self.funktiossa and self.rivi.jonoton.strip() != '':
      if 'usame' not in self.rivi.jonoton and 'class' not in self.rivi.jonoton and not self.rivi.jonoton.strip().startswith('@'):
        vali = ' ' if self.julkisuus != '' else ''
        self.rivi.jonoton = self.sisennys.taso * " " + self.julkisuus + vali + self.rivi.jonoton.lstrip()

  def parsi_lorslara(self):
    jutut = ["regresa return", "estática static", "principal main",
             "digame System.out.println", "digate System.out.print", 
             "digafe System.out.printf", "Verdado true", "Falso false",
             "nuevo new", "este this", "rompe break", "no !", 
             "sigue continue", "Lector Scanner", "Sistema System",
             "último final"]
             
    self.parsi_lista(jutut)
 
  def parsi_julkisuus(self):  
    julkisuudet = {'privado' : 'private', 'protegido' : 'protected', 'público' : 'public'}

    if self.rivi.jonoton.strip() in julkisuudet:
      self.julkisuus = julkisuudet[self.rivi.jonoton.strip()]
      return True
    return False
  
  def parsi_funktiot(self):
    alkup = self.rivi.jonoton
  
    self.rivi.sub('(\s|^)det ', '\\1%s ' % self.julkisuus)

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

  def parsi_demas(self):
    alkup = self.rivi.jonoton
    self.rivi.sub('demássi (.*):', 'else if (\\1) {')
    self.rivi.sub('demás\s*:', 'else {')
  
    if alkup != self.rivi.jonoton:
      return True
    return False

  def parsi_si(self):
    alkup = self.rivi.jonoton
    self.rivi.sub('(\s|^)si (.*):', '\\1if (\\2) {')
    if alkup != self.rivi.jonoton:
      return True
    return False
