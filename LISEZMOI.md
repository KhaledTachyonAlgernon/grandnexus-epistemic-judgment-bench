# GrandNexus — noyau de jugement (autonome)

Le moteur seul, sans l'instrument qui l'a jugé. Python 3.12, aucune dépendance externe. 739 lignes.
Vérifié le 14 octobre 2026 : réponses et objets-réponses IDENTIQUES à l'original sur 2 091 cas (mondes complice, plausible, écho) ;
Cohérence v2 : croyances et témoignages écartés IDENTIQUES à l'original (monde de la coalition à contraintes, graine 55).

- `base.py` — les types (Enonce, Question), la classe de base `Systeme` (dont `repondre()` compose les sauts) et `contributions`.
- `pesee.py` → `filiation.py` → `soupcon.py` → `meprise.py` — l'empilement de jugement ; `Meprise` est le point d'entrée.
- `reponse.py` — l'objet-réponse : valeur, confiance, deux doutes, justification.
- `coherence.py` — organe de Cohérence v3 (adopté le 14 octobre 2026). Classe `Coherence3`, à utiliser À LA PLACE de `Meprise`
  quand des contraintes sont DÉCLARÉES : C1 « qui dirige une organisation y travaille », C2 « un dirigeant habite au siège de son
  organisation », C3 « des conjoints habitent ensemble » (`contraintes=("C1", "C2", "C3")` par défaut).
  Il écarte les témoignages des sources qui se contredisent elles-mêmes sur des faits liés, côté désavoué par les sources sans
  contradiction, puis refait le jugement. `Coherence2` = C1 seule. Sans contrainte (`contraintes=()`), strictement identique à `Meprise`.
  Relations attendues : « dirige » (organisation → personne), « travaille » (personne → organisation), « habite » (personne → quartier),
  « siege » (organisation → quartier), « conjoint » (personne → personne).

Système de référence : `Meprise` quand aucune contrainte n'est déclarée ; `Coherence3` quand des contraintes le sont.

Utilisation :
    from base import Enonce, Question
    from meprise import Meprise
    from reponse import objet_reponse
    enonces = [Enonce(0, 0, "Source A", "Ville X", "dirige", "Personne P", ""),
               Enonce(1, 1, "Source B", "Ville X", "dirige", "Personne P", ""),
               Enonce(2, 1, "Source C", "Ville X", "dirige", "Personne Q", "")]
    o = Meprise(); o.ingerer(enonces)
    print(o.resoudre("Ville X", "dirige", 1))
    print(objet_reponse(o, ("Ville X", "dirige"), 1))
Un énoncé : (id, époque, source, sujet, relation, objet, texte). Les époques sont des entiers à partir de 0.
