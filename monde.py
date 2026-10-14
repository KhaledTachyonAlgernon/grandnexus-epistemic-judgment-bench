"""
monde.py — un monde synthétique pour évaluer un organe de jugement.

Vérité contrôlée. Faits qui changent avec le temps. Sources de fiabilité et de
fraîcheur inégales. Questions à réponse connue (ou sans réponse).
Aucun modèle ne peut connaître ces faits à l'avance : tout est inventé.
"""
import random
from dataclasses import dataclass


@dataclass(frozen=True)
class Source:
    nom: str
    fiabilite: float    # probabilité de rapporter la valeur vraie (à sa date)
    retard: int         # nombre d'époques de retard de ses informations
    couverture: float   # part des faits rapportés à chaque époque
    copie: str = None   # nom de la source recopiée (erreurs comprises), le cas échéant
    taux_copie: float = 0.0
    par_sujet: tuple = ()  # ((relation, fiabilité), ...) : fiabilité qui dépend du sujet
    cibles: float = 0.0    # part des faits sur lesquels la source ment, toujours de la même façon
    complice: str = None   # nom du menteur dont la source répète les mensonges, SUR SES CIBLES SEULEMENT

    def f(self, relation):
        return dict(self.par_sujet).get(relation, self.fiabilite)


@dataclass(frozen=True)
class Enonce:
    id: int
    epoque: int
    source: str
    sujet: str
    relation: str
    objet: str
    texte: str


@dataclass(frozen=True)
class Question:
    id: int
    type: str           # actuel | historique | deux_sauts | sans_reponse
    sujet: str
    chaine: tuple       # relations à suivre depuis le sujet
    epoque: int
    texte: str
    attendu: object     # None = la bonne réponse est « inconnu »
    grappe: tuple = ()  # le fait qui décide de la réponse : unité de preuve statistique


@dataclass
class Monde:
    enonces: list
    questions: list
    verite: dict
    sources: list
    n_epoques: int
    domaines: dict      # relation -> valeurs possibles (réservé au plafond)
    taux: dict          # relation -> probabilité de changement par époque (idem)
    sosie: dict = None  # relation -> {valeur: valeur avec laquelle on la confond} (idem)
    p_sosie: float = 0.0
    menteur: tuple = None  # (nom, part ciblée, faits ciblés) — les cibles ne servent qu'à l'analyse
    coalition: tuple = None  # sources qui mentent ensemble sur les cibles (réservé au plafond)
    contraintes: bool = False  # vérité cohérente : qui dirige une organisation y travaille


RELATIONS = {"habite": "quartier", "travaille": "org", "dirige": "personne", "naissance": "annee"}
SUJET_DE = {"habite": "personne", "travaille": "personne", "dirige": "org", "naissance": "personne"}
MOBILITE = {"habite": 1.0, "travaille": 1.0, "dirige": 0.5, "naissance": 0.0}

GABARITS = {
    "habite":    ["{s} habite à {o}.", "{s} vit dans le quartier {o}.", "On signale que {s} réside à {o}."],
    "travaille": ["{s} travaille pour {o}.", "{s} est employé chez {o}.", "{o} compte {s} parmi ses salariés."],
    "dirige":    ["{s} est dirigée par {o}.", "La direction de {s} est assurée par {o}.", "{o} est à la tête de {s}."],
    "naissance": ["{s} est né en {o}.", "{s} a vu le jour en {o}."],
}
QUESTIONS = {
    "habite":    "Où habite {s} {t} ?",
    "travaille": "Pour quelle organisation travaille {s} {t} ?",
    "dirige":    "Qui dirige {s} {t} ?",
    "naissance": "En quelle année est né {s} ?",
}

PRESETS = {
    # tout le monde est fiable et à jour : un témoin naïf doit presque réussir
    "facile": dict(changement=0.08, sources=[
        Source("Le Registre", 0.97, 0, 0.35),
        Source("La Gazette", 0.95, 0, 0.35),
        Source("Radio Quartier", 0.90, 0, 0.30)]),
    # mélange réaliste : une source en retard, une source bavarde et médiocre
    "realiste": dict(changement=0.12, sources=[
        Source("Le Registre", 0.95, 0, 0.25),
        Source("La Gazette", 0.85, 1, 0.35),
        Source("Radio Quartier", 0.70, 0, 0.40),
        Source("Le Forum", 0.50, 0, 0.40)]),
    # piège à majorité : les sources les plus prolifiques sont périmées ou peu fiables
    "hostile": dict(changement=0.15, sources=[
        Source("Le Registre", 0.95, 0, 0.15),
        Source("L'Almanach", 0.90, 3, 0.50),
        Source("Le Forum", 0.45, 0, 0.60),
        Source("La Gazette", 0.80, 1, 0.25)]),
    # chambre d'écho : une origine médiocre, recopiée par trois sources ; les erreurs ne sont
    # plus indépendantes (les sources d'origine doivent précéder leurs copies dans la liste)
    "echo": dict(changement=0.12, sources=[
        Source("Le Registre", 0.95, 0, 0.20),
        Source("La Gazette", 0.85, 0, 0.20),
        Source("La Dépêche", 0.55, 0, 0.45),
        Source("Le Relais", 0.90, 0, 0.35, "La Dépêche", 0.8),
        Source("L'Écho", 0.90, 0, 0.35, "La Dépêche", 0.8),
        Source("Le Miroir", 0.90, 0, 0.30, "La Dépêche", 0.7)]),
    # erreurs plausibles : on se trompe vers le « sosie » de la vérité, pas au hasard
    # fiabilité par sujet : chaque source est bonne sur certains sujets, mauvaise sur d'autres
    "thematique": dict(changement=0.12, sources=[
        Source("Le Registre", 0.85, 0, 0.30, par_sujet=(("habite", .95), ("travaille", .95), ("dirige", .55), ("naissance", .95))),
        Source("La Gazette", 0.74, 0, 0.30, par_sujet=(("habite", .55), ("travaille", .85), ("dirige", .95), ("naissance", .60))),
        Source("Radio Quartier", 0.71, 0, 0.30, par_sujet=(("habite", .85), ("travaille", .60), ("dirige", .60), ("naissance", .80))),
        Source("Le Forum", 0.65, 0, 0.30)]),
    # même casse, preuves rares : les poids ont enfin du levier
    "thematique_rare": dict(changement=0.12, sources=[
        Source("Le Registre", 0.85, 0, 0.10, par_sujet=(("habite", .95), ("travaille", .95), ("dirige", .55), ("naissance", .95))),
        Source("La Gazette", 0.74, 0, 0.10, par_sujet=(("habite", .55), ("travaille", .85), ("dirige", .95), ("naissance", .60))),
        Source("Radio Quartier", 0.71, 0, 0.10, par_sujet=(("habite", .85), ("travaille", .60), ("dirige", .60), ("naissance", .80))),
        Source("Le Forum", 0.65, 0, 0.10)]),
    # menteur stratégique : excellent partout, sauf sur quelques faits où il ment avec constance
    "menteur": dict(changement=0.12, sources=[
        Source("Le Registre", 0.90, 0, 0.25),
        Source("La Gazette", 0.80, 0, 0.25),
        Source("Radio Quartier", 0.70, 0, 0.30),
        Source("Le Notable", 0.95, 0, 0.40, cibles=0.15)]),
    # interaction : le menteur stratégique, recopié par une chambre d'écho
    "echo_menteur": dict(changement=0.12, sources=[
        Source("Le Registre", 0.90, 0, 0.25),
        Source("La Gazette", 0.80, 0, 0.25),
        Source("Le Notable", 0.95, 0, 0.40, cibles=0.15),
        Source("Le Relais", 0.90, 0, 0.35, "Le Notable", 0.8),
        Source("L'Écho", 0.90, 0, 0.35, "Le Notable", 0.8)]),
    # coordination : des complices qui répètent le mensonge sur les cibles, et sont honnêtes ailleurs
    "complice": dict(changement=0.12, sources=[
        Source("Le Registre", 0.90, 0, 0.25),
        Source("La Gazette", 0.80, 0, 0.25),
        Source("Le Notable", 0.95, 0, 0.40, cibles=0.15),
        Source("Le Relais", 0.90, 0, 0.35, complice="Le Notable"),
        Source("L'Écho", 0.90, 0, 0.35, complice="Le Notable")]),
    # monde à contraintes : la vérité respecte « qui dirige une organisation y travaille »
    "contraintes_honnete": dict(changement=0.12, contraintes=True, sources=[
        Source("Le Registre", 0.90, 0, 0.25),
        Source("La Gazette", 0.80, 0, 0.25),
        Source("Radio Quartier", 0.70, 0, 0.30),
        Source("Le Forum", 0.65, 0, 0.30)]),
    "contraintes_complice": dict(changement=0.12, contraintes=True, sources=[
        Source("Le Registre", 0.90, 0, 0.25),
        Source("La Gazette", 0.80, 0, 0.25),
        Source("Le Notable", 0.95, 0, 0.40, cibles=0.15),
        Source("Le Relais", 0.90, 0, 0.35, complice="Le Notable"),
        Source("L'Écho", 0.90, 0, 0.35, complice="Le Notable")]),
    # mixte : coalition coordonnée ET erreurs plausibles chez toutes les sources
    "mixte": dict(changement=0.12, p_sosie=0.7, sources=[
        Source("Le Registre", 0.90, 0, 0.25),
        Source("La Gazette", 0.80, 0, 0.25),
        Source("Le Notable", 0.95, 0, 0.40, cibles=0.15),
        Source("Le Relais", 0.90, 0, 0.35, complice="Le Notable"),
        Source("L'Écho", 0.90, 0, 0.35, complice="Le Notable")]),
    "plausible": dict(changement=0.12, p_sosie=0.7, sources=[
        Source("Le Registre", 0.90, 0, 0.25),
        Source("La Gazette", 0.80, 0, 0.30),
        Source("Radio Quartier", 0.70, 0, 0.35),
        Source("Le Forum", 0.60, 0, 0.35)]),
}

_SYLL = ["ka", "lo", "mi", "ra", "tu", "ven", "sor", "bel", "ni", "dra",
         "gor", "pha", "li", "zen", "mo", "ri", "ta", "quil", "es", "or"]


def generer(preset="realiste", graine=0, n_personnes=80, n_orgs=24,
            n_quartiers=6, n_epoques=12, n_questions=1200):
    rng = random.Random(graine)
    cfg = PRESETS[preset]
    pris = set()

    def frais(k):
        while True:
            x = "".join(rng.choice(_SYLL) for _ in range(k)).capitalize()
            if x not in pris:
                pris.add(x)
                return x

    personnes = [f"{frais(2)} {frais(3)}" for _ in range(n_personnes)]
    orgs = [f"Maison {frais(3)}" for _ in range(n_orgs)]
    quartiers = [frais(2) for _ in range(n_quartiers)]
    domaines = {"quartier": quartiers, "org": orgs, "personne": personnes,
                "annee": [str(a) for a in range(1950, 2006)]}
    sujets = {"personne": personnes, "org": orgs}

    # — vérité : une valeur par (sujet, relation) et par époque —
    verite = {}
    for r, typ in SUJET_DE.items():
        dom = domaines[RELATIONS[r]]
        for s in sujets[typ]:
            v, serie = rng.choice(dom), []
            for t in range(n_epoques):
                if t > 0 and rng.random() < cfg["changement"] * MOBILITE[r]:
                    v = rng.choice([x for x in dom if x != v])
                serie.append(v)
            verite[(s, r)] = serie

    # — contraintes (seulement si le monde le demande : les autres mondes restent identiques) —
    if cfg.get("contraintes"):
        p_dir, p_tr = cfg["changement"] * MOBILITE["dirige"], cfg["changement"] * MOBILITE["travaille"]
        chef = dict(zip(orgs, rng.sample(personnes, len(orgs))))
        poste = {p: rng.choice(orgs) for p in personnes}
        for o_, p in chef.items():
            poste[p] = o_
        D, W = {o_: [] for o_ in orgs}, {p: [] for p in personnes}
        for t in range(n_epoques):
            if t > 0:
                dirigeants = set(chef.values())
                for o_ in orgs:
                    if rng.random() < p_dir:
                        nouveau = rng.choice([p for p in personnes if p not in dirigeants])
                        dirigeants.discard(chef[o_]); dirigeants.add(nouveau)
                        chef[o_], poste[nouveau] = nouveau, o_
                for p in personnes:
                    if p not in dirigeants and rng.random() < p_tr:
                        poste[p] = rng.choice([x for x in orgs if x != poste[p]])
            for o_ in orgs:
                D[o_].append(chef[o_])
            for p in personnes:
                W[p].append(poste[p])
        for o_ in orgs:
            verite[(o_, "dirige")] = D[o_]
        for p in personnes:
            verite[(p, "travaille")] = W[p]

    # — sosies (seulement si le monde le demande : les autres mondes restent identiques) —
    p_sosie, sosie = cfg.get("p_sosie", 0.0), {}
    if p_sosie:
        for r, typ in RELATIONS.items():
            dom = domaines[typ]
            sosie[r] = {v: rng.choice([x for x in dom if x != v]) for v in dom}

    # — mensonges ciblés (seulement si une source en porte) —
    cibles, mensonge, menteur = set(), {}, None
    for src in cfg["sources"]:
        if src.cibles:
            for (s, r), serie in verite.items():
                if r in ("habite", "travaille", "dirige") and rng.random() < src.cibles:
                    cibles.add((s, r))
                    mensonge[(s, r)] = rng.choice([x for x in domaines[RELATIONS[r]] if x != serie[0]])
            menteur = (src.nom, src.cibles, frozenset(cibles))

    # — personnes discrètes : présentes dans le monde, mais jamais localisées —
    discretes = set(rng.sample(personnes, max(1, n_personnes // 6)))

    # — énoncés : ce que les sources disent, avec leurs défauts —
    enonces, dernier = [], {}             # dernier[(source, sujet, relation)] = objet affirmé
    for t in range(n_epoques):
        for src in cfg["sources"]:
            for (s, r), serie in verite.items():
                if rng.random() >= src.couverture:
                    continue
                if r == "habite" and s in discretes:
                    continue
                vrai = serie[max(0, t - src.retard)]
                origine = (src.copie, s, r)
                if (src.cibles or src.complice) and (s, r) in cibles:
                    o = mensonge[(s, r)]             # le mensonge, toujours le même (complices compris)
                elif src.copie and origine in dernier and rng.random() < src.taux_copie:
                    o = dernier[origine]             # recopie, erreur comprise
                elif rng.random() < src.f(r):
                    o = vrai
                elif p_sosie and rng.random() < p_sosie:
                    o = sosie[r][vrai]               # l'erreur plausible
                else:
                    o = rng.choice([x for x in domaines[RELATIONS[r]] if x != vrai])
                dernier[(src.nom, s, r)] = o
                phrase = rng.choice(GABARITS[r]).format(s=s, o=o)
                enonces.append(Enonce(len(enonces), t, src.nom, s, r, o,
                                      f"[époque {t} · {src.nom}] {phrase}"))
    rng.shuffle(enonces)  # l'ordre d'arrivée ne trahit pas le temps

    # — questions à vérité connue : chaque fait n'est demandé qu'une fois par type —
    T, qs, quart = n_epoques - 1, [], n_questions // 4

    def q(typ, s, chaine, t, texte, attendu, grappe):
        qs.append(Question(len(qs), typ, s, tuple(chaine), t, texte, attendu, grappe))

    def tirer(liste, k):
        return rng.sample(liste, min(k, len(liste)))

    faits = [(s, r) for r in ["habite", "travaille", "dirige", "naissance"]
             for s in sujets[SUJET_DE[r]] if not (r == "habite" and s in discretes)]
    for s, r in tirer(faits, quart):
        q("actuel", s, [r], T, QUESTIONS[r].format(s=s, t="maintenant"), verite[(s, r)][T], (s, r, T))
    passes = [(s, r, t) for s, r in faits if r != "naissance" for t in range(T)]
    for s, r, t in tirer(passes, quart):
        q("historique", s, [r], t, QUESTIONS[r].format(s=s, t=f"à l'époque {t}"), verite[(s, r)][t], (s, r, t))
    for p in tirer(personnes, quart):
        org = verite[(p, "travaille")][T]
        q("deux_sauts", p, ["travaille", "dirige"], T,
          f"Qui dirige, maintenant, l'organisation pour laquelle travaille {p} ?",
          verite[(org, "dirige")][T], (org, "dirige", T))
    for s in sorted(discretes):      # le piège : des personnes connues, jamais localisées
        q("sans_reponse", s, ["habite"], T, QUESTIONS["habite"].format(s=s, t="maintenant"), None, (s, "habite"))
    for _ in range(len(discretes)):  # autant de noms jamais vus
        s, r = f"{frais(2)} {frais(3)}", rng.choice(["habite", "travaille", "naissance"])
        q("sans_reponse", s, [r], T, QUESTIONS[r].format(s=s, t="maintenant"), None, (s, r))

    return Monde(enonces, qs, verite, list(cfg["sources"]), n_epoques,
                 {r: domaines[RELATIONS[r]] for r in RELATIONS},
                 {r: cfg["changement"] * MOBILITE[r] for r in RELATIONS}, sosie, p_sosie, menteur,
                 tuple([menteur[0]] + [s.nom for s in cfg["sources"] if s.complice]) if menteur else None,
                 bool(cfg.get("contraintes")))
