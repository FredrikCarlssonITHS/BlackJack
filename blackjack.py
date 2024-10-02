import spelmotor

def meny():
    try:
        spelmotor.rensa_skärm()
        print("=======================================================")
        print("Black Jack v1.0 av Fredrik Carlsson")
        print("=======================================================")
        print("")
        print("1) Spela Black Jack")
        print("2) Highscore")
        print("A) Avsluta")
        alternativ = input(">")
        match (alternativ.upper()):
            case "1":
                SpelaMotDator()
            case "2":
                VisaHighScore()
            case "A":
                print("Tack för idag, välkommen åter !")
                exit()
            case _:
                print ("Felaktigt alternativ")
                input("Tryck ENTER för att återgå till meny.")
                meny()

    except Exception as e:
        print(f"Ett mycket allvarligt generellt fel uppstod: {e}")   

def VisaHighScore():

    try:

        # rensa skärm
        spelmotor.rensa_skärm()

        # skriv rubrik
        print("=======================================================")
        print("Highscore")
        print("=======================================================")

        # skapa spelmotor och ladda in highscore
        spel = spelmotor.Spel()
        spel.visa_highscore()
        print()
        input("Tryck ENTER för att återgå till meny.")
        meny()    

    except Exception as e:
        print(f"Ett mycket allvarligt generellt fel uppstod: {e}")   

def SpelaMotDator():
    #Skapa ett program som simulerar ett blackjack-spel mellan en spelare och en dator.
    #          Spelet spelas med en vanlig kortlek som blandas innan varje runda.
    #·         Varje spelare får två kort i början av spelet. Datorn visar bara upp ett av sina kort.
    #·         Spelaren kan välja att ta fler kort (hit) eller stanna på sina nuvarande kort (stand).
    #·         Spelaren kan fortsätta att ta kort tills hen når 21 poäng eller över.
    #·         Om spelaren går över 21 poäng förlorar hen direkt.
    #·         När spelaren stannar, spelar datorn sin tur. Datorn måste ta kort så länge summan av korten är mindre än 17 poäng och stanna när datorns kortsumma är 17 poäng eller mer.
    #·         Om datorn går över 21 poäng vinner spelaren oavsett vilka kort spelaren har.
    #·         Om varken spelaren eller datorn går över 21 poäng så vinner den som har högst kortsumma.

    try:

        # ange namn
        spelare1 = input("Ange ditt namn [ENTER=Spelare1]: ")
        if spelare1 == "": spelare1 = "Spelare1" 

        # skapa spelmotor
        spel = spelmotor.Spel()

        # skapa spelare
        spel.läggtill_spelare("Dealer", True, True)
        spel.läggtill_spelare(spelare1, False, False)

        # spelets yttre loop, loopar spelrundor
        while True:
            # lägg till kortlek, inparameter anger antal kortlekar som ska användas
            spel.läggtill_kortlek(1)

            # blanda korten
            spel.kortlek.blanda()

            # ge två kort till varje spelare
            spel.ta_kort(spel.spelare[spel.SPELARE1], 2)    
            spel.ta_kort(spel.spelare[spel.DEALER], 2)

            # dölj ett av dealerns kort
            spel.spelare[spel.DEALER].dölj_spelkort(0)

            # visa aktuell kort status
            spel.kontrollera()
            spel.skriv_spelbord()

            antal_omgångar = 1
            # spelomgångens huvudloop, avslutas när någon vunnit eller det blivit oavgjort
            while True:
                antal_omgångar += 1
                if spel.resultat == "": 
                    alternativ = input("T = Ta kort  S = Stanna A = Avsluta >")
                    match (alternativ.upper()):
                        case "T":
                            spel.ta_kort(spel.spelare[spel.SPELARE1], 1)
                            spel.kontrollera()
                            spel.skriv_spelbord()

                        case "S":
                                #Datorn måste ta kort så länge summan av korten är mindre än 17 poäng och stanna när datorns kortsumma är 17 poäng eller mer.
                            while spel.spelare[spel.DEALER].resultat=="":
                                spel.ta_kort(spel.spelare[spel.DEALER], 1)
                                spel.kontrollera()
                                spel.skriv_spelbord()
                            spel.kontrollera(True)                                            
                            spel.skriv_spelbord()
                        case "A":    
                            spel.spara_highscore()
                            print ("Tack för att du spelat Black Jack")
                            input("Tryck ENTER för att återgå till meny.")
                            meny()
                else:
                    spel.skriv_spelbord()
                    alternativ = input("ENTER = Ny runda A = Avsluta >")                        
                    if alternativ.upper() == "A": 
                        spel.spara_highscore()
                        meny()
                    break
            
            # nollställ inför nästa runda
            spel.nollställ_spel()

    except Exception as e:
        print(f"Ett mycket allvarligt generellt fel uppstod: {e}")   


# ladda huvudmeny vid start av program
meny()