import json, os, urllib.request

URL = "https://shoppen.brondby.com/products/udebanetroje-l-s-26-27.js"
SIDE = "https://shoppen.brondby.com/products/udebanetroje-l-s-26-27"
TOPIC = os.environ["NTFY_TOPIC"]
STR = os.environ.get("STOERRELSE", "L").strip().upper() or "L"

req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0"})
data = json.load(urllib.request.urlopen(req, timeout=20))
v = next(v for v in data["variants"] if v["title"].strip().upper() == STR)
print(f"{STR} på lager:", v["available"])

if v["available"]:
    tekst = f"Størrelse {STR} er på lager!"
    if STR != "L":
        tekst = "TEST: " + tekst
    urllib.request.urlopen(urllib.request.Request(
        f"https://ntfy.sh/{TOPIC}", data=tekst.encode(),
        headers={"Title": "Brondby-troje", "Click": SIDE, "Priority": "high"}), timeout=15)
