#!/usr/bin/env python3
"""Importa automaticamente metadati da una collezione predefinita Normattiva.
Scarica ZIP ufficiale e indicizza nomi degli atti; non dichiara testi completi.
"""
import datetime, hashlib, io, json, os, pathlib, re, urllib.parse, urllib.request, zipfile
ROOT=pathlib.Path(__file__).resolve().parents[1]
BASE="https://api.normattiva.it/t/normattiva.api/bff-opendata/v1/api/v1/collections"
def request(url,limit):
 req=urllib.request.Request(url,headers={"Accept":"application/json, application/zip, */*","User-Agent":"LegislazioneItaliana/0.3"})
 with urllib.request.urlopen(req,timeout=120) as response:
  body=response.read(limit+1)
  if len(body)>limit: raise RuntimeError("Archivio oltre limite configurato")
  return body
def main():
 max_bytes=int(os.environ.get("MAX_DOWNLOAD_MB","80"))*1024*1024
 catalog=json.loads(request(BASE+"/collection-predefinite",5_000_000))
 if not isinstance(catalog,list):raise RuntimeError("Catalogo API inatteso")
 choices=[x.get("nomeCollezione") for x in catalog if isinstance(x,dict) and isinstance(x.get("nomeCollezione"),str)]
 wanted=os.environ.get("COLLECTION_NAME","Codici")
 if wanted not in choices:raise RuntimeError("Collezione non disponibile: "+wanted+"; disponibili: "+", ".join(choices[:30]))
 params=urllib.parse.urlencode({"nome":wanted,"formato":"JSON","formatoRichiesta":"O"})
 url=BASE+"/download/collection-preconfezionata?"+params
 data=request(url,max_bytes)
 if not zipfile.is_zipfile(io.BytesIO(data)):raise RuntimeError("Risposta non ZIP: non importata")
 digest=hashlib.sha256(data).hexdigest()
 manifest=[]
 with zipfile.ZipFile(io.BytesIO(data)) as archive:
  for item in archive.infolist():
   if item.is_dir():continue
   path=pathlib.PurePosixPath(item.filename)
   if path.is_absolute() or ".." in path.parts or item.file_size>50_000_000:raise RuntimeError("Elemento ZIP non sicuro")
   parts=path.parts
   if len(parts)<2:continue
   match=re.fullmatch(r"(.+)_([0-9]{8})_([^/]+)",parts[0])
   if not match:continue
   kind,date,number=match.groups()
   manifest.append({"tipo_originale":kind,"data_emanazione":date,"numero":number,"file_originale":item.filename,"byte":item.file_size,"crc32":item.CRC,"archivio_sha256":digest,"fonte":url})
 out=ROOT/"dati"/"importazioni"/"normattiva-codici.json"
 out.parent.mkdir(parents=True,exist_ok=True)
 out.write_text(json.dumps({"collezione":wanted,"acquisizione_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"numero_file":len(manifest),"atti":manifest},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 print("File indicizzati:",len(manifest))
if __name__=="__main__":main()
