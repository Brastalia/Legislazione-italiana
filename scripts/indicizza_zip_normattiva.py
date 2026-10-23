#!/usr/bin/env python3
"""Importa ZIP ufficiali Normattiva in un catalogo manifest con provenienza.
Uso: python scripts/indicizza_zip_normattiva.py percorso.zip
Non inventa metadati e non modifica i testi originali.
"""
import argparse, hashlib, json, pathlib, re, zipfile
ROOT=pathlib.Path(__file__).resolve().parents[1]
PAT=re.compile(r"^([^/]+)/([^/]+)$")
def main():
 p=argparse.ArgumentParser();p.add_argument("zipfile",type=pathlib.Path);p.add_argument("--max-files",type=int,default=200000);a=p.parse_args()
 sha=hashlib.sha256(a.zipfile.read_bytes()).hexdigest()
 out=ROOT/"dati"/"importazioni"/(sha[:16]+".jsonl");out.parent.mkdir(parents=True,exist_ok=True)
 total=0
 with zipfile.ZipFile(a.zipfile) as z, out.open("w",encoding="utf-8") as f:
  for entry in z.infolist():
   if entry.is_dir():continue
   if total>=a.max_files:raise ValueError("Limite file superato")
   if entry.file_size>100_000_000:raise ValueError("File interno troppo grande")
   path=pathlib.PurePosixPath(entry.filename)
   if path.is_absolute() or ".." in path.parts:raise ValueError("Percorso non sicuro")
   match=PAT.match(entry.filename)
   if not match:continue
   folder,name=match.groups()
   parts=folder.rsplit("_",2)
   if len(parts)!=3 or not re.fullmatch(r"\d{8}",parts[1]):continue
   record={"fonte":"Normattiva Open Data","archivio_sha256":sha,"percorso_archivio":entry.filename,"tipo_originale":parts[0],"data_emanazione":parts[1],"numero":parts[2],"nome_file":name,"dimensione_byte":entry.file_size,"crc32":entry.CRC}
   f.write(json.dumps(record,ensure_ascii=False)+"\n");total+=1
 print(json.dumps({"schede":total,"manifest":str(out),"archivio_sha256":sha}))
if __name__=="__main__":main()
