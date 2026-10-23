# Piano di importazione progressiva

1. **Nazionali**: acquisire esportazioni ufficiali da https://dati.normattiva.it/ e consultare la documentazione API https://dati.normattiva.it/assets/come_fare_per/Normattiva%20OpenData.html .
2. **Regionali**: utilizzare le banche dati elencate da https://www.normattiva.it/legislazioneRegionale ; verificare per ogni Regione modalità di esportazione, termini d'uso e aggiornamento.
3. Convertire esportazioni in JSONL con almeno tipo, anno, numero, titolo, fonte_url; includere URN, data, versione e stato solo se verificati.
4. Importare con `python scripts/importa_jsonl.py file.jsonl`, oppure caricare un file JSONL in `import/` e avviare manualmente il workflow.
5. Non confondere testo originario, testo vigente e multivigenza. Conservare provenienza e data di acquisizione.
6. Prima di automatizzare download/API, verificare autenticazione, limiti, termini di riutilizzo e formati reali. Non fare scraping aggressivo.

**Stato:** infrastruttura pronta per importazione manuale di dati verificati; non è attiva una sincronizzazione automatica con Normattiva.
