#!/usr/bin/env python3
"""Importa metadati JSONL verificati, senza inventare testi normativi."""
import argparse
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
TIPI = {"leggi-ordinarie", "decreti-legge", "decreti-legislativi", "dpr", "dpcm", "leggi-regionali", "regolamenti-regionali", "statuti"}

def slug(value):
    return re.sub(r"[^a-z0-9-]+", "-", str(value).lower()).strip("-")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("jsonl", type=pathlib.Path)
    args = parser.parse_args()
    count = 0
    for line in args.jsonl.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        record = json.loads(line)
        kind = record["tipo"]
        year = int(record["anno"])
        number = str(record["numero"])
        source = record["fonte_url"]
        if kind not in TIPI or not source.startswith("https://"):
            raise ValueError("Tipo o fonte non validi")
        if record.get("regione"):
            base = ROOT / "regioni" / slug(record["regione"]) / kind
        else:
            base = ROOT / "nazionale" / kind
        if not base.is_dir():
            raise ValueError(f"Percorso non previsto: {base}")
        destination = base / str(year) / (slug(number) + ".json")
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        count += 1
    print(f"Importati {count} record; nessun testo normativo scaricato.")

if __name__ == "__main__":
    main()
