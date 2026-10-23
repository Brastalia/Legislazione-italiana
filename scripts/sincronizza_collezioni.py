#!/usr/bin/env python3
"""Acquisisce il catalogo delle collezioni predefinite dall'API Normattiva.
Non equivale all'importazione dei testi delle leggi.
"""
import datetime,json,pathlib,urllib.request
ROOT=pathlib.Path(__file__).resolve().parents[1]
URL="https://api.normattiva.it/t/normattiva.api/bff-opendata/v1/api/v1/collections/collection-predefinite"
req=urllib.request.Request(URL,headers={"Accept":"application/json","User-Agent":"LegislazioneItaliana/0.2 (catalogo pubblico)"})
with urllib.request.urlopen(req,timeout=45) as response:
    raw=response.read(5_000_001)
    if len(raw)>5_000_000: raise RuntimeError("Risposta oltre limite")
    data=json.loads(raw)
dest=ROOT/"dati"/"collezioni-normattiva.json"
dest.write_text(json.dumps({"fonte":URL,"aggiornato_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"collezioni":data},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(f"Catalogo salvato in {dest}")
