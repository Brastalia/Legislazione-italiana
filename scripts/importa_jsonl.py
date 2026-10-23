#!/usr/bin/env python3
"""Importazione incrementale di schede da cataloghi ufficiali esportati in JSONL."""
import argparse, json, pathlib, re, hashlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
REGIONI=set(json.loads((ROOT/"dati/regioni.json").read_text())["regioni"])
TIPI={"leggi-regionali","regolamenti-regionali","statuti","leggi-ordinarie","decreti-legge","decreti-legislativi","dpr","dpcm"}
def safe(s):
    x=re.sub(r"[^a-z0-9-]","-",str(s).lower()).strip("-")
    if not x: raise ValueError("Identificativo vuoto")
    return x
def importa(source):
    total=0
    for n,line in enumerate(source.read_text(encoding="utf-8").splitlines(),1):
        if not line.strip(): continue
        obj=json.loads(line)
        for field in ("tipo","anno","numero","titolo","fonte_url"):
            if not obj.get(field): raise ValueError(f"Riga {n}: manca {field}")
        tipo=obj["tipo"]; anno=int(obj["anno"]); regione=obj.get("regione")
        if tipo not in TIPI or not (1861<=anno<=2100): raise ValueError(f"Riga {n}: tipo/anno errato")
        if regione and regione not in REGIONI: raise ValueError(f"Riga {n}: regione non valida")
        if regione and tipo not in {"leggi-regionali","regolamenti-regionali","statuti"}: raise ValueError("Tipo non regionale")
        if not str(obj["fonte_url"]).startswith("https://"): raise ValueError("Fonte HTTPS richiesta")
        path=(ROOT/"regioni"/regione if regione else ROOT/"nazionale")/tipo/str(anno)
        path.mkdir(parents=True,exist_ok=True)
        digest=hashlib.sha256((str(regione)+tipo+str(anno)+str(obj["numero"])+str(obj.get("data",""))).encode()).hexdigest()[:12]
        file=path/(safe(obj["numero"])+"-"+digest+".json")
        content=json.dumps(obj,ensure_ascii=False,sort_keys=True,indent=2)+"\n"
        if not file.exists() or file.read_text(encoding="utf-8")!=content:
            file.write_text(content,encoding="utf-8")
            total+=1
    return total
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("file",type=pathlib.Path);a=p.parse_args()
    print(f"Nuove schede o schede aggiornate: {importa(a.file)}")
