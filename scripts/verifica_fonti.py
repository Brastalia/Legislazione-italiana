#!/usr/bin/env python3
"""Controlla raggiungibilità delle fonti ufficiali senza scaricare i testi."""
import datetime,json,pathlib,urllib.request
ROOT=pathlib.Path(__file__).resolve().parents[1]
sources=[
 ("normattiva","https://www.normattiva.it/"),
 ("open-data","https://dati.normattiva.it/"),
 ("gazzetta-ufficiale","https://www.gazzettaufficiale.it/"),
 ("legislazione-regionale","https://www.normattiva.it/legislazioneRegionale")
]
out=[]
for name,url in sources:
    try:
        req=urllib.request.Request(url,headers={"User-Agent":"LegislazioneItalianaMonitor/0.1"})
        with urllib.request.urlopen(req,timeout=20) as resp:
            out.append({"fonte":name,"url":url,"status":resp.status,"raggiungibile":200<=resp.status<400})
    except Exception as exc:
        out.append({"fonte":name,"url":url,"raggiungibile":False,"errore":str(exc)[:200]})
report={"controllato_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"fonti":out,"nota":"Monitor disponibilità, NON aggiornamento delle leggi"}
(ROOT/"dati"/"stato-fonti.json").write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
print(json.dumps(report,indent=2,ensure_ascii=False))
