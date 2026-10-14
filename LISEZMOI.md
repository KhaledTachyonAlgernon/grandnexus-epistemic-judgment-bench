# Banc d'essai GrandNexus — v0

Le premier fichier de GrandNexus n'est pas un organe : c'est l'instrument qui jugera les organes.

## Paradigme
GrandNexus est un organe de jugement. Les propositions arrivent seules ; seul le jugement compte.
Il doit croire durablement, dire pourquoi, réviser, et savoir ce qu'il ne sait pas.

## Le monde
`monde.py` génère un monde inventé (personnes, organisations, quartiers) dont les faits
changent avec le temps, rapportés par des sources de fiabilité et de fraîcheur inégales.
Trois réglages : `facile` (contrôle de cohérence), `realiste`, `hostile` (piège à majorité).
Quatre types de questions : `actuel`, `historique`, `deux_sauts`, `sans_reponse`
(dont des personnes connues mais jamais localisées : le piège à hallucination).

## Les témoins (`temoins.py`)
- `dernier gagne` — la dernière affirmation datée l'emporte ;
- `majorité` — vote sur tout ce qui a été dit ;
- `mots-clés` — recherche textuelle naïve, type RAG ;
- témoin LLM — `python evaluer.py --exporter-llm`, puis `noter_llm()` (non exécuté en v0).

`plafond (triche)` n'est pas un témoin : c'est l'optimum bayésien qui connaît les vrais
paramètres du monde. Il valide l'instrument et borne ce qui est atteignable.

## Règles
1. Un seul type de donnée qui circule : l'assertion.
2. Chaque organe sous ~200 lignes, nommé par ce qu'il fait à l'information.
3. Aucun organe sans métrique où il bat la configuration précédente, sans régression nette ailleurs.
4. Chaque hypothèse est écrite, avec son seuil, AVANT l'expérience.
5. Une métrique où tout le monde réussit est retirée ou durcie.

## Système de référence (état actuel)
`Meprise()` (meprise.py), qui empile : Pesée E → Filiation → Soupçon → Méprise.
Chaque organe est né d'un échec mesuré ; le registre `HYPOTHESES.md` donne, pour chacun,
l'hypothèse écrite avant, le verdict, et les réserves.

## Instrument (v2)
- L'unité de preuve est le FAIT, pas la question : intervalles par bootstrap en grappes de faits.
- Monde : 80 personnes, 24 organisations ; chaque fait n'est demandé qu'une fois par type.
- Plafond optimal sur les chaînes ; vérifié dominant dans les quatre mondes (I1).
- Graines 0-5 : vues. Toute nouvelle hypothèse se juge sur graines neuves (6 et au-delà).

## Limites connues
- Les systèmes structurés reçoivent les triplets : on teste le jugement, pas la perception.
- `sans_reponse` ne discrimine que les systèmes textuels.
- « deux sauts » : ~23 faits distincts par graine — seuls les grands écarts y sont lisibles.
- Le monde suit exactement le modèle des organes (changements markoviens, erreurs uniformes) :
  bon pour valider un mécanisme, muet sur sa robustesse quand ce modèle est faux.

## Lancer
    python evaluer.py
    python verifier_instrument.py <monde> 0,1,2,3,4,5 [budget_secondes]

---

# État au 13 octobre 2026 — carte des fichiers

## Le moteur de jugement (≈ 580 lignes) — c'est « GrandNexus » au sens strict
Empilement de référence : `Meprise()` = Pesée E → Filiation v3 → Soupçon → Méprise.
- `pesee.py` — Pesée E : datation, fiabilité et retard de chaque source, lissage dans le temps (avant-arrière), un-contre-tous.
- `filiation.py` — Filiation v3 : détecte les sources qui se recopient et retire leurs voix en double.
- `soupcon.py` — Soupçon : compromission locale (une source qui ment sur un fait précis).
- `meprise.py` — Méprise : apprend la FORME des erreurs (sosies, confusions partagées). Point d'entrée : `Meprise().ingerer(enonces)`, puis `.repondre(question)`.
- `reponse.py` — objet-réponse : valeur, confiance, deux doutes séparés (incertitude, contestation), justification, motifs.
- `litige.py` — organe REJETÉ (régression mesurée), conservé pour mémoire.

## L'Accueil (lire du texte au lieu de triplets)
- `accueil_regles.py` — lecteur de phrases à règles, sans LLM (figé, 99,5 % sur le désordre de style).
- `accueil_paragraphes.py` — lecteur de paragraphes à règles : pronoms, descriptions, corrections (figé, empreinte 33accea15603db46).

## L'instrument
- `monde.py` — générateur des mondes synthétiques (facile, réaliste, hostile, écho, plausible, menteur, complice, mixte…).
- `hors_modele.py` — monde où toutes les hypothèses des organes sont fausses à la fois.
- `temoins.py` — témoins de référence (dernier gagne, majorité, mots-clés, plafond bayésien).
- `evaluer.py`, `cache.py`, `verifier_instrument.py` — évaluation avec intervalles en grappes, caches versionnés par empreinte du code.

## Les mesures (un script par hypothèse pré-enregistrée)
- `test_*.py`, `mesure_echelle.py`, `echelle.py`, `mecanisme_*.py` — phase synthétique (organes, robustesse, ancres, boucle, objet-réponse).
- `eval_accueil.py`, `eval_paragraphes.py` — Accueil.
- `temoin_llm_noter.py`, `bout_en_bout_noter.py`, `fond_noter.py`, `fond2_noter.py`, `hm_noter.py` — confrontations avec Opus.
- `reel_collecte.py`, `reel_collecte2.py` — collecte des données réelles (Wikipédia, Wikidata).

## Les documents
- `CHARTE.md` — règles de méthode et résultats établis, avec leurs limites.
- `HYPOTHESES.md` — registre complet : 161 hypothèses écrites AVANT chaque expérience, avec verdicts et calibration.

## Résultats établis (résumé ; le détail et les réserves sont dans CHARTE.md)
- Dans les mondes synthétiques qui débordent de la fenêtre de lecture d'Opus 5.5, GrandNexus devance Opus outillé d'une recherche
  (+7,9 points sur trois graines ; +13,2 hors modèle), surtout sur le temps et la composition ; Opus raisonnant question par question
  ne fait pas mieux.
- Premier réel (maires, Wikipédia, 2019-2021, anonymisé) : égalité (94 % contre 96 %). La référence elle-même se trompe ;
  GrandNexus anticipe parfois les changements à tort.

## Reproduire
Python 3.12, aucune dépendance externe. Exemple :
    from monde import generer
    from meprise import Meprise
    m = generer("complice", 0)
    o = Meprise(); o.ingerer(m.enonces)
    for q in m.questions[:5]: print(q.texte, "→", o.repondre(q))
Les archives de données (réponses des témoins, collectes réelles) sont dans l'archive séparée `grandnexus_donnees`.
