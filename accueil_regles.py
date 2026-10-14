"""
accueil_regles.py — Accueil, version 1 : un lecteur à RÈGLES, sans LLM, entièrement transparent.

Il transforme une phrase en (sujet, relation, objet) avec une CONFIANCE DE LECTURE, ou ne lit rien.
- Entités : il connaît les entités du monde (avantage déclaré : un graphe connaît ses entités) ; il tolère une faute
  de frappe (distance d'édition 1) au prix d'une confiance plus basse.
- Relation : le type des entités la détermine presque entièrement (année → naissance ; quartier → habite) ;
  la seule ambiguïté, personne + organisation, est tranchée par des mots-clés de direction ou d'emploi.
- Une rumeur (« il paraîtrait que ») ne change pas le fait lu : elle ne concerne pas la lecture mais la source.
Chaque lecture renvoie aussi ses RAISONS (quelles entités, quels mots-clés), pour rester une boîte de verre.
"""
import re
import unicodedata

DIRIGE = ["dirig", "direction", "à la tête", "a la tete", "tient les rênes", "tient les renes", "rênes", "patron",
          "patronne", "chef", "préside", "president", "présid", "aux commandes", "commande", "pilote", "gouvern",
          "manette", "numéro un", "numero un", "n°1", "aux manettes", "mène la barque", "tête de", "sa tête",
          "responsable", "dirigeante", "gérant", "gérante", "administr"]
MOTS_ENTIERS_DIRIGE = ["boss"]      # mots entiers seulement (« boss » oui, « bosse » non)
TRAVAILLE = ["travaill", "bosse", "boss pour", "salari", "employ", "personnel", "effectif", "embauch", "boulot",
             "taf", "équipe", "equipe", "fait partie", "recrue", "poste", "bureau", "collaborat", "émarge",
             "émargerait", "contrat", "rattach", "œuvre", "oeuvre", "turbin", "job", "staff", "travaux"]


def sans_accents(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn").lower()


def distance1(a, b):
    """Vrai si a et b diffèrent d'au plus une substitution, insertion, suppression ou interversion de deux lettres."""
    if a == b:
        return True
    if len(a) == len(b):
        d = [i for i in range(len(a)) if a[i] != b[i]]
        if len(d) == 2 and d[1] == d[0] + 1 and a[d[0]] == b[d[1]] and a[d[1]] == b[d[0]]:
            return True
    la, lb = len(a), len(b)
    if abs(la - lb) > 1:
        return False
    if la == lb:
        return sum(x != y for x, y in zip(a, b)) == 1
    if la > lb:
        a, b, la, lb = b, a, lb, la
    i = 0
    while i < la and a[i] == b[i]:
        i += 1
    return a[i:] == b[i + 1:]


class LecteurRegles:

    def __init__(self, personnes, orgs, quartiers):
        self.lex = [(p, "personne") for p in personnes] + [(o, "org") for o in orgs] + [(q, "quartier") for q in quartiers]

    def _entites(self, texte):
        """Entités reconnues : d'abord les correspondances exactes (les plus longues d'abord), puis, sur les mots
        restants seulement, les fautes tolérées (noms d'au moins 5 lettres par mot)."""
        jetons = [(m.start(), m.end(), sans_accents(m.group())) for m in re.finditer(r"[A-Za-zÀ-ÿ-]+", texte)]  # l'apostrophe sépare (élisions)
        pris, trouve = set(), []
        for nom, typ in sorted(self.lex, key=lambda x: -len(x[0])):        # exactes
            parties = sans_accents(nom).split()
            n = len(parties)
            for i in range(len(jetons) - n + 1):
                if any(j in pris for j in range(i, i + n)):
                    continue
                if [t[2] for t in jetons[i:i + n]] == parties:
                    pris.update(range(i, i + n)); trouve.append((jetons[i][0], nom, typ, 1.0)); break
        for nom, typ in sorted(self.lex, key=lambda x: -len(x[0])):        # fautes tolérées
            if any(t[1] == nom for t in trouve):
                continue
            parties = sans_accents(nom).split()
            n = len(parties)
            if min(len(p) for p in parties) < 5 and n == 1:
                continue
            for i in range(len(jetons) - n + 1):
                if any(j in pris for j in range(i, i + n)):
                    continue
                fen = [t[2] for t in jetons[i:i + n]]
                ecarts = [f != p for f, p in zip(fen, parties)]
                if sum(ecarts) == 1 and all(distance1(f, p) for f, p in zip(fen, parties)) \
                        and all(len(p) >= 5 for p, e in zip(parties, ecarts) if e):
                    pris.update(range(i, i + n)); trouve.append((jetons[i][0], nom, typ, 0.8)); break
        return trouve

    def lire(self, texte):
        bas = sans_accents(texte)
        ents = self._entites(texte)
        annee = re.search(r"\b(1[89]\d\d|20\d\d)\b", texte)
        pers = [e for e in ents if e[2] == "personne"]
        orgs = [e for e in ents if e[2] == "org"]
        quart = [e for e in ents if e[2] == "quartier"]
        raisons = [f"{e[1]} ({e[2]}{', faute tolérée' if e[3] < 1 else ''})" for e in ents]
        if annee and len(pers) == 1:
            return (pers[0][1], "naissance", annee.group(1), pers[0][3]), raisons + [f"année {annee.group(1)}"]
        if quart and len(pers) == 1 and len(quart) == 1:
            return (pers[0][1], "habite", quart[0][1], pers[0][3] * quart[0][3]), raisons + ["quartier → habite"]
        if len(pers) == 1 and len(orgs) == 1:
            d = [k for k in DIRIGE if re.search(r"(^|\W)" + re.escape(sans_accents(k)), bas)]
            d += [k for k in MOTS_ENTIERS_DIRIGE if re.search(r"(^|\W)" + k + r"(\W|$)", bas)]
            w = [k for k in TRAVAILLE if re.search(r"(^|\W)" + re.escape(sans_accents(k)), bas)]
            q = pers[0][3] * orgs[0][3]
            if d and not w:
                return (orgs[0][1], "dirige", pers[0][1], q), raisons + [f"mots de direction : {d}"]
            if w and not d:
                return (pers[0][1], "travaille", orgs[0][1], q), raisons + [f"mots d'emploi : {w}"]
            if d and w:
                return (orgs[0][1], "dirige", pers[0][1], 0.5 * q), raisons + [f"ambigu : direction {d} et emploi {w}"]
            return (pers[0][1], "travaille", orgs[0][1], 0.5 * q), raisons + ["aucun mot-clé : emploi par défaut"]
        return None, raisons + ["entités insuffisantes ou ambiguës : rien lu"]
