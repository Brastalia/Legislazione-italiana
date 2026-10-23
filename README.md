# Legislazione Italiana 🇮🇹

Archivio **in costruzione** di metadati normativi italiani, organizzato per territorio, tipo e anno. **Non contiene ancora tutte le leggi.**

## Fonti ufficiali
- https://www.normattiva.it/
- https://dati.normattiva.it/
- https://www.gazzettaufficiale.it/
- https://www.normattiva.it/legislazioneRegionale

## Struttura
- `nazionale/<tipo>/<anno>/`
- `regioni/<regione>/<tipo>/<anno>/` (20 regioni)
- `province-autonome/<provincia>/`
- `materie/` (indici tematici, senza duplicazione)
- `dati/` (fonti e metadati)

## Importazione
Eseguire `python scripts/importa_catalogo.py catalogo.jsonl` su dati ufficiali verificati. Lo script **non scarica automaticamente leggi**: serve prima configurare e verificare i connettori alle fonti. Ogni scheda deve avere URL ufficiale e metadati verificabili. Non interpretare questo archivio come fonte legale autentica.
