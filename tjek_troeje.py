#!/usr/bin/env python3
"""Overvåger om Brøndby udebanetrøje 26/27 bliver tilgængelig i størrelse L.
Giver en macOS-notifikation (og evt. push via ntfy) når L skifter til "på lager"."""
import json, os, sys, subprocess, urllib.request, datetime

URL = "https://shoppen.brondby.com/products/udebanetroje-l-s-26-27.js"
PRODUKT_SIDE = "https://shoppen.brondby.com/products/udebanetroje-l-s-26-27"
TEST = len(sys.argv) > 1  # test: python3 tjek_troeje.py S
STOERRELSE = sys.argv[1].upper() if TEST else "L"
NTFY_TOPIC = "broendby-troeje-a5ec160028"  # valgfrit: skriv et hemmeligt emnenavn, fx "mathias-broendby-xyz123", og installér ntfy-appen på iPhone

mappe = os.path.dirname(os.path.abspath(__file__))
state_fil = os.path.join(mappe, "sidste_status.txt")
log_fil = os.path.join(mappe, "log.txt")

def log(tekst):
    with open(log_fil, "a") as f:
        f.write(f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S}  {tekst}\n")

def notificer(tekst):
    subprocess.run(["osascript", "-e",
        f'display notification "{tekst}" with title "Brøndby-trøje" sound name "Glass"'])
    subprocess.run(["open", PRODUKT_SIDE])
    if NTFY_TOPIC:
        req = urllib.request.Request(f"https://ntfy.sh/{NTFY_TOPIC}", data=tekst.encode(),
                                     headers={"Title": "Brondby-troje", "Click": PRODUKT_SIDE})
        urllib.request.urlopen(req, timeout=15)

try:
    req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0"})
    data = json.load(urllib.request.urlopen(req, timeout=20))
    status = next(v["available"] for v in data["variants"]
                  if v["title"].strip().upper() == STOERRELSE or STOERRELSE in v.get("option1", "").upper().split())
except Exception as e:
    log(f"FEJL: {e}")
    raise SystemExit(1)

if TEST:
    print(f"Størrelse {STOERRELSE} på lager: {status}")
    if status:
        notificer(f"TEST: størrelse {STOERRELSE} er på lager!")
    raise SystemExit(0)

forrige = open(state_fil).read().strip() if os.path.exists(state_fil) else "False"
open(state_fil, "w").write(str(status))
log(f"Størrelse {STOERRELSE} på lager: {status}")

if status and forrige != "True":
    notificer(f"Størrelse {STOERRELSE} er nu på lager!")
