"""
cache.py — un cache qui ne peut pas mentir sur sa provenance.

Le répertoire de cache porte l'empreinte (SHA-256) du code source de TOUS les fichiers dont dépend un
résultat, et du script appelant. Si un seul de ces fichiers change, le cache change : un résultat
écrit par un ancien code ne peut plus être relu par un nouveau.
"""
import hashlib
import os
import sys

DEPENDANCES = ["monde.py", "temoins.py", "evaluer.py", "pesee.py", "filiation.py",
               "soupcon.py", "meprise.py", "litige.py", "echelle.py", "cache.py"]


def empreinte(script=None):
    ici = os.path.dirname(os.path.abspath(__file__))
    h = hashlib.sha256()
    for f in DEPENDANCES + ([os.path.basename(script)] if script else []):
        chemin = os.path.join(ici, f)
        if os.path.exists(chemin):
            h.update(f.encode())
            h.update(open(chemin, "rb").read())
    return h.hexdigest()[:12]


def repertoire(nom):
    script = sys.argv[0] if sys.argv and sys.argv[0].endswith(".py") else None
    d = f"/tmp/cache_{nom}_{empreinte(script)}"
    os.makedirs(d, exist_ok=True)
    return d
