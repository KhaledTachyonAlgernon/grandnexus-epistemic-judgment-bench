"""Étape 2 — collecte des infobox (extracteur FIGÉ : il lit un champ, ne connaît aucun nom). Reprise automatique."""
import json, os, re, sys, time, urllib.request, urllib.parse
from concurrent.futures import ThreadPoolExecutor

UA = {"User-Agent": "GrandNexusBanc/0.1 (etude; contact via claude.ai)"}
CLES = {"fr": "maire", "de": "maire", "en": "mayor", "es": "dirigentes_nombres", "it": "Amministratore locale"}
MOIS = [f"{a}-{m:02d}-01" for a in (2019, 2020, 2021) for m in range(1, 13) if (2019, 7) <= (a, m) <= (2021, 6)]
FIC = "reel_brut.json"


def extraire(txt, lang):
    m = re.search(r"^\s*\|\s*" + re.escape(CLES[lang]) + r"\s*=\s*(.*)$", txt, re.M | re.I)
    if not m:
        return None
    v = m.group(1)
    v = re.split(r"<br\s*/?>|\n", v, flags=re.I)[0]
    v = re.sub(r"<ref[^>]*/>|<ref.*?</ref>|<ref.*$", "", v, flags=re.I)
    v = re.sub(r"\[\[(?:[^\]|]*\|)?([^\]]*)\]\]", r"\1", v)
    v = re.sub(r"\{\{[^{}]*\}\}|<[^>]+>|\([^)]*\)|''+", "", v)
    v = " ".join(v.replace("&nbsp;", " ").split()).strip(" ,;-–")
    return v or None


def lire(qid, lang, titre, mois):
    url = (f"https://{lang}.wikipedia.org/w/api.php?action=query&prop=revisions&titles={urllib.parse.quote(titre)}"
           f"&rvlimit=1&rvstart={mois}T00:00:00Z&rvdir=older&rvprop=timestamp|content&rvslots=main&rvsection=0&format=json&formatversion=2")
    for essai in range(4):
        try:
            r = json.loads(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40).read())
            p = r["query"]["pages"][0]
            if "revisions" not in p:
                return [qid, lang, mois, None, "pas de révision"]
            rev = p["revisions"][0]
            return [qid, lang, mois, extraire(rev["slots"]["main"].get("content", ""), lang), rev["timestamp"]]
        except Exception as e:
            time.sleep(2 + 3 * essai)
    return [qid, lang, mois, None, "ERREUR"]


if __name__ == "__main__":
    budget = time.time() + float(sys.argv[1] if len(sys.argv) > 1 else 240)
    C = json.load(open("reel_communes.json"))
    fait = json.load(open(FIC)) if os.path.exists(FIC) else []
    vus = {(x[0], x[1], x[2]) for x in fait if x[4] != "ERREUR"}
    fait = [x for x in fait if x[4] != "ERREUR"]
    taches = [(c["qid"], l, c["titres"][l], m) for c in C for l in CLES if l in c["titres"] for m in MOIS if (c["qid"], l, m) not in vus]
    print("à faire :", len(taches))
    with ThreadPoolExecutor(6) as ex:
        for k in range(0, len(taches), 120):
            if time.time() > budget:
                break
            fait += list(ex.map(lambda t: lire(*t), taches[k:k + 120]))
            json.dump(fait, open(FIC, "w"), ensure_ascii=False)
    print("collectées :", len(fait), "| erreurs dans la dernière passe :", sum(1 for x in fait if x[4] == "ERREUR"))
