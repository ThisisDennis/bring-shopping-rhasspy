# Old -SNIPS Bring! Shopping List- Refactored for Rhasspy (Rhasspy-Hermes-App)

## Preamble

The Original was written by https://github.com/philipp2310 (https://github.com/philipp2310/snips-bring-shopping). 
I changed a few things to make it work on Rhasspy.

There is also a List of Items for shopping lists (SlotsAndSentences4Rhasspy/bringItems) a manual may come... 
or not.

Rename "congfig copy.ini" to "config.ini" fill the uuid's and change the path in action-bring.py to your path at "CONFIG_INI=...".
You may wanna use setupWithService.sh. Show the Logs with logs.sh, reload after changes with reload.sh.
Have fun

Connect your Rhasspy Assistant to your Bring! shopping list!
With Bring! your list will be available on Android, iOs and via Web Access.
## Languages
- German ✓
- English ~ (translated, but not in store)

## Featuers
- Add Item(s) ✓
- Remove Item(s) ✓
- Read shopping List ✓
- Ask for Item on List ✓

## Future Ideas:
- Change Quantity
- Show list on Screen
- add complete lists from receipt

## Setup
This skill for Rhasspy takes two secret parameters:
The first one is your unique user ID, the second one is the unique ID of your shopping list.
You can get these here after you fill in your credentials: https://api.getbring.com/rest/bringlists?email=~mail-adress~&password=~password~

## Usage
### Deutsch:

Add:  
Hey <Wakeword>, schreibe Mehl auf meine Einkaufsliste  
Hey <Wakeword>, bitte füge Eier zum Einkaufszettel hinzu  

Remove:  
Hey <Wakeword>, streiche Mehl von meiner Einkaufsliste  

Read:  
Hey <Wakeword>, les mir meine Einkaufsliste vor  

Ask:  
Hey <Wakeword>, habe ich Kartoffeln schon auf meiner Einkaufsliste?  

(idea) Change Quantity:  
Hey <Wakeword>, füge zwei Kästen Bier zu meiner Liste hinzu  
- Es befinden sich bereits zwei Kästen Bier auf deiner Liste, soll ich "zwei Kästen" hinzufügen?  
Ja/Nein, mach insgesamt 3 Kästen.  

(idea) Add List:  
Hey <Wakeword>, schreibe alles für Pizza Hawaii auf meine Einkaufsliste  
- Ok, ich füge hinzu:
- Mehl, 400g  
Nein/Stop -> Ok, kein Mehl  
- Öl, 6 Esslöffel
- Tomaten Sauce, 1 Pack
- Schinken, 1 Pack
- Ananas, 1 Stück
- Die folgenden Dinge solltest du haben, fehlt doch etwas?
- Salz  
Ja/Stop -> Ok, ich setze Salz auf die Einkaufsliste  
- Wasser

(idea) Show List:  
Hey <Wakeword>, zeige mir meine Einkaufsliste  
- <keine Antwort, Anzeige auf Display>  
