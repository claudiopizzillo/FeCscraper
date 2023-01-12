# FeCscraper
Scraper for Sogei's Fatture e Corrispettivi service.
Library to install via pip: requests, pytz, clint, tqdm.

Input field in order:

CF (or Entratel code) of your FeC service.
PIN  of your FeC service.
Password of your FeC service.
Your Partita IVA
Date from
Date to
FOL or ENT (FiscoOnLine user or Entratel user)

Ex: fec.py PZZCLD79D79H345Y 3456789 mypassword 01234567891 01012019 01032019 FOL

In the subfolder "Ricevute_PIVA" you will find your FE and related metadati.

Enjoy!

[ITALIANO]

Scraper per il servizio Fatture e Corrispettivi.
Librerie da installare via pip: requests, pytz, clint, tqdm.

Dati di input in ordine:

CF (o codice Entratel) di FeC.
PIN di FeC.
Password di FeC.
Partita IVA
Data dal
Data al
FOL o ENT (utente FiscoOnLine o utente Entratel)

Nella sottocartella Ricevute_PIVA troverai le tue FE e i relativi metadati.
