# BlackJack
Inlämningsuppgift 1

Spelet körs genom att köra filen "blackjack.py" som startar huvudmeny.
Välj 1 för att spela Blackjack eller 2 för att se highscore.

Spelet använder grundläggande black jack regler och de regler som defineras i uppgiften.
Efter avslutat spel sparas highscore i fil "highscore.csv".
Pandas dataframe används för att ladda och presentera highscore lista.
Spelet bygger på klasser med metoder för att generera spelkort, hantera logik etc. 
Dessa klasser finns i "spelmotor.py"

## Strukturen för klasserna
En stor del av spelet hanteras av klassen Spel och dess metoder. Spel klassen håller en instans av Kortlek som i sin tur håller 52 instanser av Spelkort (eller fler beroende på hur många kortlekar som används i spelet, vilket styrs av en inparameter till läggtill_spelkort metoden i Spel). Spel innehåller även 2 instanser av Person. Detta avser Dealer och Spelare1 och håller resultat, statistik och metoder för att hantera spelaren. Metoden "kontrollera" i klassen Spel kontrollerar om någon av spelarna fått Black Jack, blivit tjock, i dealerns fall stanna eller om någon vunnit på högst kortsumma eller det blivit oavgjort.

Spel

&nbsp;&nbsp;&nbsp;Kortlek

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Spelkort

&nbsp;&nbsp;&nbsp;Person (spelare)

## Operativssystem
Spelet är utvecklat och testat på en Windows maskin. Har ej haft möjlighet att testa funktionen "rensa_skärm" på annat operativssystem.