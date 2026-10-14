# GrandNexus Epistemic Judgment Bench

Projet parallèle expérimental de GrandNexus.

Ce dépôt ne constitue pas GrandNexus v6.4 complet. Il explore un organe spécialisé de jugement épistémique : évaluer des assertions provenant de sources imparfaites, détecter les dépendances entre sources, distinguer l’incertitude de la contestation et mesurer les formes d’erreur.

## Positionnement

- projet expérimental séparé de `grandnexus-rebuild` ;
- aucune autonomie réelle et aucune action externe ;
- les mondes synthétiques servent à tester des mécanismes précis ;
- les hypothèses, seuils, échecs et limites sont consignés avant ou après chaque expérience ;
- une éventuelle intégration future dans GrandNexus passera par une interface contrôlée, en shadow/simulation, sans promotion automatique vers la vérité.

## Composants principaux

- `pesee.py` : fiabilité et retard des sources ;
- `filiation.py` : dépendances et copies entre sources ;
- `soupcon.py` : soupçon localisé ;
- `meprise.py` : formes d’erreurs ;
- `reponse.py` : réponse avec confiance, doutes et justification ;
- `base.py` : types minimaux et composition des chaînes de raisonnement ;
- `coherence.py` : contraintes déclarées C1/C2/C3, avec `Coherence3` et compatibilité `Coherence2` ;
- `monde.py` : générateur de mondes synthétiques ;
- `evaluer.py` : évaluation et intervalles en grappes ;
- `CHARTE.md` et `HYPOTHESES.md` : protocole et registre expérimental.

## Données

Les archives de données, sorties de campagnes, collectes externes et réponses de témoins ne sont pas incluses dans ce dépôt public initial. Elles restent séparées afin de limiter la diffusion de données dérivées et de préserver la distinction entre code, instrument et résultats.

## Exécution minimale

Python 3.11+ sans dépendance externe pour le noyau synthétique :

```bash
python3 evaluer.py
python3 test_echo.py
python3 test_echo_menteur.py
python3 test_filiation_v2.py echo
python3 test_noyau_compact.py
```

Certaines campagnes sont longues et certaines nécessitent des arguments ; voir les docstrings et `LISEZMOI.md`.

## Relation avec GrandNexus

Ce banc pourra fournir ultérieurement un organe de jugement ou des corpus adversariaux à GrandNexus v6.4. Il n'est pas un remplacement de sa mémoire, de son graphe, de son planificateur, de son ledger d'état ou de sa boucle d'autonomie simulée.
