"""
accueil_paragraphes.py — Accueil, version 1 bis : un lecteur de PARAGRAPHES à règles, sans LLM.

Principes (génériques, écrits avant de regarder la moitié de test) :
- chaque valeur typée (quartier → habite, année → naissance, organisation → travaille ou dirige) devient un fait ;
- son SUJET est la personne la plus proche avant elle dans la phrase (nom complet, nom partiel déjà rencontré dans le
  paragraphe, ou pronom il/elle/lui renvoyant à la personne « en focus ») ; à défaut, la plus proche après ; à défaut,
  la personne en focus ;
- pour un même sujet et une même relation, la DERNIÈRE valeur énoncée l'emporte : c'est ainsi que s'exprime une correction ;
- aucune détection des personnes INCONNUES du graphe : c'est la limite d'un lecteur qui ne connaît que ses entités.
Chaque fait lu porte une confiance de lecture et ses raisons.
"""
import re

from accueil_regles import LecteurRegles, DIRIGE, MOTS_ENTIERS_DIRIGE, sans_accents, distance1

PRONOMS = r"\b(il|elle|lui|cette personne|celui-ci|celle-ci|ce dernier|cette derniere)\b"
DESCRIPTION = r"\b(le|la|ce|cette|l'|un|une)\s*(salarie|salariee|employe|employee|patron|patronne|dirigeant|dirigeante|directeur|directrice|responsable|chef)\s+(de|chez|du)\s+(la\s+)?"
MOTS_COURANTS = {"le", "la", "les", "un", "une", "pour", "dans", "selon", "chez", "non", "mais", "et", "il", "elle", "cette",
                 "ce", "on", "je", "quant", "du", "de", "des", "cote", "a", "au", "aux", "sa", "son", "ses", "leur", "en",
                 "c", "d", "l", "j", "qu", "s", "apres", "avant", "depuis", "ainsi", "donc", "puis", "enfin", "oui"}


class LecteurParagraphes:

    def __init__(self, personnes, orgs, quartiers):
        self.base = LecteurRegles(personnes, orgs, quartiers)
        self.personnes = personnes

    def _entites(self, phrase):
        """Comme le lecteur de phrases, mais TOUTES les occurrences d'un nom sont repérées (une correction répète le nom)."""
        jetons = [(m.start(), sans_accents(m.group())) for m in re.finditer(r"[A-Za-zÀ-ÿ-]+", phrase)]
        pris, trouve = set(), []
        for exact in (True, False):
            for nom, typ in sorted(self.base.lex, key=lambda x: -len(x[0])):
                parties = sans_accents(nom).split()
                n = len(parties)
                if not exact and n == 1 and len(parties[0]) < 5:
                    continue
                for i in range(len(jetons) - n + 1):
                    if any(j in pris for j in range(i, i + n)):
                        continue
                    fen = [t[1] for t in jetons[i:i + n]]
                    if exact and fen == parties:
                        pris.update(range(i, i + n)); trouve.append((jetons[i][0], nom, typ, 1.0))
                    elif not exact:
                        ecarts = [f != p for f, p in zip(fen, parties)]
                        if sum(ecarts) == 1 and all(distance1(f, p) for f, p in zip(fen, parties)) \
                                and all(len(p) >= 5 for p, e in zip(parties, ecarts) if e):
                            pris.update(range(i, i + n)); trouve.append((jetons[i][0], nom, typ, 0.8))
        return trouve

    def _direction(self, segment):
        b = sans_accents(segment)
        return any(re.search(r"(^|\W)" + re.escape(sans_accents(k)), b) for k in DIRIGE) or \
            any(re.search(r"(^|\W)" + k + r"(\W|$)", b) for k in MOTS_ENTIERS_DIRIGE)

    def lire(self, texte):
        faits, focus, vus = [], None, []
        for phrase in re.split(r"(?<=[.!?;])\s+", texte):
            b = sans_accents(phrase)
            ments = []                                                   # (position, genre, valeur, qualité)
            descr_orgs = set()
            for pos, nom, typ, q in self._entites(phrase):
                ments.append((pos, typ, nom, q))
            for m in re.finditer(DESCRIPTION, b):                       # « le salarié de Maison X » → personne liée à X
                apres = [x for x in ments if x[1] == "org" and m.end() <= x[0] <= m.end() + 3]
                if apres:
                    org = apres[0][2]
                    lies = [f[0] for f in faits if f[1] == "travaille" and f[2] == org] + \
                           [f[2] for f in faits if f[1] == "dirige" and f[0] == org]
                    if lies:                                            # sinon l'organisation redevient un fait ordinaire
                        descr_orgs.add(apres[0][0])
                        ments.append((m.start(), "personne", lies[-1], 0.8))
            pris = [(p, p + len(n)) for p, t, n, _ in ments if t in ("personne", "org", "quartier")]
            for m in re.finditer(r"\b(1[89]\d\d|20\d\d)\b", phrase):
                ments.append((m.start(), "annee", m.group(1), 1.0))
            jetons = list(re.finditer(r"[A-Za-zÀ-ÿ-]+", phrase))
            for k in range(len(jetons) - 1):                              # barrière : un nom propre INCONNU est quelqu'un d'autre
                t1, t2 = jetons[k], jetons[k + 1]
                if any(a_ <= t1.start() < b_ for a_, b_ in pris) or any(a_ <= t2.start() < b_ for a_, b_ in pris):
                    continue
                if t1.group()[0].isupper() and t2.group()[0].isupper() and phrase[t1.end():t2.start()] == " " \
                        and sans_accents(t1.group()) not in MOTS_COURANTS and len(t1.group()) >= 3 and len(t2.group()) >= 3:
                    ments.append((t1.start(), "inconnu", t1.group() + " " + t2.group(), 0.0))
                    pris.append((t1.start(), t2.end()))
            for m in jetons:                                              # noms partiels déjà rencontrés (même phrase comprise)
                if any(a_ <= m.start() < b_ for a_, b_ in pris):
                    continue
                w = sans_accents(m.group())
                connus = vus + [x[2] for x in ments if x[1] == "personne" and x[3] == 1.0 and x[0] < m.start()]
                cand = sorted({p for p in connus if w in sans_accents(p).split()})
                if len(cand) == 1 and len(w) >= 3:
                    ments.append((m.start(), "personne", cand[0], 0.8))
            for m in re.finditer(PRONOMS, b):
                ments.append((m.start(), "pronom", None, 0.8))
            ments.sort(key=lambda x: (x[0], x[1]))
            res = []                                                      # les pronoms renvoient à la personne la plus proche avant
            for pos, typ, val, q in ments:
                if typ == "pronom":
                    prec = [x for x in res if x[1] in ("personne", "inconnu")]
                    cible = prec[-1] if prec else (None if focus is None else (pos, "personne", focus, 0.8))
                    if cible:
                        res.append((pos, cible[1], cible[2], 0.8))
                else:
                    res.append((pos, typ, val, q))
            ments = res
            for i, (pos, typ, val, q) in enumerate(ments):
                if typ == "personne" and q == 1.0 and val not in vus:
                    vus.append(val)
                if typ not in ("quartier", "annee", "org") or (typ == "org" and pos in descr_orgs):
                    continue
                avant = [m for m in ments[:i] if m[1] in ("personne", "inconnu")]
                apres = [m for m in ments[i + 1:] if m[1] in ("personne", "inconnu")]
                if avant:
                    suj, qs, d, g = avant[-1][2], avant[-1][3], "personne précédente", avant[-1][1]
                elif apres:
                    suj, qs, d, g = apres[0][2], apres[0][3], "personne suivante", apres[0][1]
                elif focus:
                    suj, qs, d, g = focus, 0.8, "personne en focus", "personne"
                else:
                    continue
                if g == "inconnu":                                         # on ne lit rien sur un inconnu
                    focus = None
                    continue
                debut = avant[-1][0] if avant else 0
                if typ == "quartier":
                    faits.append([suj, "habite", val, q * qs, d])
                elif typ == "annee":
                    faits.append([suj, "naissance", val, q * qs, d])
                else:
                    seg = phrase[debut:pos + len(val) + 40]
                    if self._direction(seg):
                        faits.append([val, "dirige", suj, q * qs, d + " ; mot de direction"])
                    else:
                        faits.append([suj, "travaille", val, q * qs, d])
                focus = suj
            pleines = [m for m in ments if m[1] in ("personne", "inconnu") and m[3] in (1.0, 0.0)]
            if pleines:
                focus = pleines[-1][2] if pleines[-1][1] == "personne" else None
        final = {}
        for s_, r, o, c, d in faits:                                     # la dernière valeur l'emporte
            k = (s_, r)
            if k in final and final[k][0] != o:
                final[k] = (o, min(c, 0.7), d + " ; valeur corrigée (dernière énoncée)")
            else:
                final[k] = (o, c, d)
        return [(s_, r, o, c, d) for (s_, r), (o, c, d) in final.items()]
