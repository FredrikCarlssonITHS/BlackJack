import random
import functools
import os 
from datetime import datetime
import pandas as pd

def rensa_skärm():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

class Person:
    def __init__(self, namn, är_dator, är_dealer):
        
        self.spelkort = []
        self.namn = namn
        self.är_dator = är_dator
        self.är_dealer = är_dealer
        self.antal_spelkort = 0
        self.kort_summa = 0
        self.resultat = ""
        self.antal_vinster = 0
        self.antal_blackjack = 0
        self.antal_spelrundor = 0
        self.vinstprocent = 0
        
    def __str__(self):
        return f"Spelare: {self.namn}"
    def läggtill_spelkort(self, spelkort):
        self.spelkort.append(spelkort)
        self.antal_spelkort += 1

    def uppdatera_statistik(self, vinster, blackjack):
        self.antal_vinster += vinster
        self.antal_blackjack += blackjack
        self.antal_spelrundor += 1
        self.vinstprocent = 100 * (self.antal_vinster / self.antal_spelrundor)

    def ta_spelkort(self, spelkort):
        self.spelkort.append(spelkort)
        self.antal_spelkort += 1
    def dölj_spelkort(self, index=-1):
        self.spelkort[index].är_dolt=True
    def lista_spelkort(self):
        return list(map(str, self.spelkort))        
    def skriv_spelkort(self):
        for i in self.spelkort:
            print(self.namn)
            print(i)
    def nollställ_spelare(self):
        self.spelkort.clear()
    def skriv_antal_spelkort(self):
        print(f"{self.namn} antal spelkort: {self.antal_spelkort}")    

class Spelkort:
    def __init__(self, färg, färg_kort_kod, nummer, typ, värde, kortlek_nr):
        # lägg till spelkort
        self.färg = färg
        self.färg_kort_kod = färg_kort_kod
        self.nummer = nummer
        self.namn = str(nummer) if typ=="Nummerkort" else typ
        self.typ = typ
        self.värde = värde
        self.kortlek_nr = kortlek_nr
        self.är_dolt = False 

    def __str__(self):
        if self.typ == "E":
            return f"({self.värde}/11) {self.färg} {self.namn}" 
        else:
            return f"({self.värde}) {self.färg} {self.namn}" 

class Kortlek:
    def __init__(self, spelkort=[]):
        self.spelkort = spelkort
        self.namn = "Kortlek"
        self.antal_spelkort = 0

    def läggtill_spelkort(self, spelkort):
        self.spelkort.append(spelkort)
        self.antal_spelkort += 1

    def tabort_spelkort(self):
        self.antal_spelkort -= 1
        return(self.spelkort.pop())

    def tabort_alla_spelkort(self):
        self.spelkort.clear()

    def lista_spelkort(self):
            return list(map(str, self.spelkort))
    def blanda(self):
            random.shuffle(self.spelkort)

class Spel:
    # konstanter för spelare / filnamn
    DEALER = 0
    SPELARE1 = 1
    HIGHSCORE_FIL = "highscore.csv"

    def __init__(self):
        self.spelare = []
        self.kortlek = []

        self.antal_kortlekar = 0
        self.antal_spelkort = 0
        self.antal_spelare = 0
        self.antal_oavgjort = 0
        self.vinnare = -1
        self.resultat = ""
    def läggtill_kortlek(self, antal_kortlekar):
        self.kortlek = Kortlek()
        färger = ["Hjärter", "Ruter", "Spader", "Klöver"]
        for a in range(0, antal_kortlekar):
            for f in färger:
                self.kortlek.läggtill_spelkort(Spelkort(f"{f}", f[0], 1, "E", 1, a))
                for i in range(2, 11):
                    self.kortlek.läggtill_spelkort(Spelkort(f"{f}", f[0], i, "Nummerkort", i, a))
                self.kortlek.läggtill_spelkort(Spelkort(f"{f}", f[0], 11, "Kn", 10, a))
                self.kortlek.läggtill_spelkort(Spelkort(f"{f}", f[0], 12, "D", 10, a))
                self.kortlek.läggtill_spelkort(Spelkort(f"{f}", f[0], 13, "K", 10, a))

        self.antal_kortlekar = antal_kortlekar
        self.antal_spelkort = self.kortlek.antal_spelkort
    def läggtill_spelare(self, namn, är_dator, är_dealer):
        self.spelare.append(Person(namn, är_dator, är_dealer))
        self.antal_spelare += 1
    
    def tabort_kortlekar(self):
        self.kortlek.clear()

    def skriv_antal_spelkort(self):
        print(f"Antal spelkort i banken: {self.kortlek.antal_spelkort}")
        
    def ta_kort(self, person, antal):
         for i in range(0, antal):
            översta_spelkort = self.kortlek.tabort_spelkort()
            person.läggtill_spelkort(översta_spelkort)

    def skriv_spelbord(self):
        
        rensa_skärm()
        
        for i in self.spelare:
            print("")
            print("==========================================")
            print(i)
            print("==========================================")
            print(f"Antal vinster: {i.antal_vinster}/{i.antal_spelrundor} Vinstprocent: {format(i.vinstprocent,".2f")}%")
            print("")
            for s in i.spelkort:
                if s.är_dolt==False or self.resultat != "":
                    print(s)
                else:
                    print(f"?")

        print("")
        if self.resultat != "":
            print(self.resultat)                    


    def nollställ_spel(self):
        self.kortlek.tabort_alla_spelkort()
        self.resultat=""
        for i in self.spelare:
            i.nollställ_spelare()
            i.resultat=""

    def kontrollera(self, spel_slut=False):
        # räkna ut summa av kort och antal ess för spelare
        for i in self.spelare:
            kort_summa = functools.reduce(lambda a, b: a + b, map(lambda spelkort: spelkort.värde, i.spelkort), 0)
            antal_ess = len([s for s in i.spelkort if s.typ == 'E'])

            # uppdatera kort summa / resultat
            i.kort_summa = kort_summa
            i.resultat = ""

            # kontrollera kort summa och ev ess för spelare
            if kort_summa > 21: i.resultat = "Tjock"
            elif kort_summa == 21: i.resultat = "Black Jack"
            elif antal_ess > 0 and kort_summa + 10 == 21: i.resultat = "Black Jack"
            elif antal_ess > 0 and (kort_summa + 10) > 16 and (kort_summa + 10) < 21: 
                i.resultat = "Stanna"
                i.kort_summa = kort_summa + 10
            elif antal_ess == 0 and kort_summa > 16 and kort_summa < 21: i.resultat = "Stanna"

        # kontrollera om någon av spelarna vunnit eller förlorat
        if self.resultat == "":
            if self.spelare[self.DEALER].resultat == "Black Jack" and self.spelare[self.SPELARE1].resultat != "Black Jack": 
                self.resultat = "Huset fick 21 och vinner"
                self.spelare[self.DEALER].uppdatera_statistik(1, 1)
                self.spelare[self.SPELARE1].uppdatera_statistik(0, 0)
            elif self.spelare[self.DEALER].resultat != "Black Jack" and self.spelare[self.SPELARE1].resultat == "Black Jack": 
                self.resultat = "Spelare fick 21 och vinner"
                self.spelare[self.SPELARE1].uppdatera_statistik(1, 1)
                self.spelare[self.DEALER].uppdatera_statistik(0, 0)
            elif self.spelare[self.DEALER].resultat == "Tjock":
                self.resultat = "Huset blev tjock. Spelare vinner"
                self.spelare[self.SPELARE1].uppdatera_statistik(1, 0)
                self.spelare[self.DEALER].uppdatera_statistik(0, 0)
            elif self.spelare[self.SPELARE1].resultat == "Tjock": 
                self.resultat = "Du blev tjock. Huset vinner"
                self.spelare[self.DEALER].uppdatera_statistik(1, 0)
                self.spelare[self.SPELARE1].uppdatera_statistik(0, 0)

        # om ingen har fått blackjack, kontrollera vem som har högst totalsumma
        if spel_slut==True and self.resultat == "":
            if self.spelare[self.DEALER].kort_summa > self.spelare[self.SPELARE1].kort_summa: 
                self.resultat = "Huset vinner, högst totalsumma"
                self.spelare[self.DEALER].uppdatera_statistik(1, 0)
                self.spelare[self.SPELARE1].uppdatera_statistik(0, 0)                
            elif self.spelare[self.SPELARE1].kort_summa > self.spelare[self.DEALER].kort_summa: 
                self.resultat = "Spelare vinner, högst totalsumma"
                self.spelare[self.DEALER].uppdatera_statistik(0, 0)
                self.spelare[self.SPELARE1].uppdatera_statistik(1, 0)                
            elif self.spelare[self.DEALER].kort_summa == self.spelare[self.SPELARE1].kort_summa: 
                self.resultat = "Oavgjort, samma totalsumma"
                self.spelare[self.DEALER].uppdatera_statistik(0, 0)
                self.spelare[self.SPELARE1].uppdatera_statistik(0, 0)                
                self.antal_oavgjort += 1

        return(self.resultat)

    def spara_highscore(self):
        
        try:
            data = {
                'Namn': [self.spelare[self.SPELARE1].namn],
                'Vinster': [self.spelare[self.SPELARE1].antal_vinster],
                'Vinstprocent': [round(self.spelare[self.SPELARE1].vinstprocent,2)],
                'Datum': [datetime.now().strftime("%Y-%m-%d")]}

            df = pd.DataFrame(data)

            # om ingen highscore fil, skapa ny med header, annars lägg till rader utan att skriva header
            if os.path.isfile(self.HIGHSCORE_FIL)==False:
                df.to_csv(self.HIGHSCORE_FIL, mode='w', index=False, header=True)
            else:
                df.to_csv(self.HIGHSCORE_FIL, mode='a', index=False, header=False)

        except FileNotFoundError:
            print(f"Highscore fil {self.HIGHSCORE_FIL} kunde ej hittas. Spela några rundor först!")
        except Exception as e:
            print(f"Ett mycket allvarligt generellt fel uppstod: {e}")        


    def visa_highscore(self):

        try:
            df = pd.read_csv(self.HIGHSCORE_FIL).sort_values(by=['Vinstprocent'], ascending=False)
            print(df.to_string(index=False))
        except FileNotFoundError:
            print(f"Highscore fil {self.HIGHSCORE_FIL} kunde ej hittas. Spela några rundor först!")
        except Exception as e:
            print(f"Ett mycket allvarligt generellt fel uppstod: {e}")        


