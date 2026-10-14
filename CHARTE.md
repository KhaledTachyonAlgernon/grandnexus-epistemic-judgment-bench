# Charte opérationnelle de GrandNexus

Ce document dit ce que le système a le droit de conclure, et rien de plus. Il sert à fixer les critères
d'une mesure AVANT de la faire. Les preuves sont dans `HYPOTHESES.md` ; cette charte n'en ajoute aucune.

## 1. Paradigme
GrandNexus est un organe de jugement. Il reçoit des propositions de sources et décide ce qu'il en croit,
à quel degré, pourquoi, et jusqu'à quand. Une seule unité circule : l'assertion (sujet, relation, objet,
source, époque). Il ne génère pas, ne lit pas de texte (entrée = triplets), ne revendique aucune autonomie.

## 2. Statuts d'une affirmation
- **ÉTABLI** : hypothèse écrite avant, jugée sur graines neuves, verdict consigné.
- **EXPLORATOIRE** : mesuré sur graines déjà vues, ou après coup. Oriente ; ne prouve rien.
- **REJETÉ** : a échoué à sa règle écrite d'avance.
- **RETIRÉ** : affirmé puis réfuté par une mesure.

## 3. Système de référence : Pesée E → Filiation v3 → Soupçon → Méprise

| Organe | Ce qu'il peut conclure | Établi dans | Échecs connus (établis) |
|---|---|---|---|
| **Pesée E** (datation, fiabilité, retard, un contre tous, désatténuation) | une croyance par fait et par époque ; la fiabilité de chaque source (erreur ≤ 0,03) ; son retard | facile, réaliste, hostile ≈ plafond ; retard exact 3/3 ; fiabilité à ±0,014 | seule, dégrade l'écho (−1,9) ; capturée par un menteur crédible ; échoue face à une coalition |
| **Filiation v3** | « X recopie Y » et le taux de copie (estimé 0,71-0,83 pour 0,7-0,8) | écho +21,7 ; aucune fausse accusation sur 9 mondes-graines ; copieurs d'un menteur détectés 3/3 | sous coalition, a accusé deux honnêtes de se recopier (graine 36, taux 0,32 pour un seuil 0,3) |
| **Soupçon** | « telle source ment sur tel fait » (une seule par fait) | faits ciblés 44 → 85 % ; précision 100 % sur couples ; rappel 87-90 % (95-96 % sur candidats) ; 1 faux soupçon sur ~2 900 | face à une coalition, accuse les honnêtes ; aveugle si le menteur n'a qu'un énoncé ; garde-fou facile passé d'un cheveu (−0,20, borne +0,009) |
| **Méprise** | la forme des erreurs (quelles valeurs on confond) | plausible +3,75 puis +4,0 (deux séries) ; aucune perte ailleurs | reste ~2,4 points sous le plafond ; λ « habite » jusqu'à 0,58 hors monde plausible (sans coût mesuré) |

## 3 bis. Hors référence (outils de recherche)
- **Sources fixes (ancres)** : faits vérifiés de l'extérieur, fiabilité figée. Efficaces au-delà des faits ancrés
  (coalition : +29 à +62 points sur les mensonges non vérifiés, levier identifié : la Filiation rattache les complices
  dès que leurs accords deviennent des erreurs partagées). REJETÉES de la référence : perte hors cibles reproductible
  (−0,22 ; −0,43) au-delà de la marge de non-infériorité (0,5). Remède envisagé, non testé : complicité LOCALE.

## 4. Rejetés (ne pas réintroduire sans nouvelle hypothèse)
- Pesée B/C : fiabilité jugée contre ses propres croyances → auto-confirmation.
- Filiation v1 et v2 : fausses accusations dans les mondes honnêtes (cause : atténuation, corrigée en v3).
- Litige : régression de calibration significative dans le monde menteur (+0,002 Brier), due à la règle
  « un dissident peut n'avoir parlé qu'une fois » ; aveuglé quand la Filiation fusionne les honnêtes.
  Il réduisait pourtant de moitié les réponses sûres et fausses face aux complices.

## 5. Limites établies
- **Coalition coordonnée** (complices honnêtes ailleurs) : faits ciblés 7,4 % (majorité 10,7 %, plafond 75,6 %).
  Les défenses fondées sur les accords se retournent contre les honnêtes.
- **La réputation ne démasque pas un menteur stratégique** : complices jugés 0,89-0,93.
- **Hors du modèle des organes, rien n'est garanti** : tous les mondes suivent des changements markoviens,
  des retards fixes, et une seule forme d'erreur à la fois.
- **Instrument** : le plafond n'a été vérifié dominant que dans facile, réaliste, hostile, écho.
  La colonne « deux sauts » (~23 faits par graine) ne lit que de grands écarts.
- **Non testé** : perception (texte), témoin LLM, données réelles.

## 5 bis. Établi sur l'échelle de mondes à contraintes imbriquées (graines 45-49)
Dans CE monde synthétique : chaque contrainte déclarée rend plus cher le mensonge d'un menteur cohérent qui
minimise son coût (K : 0 → 1,96 → 4,56 → 7,20 faits × époques par mensonge ; chaque marche significative), mais
ne protège que la famille de faits qu'elle touche. Au sommet (d3), 48,5 % des mensonges restent gratuits —
surtout l'emploi des non-dirigeants, qu'aucune contrainte ne touche. Ce n'est pas une loi sur la densité des
graphes ni une preuve sur le réel.

## 5 ter. L'objet-réponse et les trois autres piliers (établi dans ces mondes synthétiques)
GrandNexus répond par un OBJET, jamais par un score fusionné (`reponse.py`) : valeur ; confiance ; doute « preuves »
(motif « peu de preuves » si confiance < 0,9) ; doute « contestation » (motif « contestée » si ≥ 2 voix effectives
la contredisent) avec contradicteurs et fusions de sources ; justification courte ; soupçons appliqués.
- **Dire pourquoi** : 3 énoncés cités suffisent à reproduire la décision dans 99 % des cas (fidélité locale), mais
  sont rarement nécessaires (22 %) : les réponses sont surdéterminées. Échec : dans le monde plausible, les cités
  sont un peu moins suffisants que le hasard (93 % contre 96 %).
- **Savoir ce qu'on ne sait pas** : deux défaillances, deux signaux. L'incertitude repère le bruit (AUC 0,93-0,98),
  pas la coordination (0,68-0,74) ; la contestation repère la coordination (0,88), pas le bruit (≈ 0,5). La fragilité
  est redondante avec l'incertitude. Un score fusionné ne s'effondre nulle part mais coûte dans le bruit ; dans un monde
  mixte, les motifs de l'objet sont JUSTES (« contestée » → coordination 100 % ; « peu de preuves » seul → bruit 96 %).
- **Où vérifier** : choisir les faits contredits par des sources indépendantes bat le hasard dans 3 mondes (78 % de
  l'oracle face à la coalition). Les justifications, écrites au moment du choix, rendent visibles les erreurs du
  sélecteur (une fausse fusion de deux honnêtes, graine 61).
- **Réviser — la boucle de bout en bout** (choisir → vérifier → ancrer → réviser → rechoisir) : chaque file répare son
  type de défaillance. Dans le monde mixte, la file « contestée » réduit de moitié les erreurs de coordination sans
  toucher au bruit ; la file « incertitude » fait l'inverse. Le second tour apporte encore la moitié du gain. Dégâts
  collatéraux ≈ 1 pour 17 corrections (ancres toujours hors référence pour cette raison).
- **Limites** : la répartition du budget entre les deux files est une décision d'usage ; la moitié-moitié coûte dans
  le bruit pur ; la file contestée s'épuise. Rien de cela ne vaut hors du modèle de monde testé.

## 5 quater. Le désordre réel — premiers résultats (établi sur texte ÉCRIT par Claude)
- Témoin LLM (Opus 5.5 effort élevé selon Khaled, lisant tout le corpus) contre GrandNexus (triplets, organes faits pour ces mondes) :
  jeu égal sur l'exactitude dans 3 mondes sur 4 ; GrandNexus nettement meilleur sur le passé et la calibration (Brier 0,09 contre 0,18).
  Le témoin n'invente jamais.
- Accueil : variation de STYLE → un lecteur à règles de 109 lignes suffit (99,5 %). Désordre STRUCTUREL (pronoms, corrections,
  descriptions, noms partiels, personnes inconnues) → lecteur à règles : précision 100 %, rappel 84 % (97 % hors inconnus) ;
  lecteur LLM : 100 % / 100 %. Aucun des deux ne tombe dans les corrections. Texte écrit et lu par la même famille de modèles.
- Architecture qui en ressort : le LLM PERÇOIT, GrandNexus JUGE.
- De bout en bout (petit monde qui tient dans le contexte, coalition) : « Opus lit, GrandNexus juge » = « Opus seul » en exactitude
  (84 % / 84 %), un peu mieux calibré sans significativité, plus cher (19 appels de lecture de plus). Opus a tout lu sans erreur.
  GrandNexus n'apprend pas nettement à se méfier d'un lecteur faible : ses erreurs sont surtout des OMISSIONS, invisibles à
  l'apprentissage de fiabilité. Valeur de GrandNexus NON démontrée sur l'exactitude ; restent à tester : corpus plus grand que le
  contexte, mise à jour incrémentale, persistance, objet-réponse (doutes et motifs) sur données réelles de bout en bout.
- Monde plus grand que la fenêtre (graine 83, coalition, 3 points de contrôle) : verdict pré-écrit « APTE » — GrandNexus 87 % contre
  Opus-recherche 82 % (+5,3 [+0,9 ; +10,5]) et Opus-fenêtre 66 %. Réplication : coalition (graine 84) +5,3 [−0,9 ; +12,3] → « APTE »
  formellement NON reproduit ; erreurs ordinaires (graine 85) +13,2 [+5,3 ; +21,1] → APTE. Trois graines réunies : +7,9 [+3,8 ; +11,7].
  Établi, dans ces mondes : quand le corpus déborde de la fenêtre, GrandNexus devance un modèle de pointe outillé d'une recherche,
  d'environ 8 points en moyenne. Non établi : le « profil de la tortue » (ne se reproduit pas).
- Hors du modèle (graine 86 : non markovien, vagues, retard variable, fiabilité qui se dégrade, erreurs fétiches, copie différée ; aucune
  adaptation) : GrandNexus 85 % contre Opus-recherche 72 %, +13,2 [+5,3 ; +21,1] → ROBUSTE HORS MODÈLE. L'avantage ne tient pas à la
  forme des mondes construits pour lui. Opus raisonnant question par question : aucun gain (72 % = 72 %) ; GrandNexus +10 [+3 ; +18].
- PREMIER RÉEL (maires de 60 villes, 5 éditions de Wikipédia, 2019-2021, anonymisé) : ÉGALITÉ (94,1 % contre 95,5 %, −1,4 [−3,2 ; 0]).
  Réel calme, sans débordement ni composition. Leçons : la référence (Wikidata) se trompe elle-même ; GrandNexus ANTICIPE parfois
  les changements à tort (modèle de retard trop confiant).

## 6. Exploratoire (ne pas citer comme acquis)
Contagion du menteur par la confiance (+0,55 point sur faits non ciblés) ; désatténuation plus utile quand
les preuves sont rares ; monde à contraintes : 17-33 % de mensonges exposés, la cohérence propage aussi le
mensonge, l'auto-contradiction brute ne sépare pas honnêtes et coalition.
**Retiré** : « une coalition est indiscernable sur les faits immobiles » (le plafond y fait 90 %).

## 7. Règles de méthode
1. Hypothèse écrite avant : spécification, seuil, probabilité, type **sens** ou **ampleur**.
   Prédire l'absence d'effet est une prédiction d'ampleur.
2. Graines neuves pour juger ; graines vues pour explorer. Tout paramètre choisi en exploration est figé avant le test.
3. L'unité de preuve est le fait ; intervalles par bootstrap en grappes.
4. Une métrique porte sur l'unité exacte de l'affirmation (couples source–fait, pas faits seuls) et vérifie
   ses invariants au lieu de les supposer.
5. Cache versionné par empreinte du code ; toute refonte vérifiée par non-régression.
6. Une règle écrite d'avance ne se change pas après coup ; une meilleure règle exige une confirmation sur graines neuves.
7. Tout signal défavorable vu en exploration est reporté dans l'hypothèse, pas résumé.
8. Une affirmation de mécanisme non mesurée n'entre pas dans le registre.
9. Un garde-fou d'absence de perte se formule avec une MARGE de non-infériorité fixée d'avance (perte < x),
   jamais « non significativement négatif » : avec assez de données, tout effet minuscule devient significatif.
10. Toute proportion utilisée comme diagnostic est comparée à son TAUX DE BASE, défini avant la mesure :
    « 100 % des cas présentent X » ne dit rien si 98 % de tous les cas le présentent.
11. Un signal nouveau se juge contre le MEILLEUR signal existant, pas seulement contre le hasard.
12. Tout script dont on importe des fonctions a une garde `if __name__ == "__main__"`.

## 8. Critères figés pour le test de densité (avant toute mesure)
**Objet, tel que figé** : une ÉCHELLE DE MONDES SYNTHÉTIQUES À CONTRAINTES IMBRIQUÉES — pas « la densité du
graphe » en général. Chaque niveau ajoute des contraintes ET de nouvelles familles de relations (emploi, siège,
résidence, couple) : un résultat portera sur cette progression précise, et ne pourra pas être attribué à la
densité seule. (Correction de Khaled, intégrée avant tout code.)

**Question** : sur cette échelle, l'information que le graphe rend disponible contre un mensonge coordonné
croît-elle, et à quel prix pour le menteur ?

**Statut des contraintes** : d1 est quasi définitionnelle dans ce monde ; celles de d2 et d3 sont des
régularités sociales CONTINGENTES, rendues dures (sans exception) par le générateur. Ce sont des règles de ce
monde synthétique, pas des vérités que GrandNexus devrait présumer du réel.

**Grille figée** (aucun niveau ajouté, retiré ou réglé après mesure ; tous rapportés) :
- d0 : aucune contrainte ;
- d1 : « qui dirige une organisation y travaille » ;
- d2 : d1 + « une organisation a un siège ; qui la dirige habite le quartier du siège » ;
- d3 : d2 + « des personnes forment des couples ; un couple habite le même quartier ».

**Menteurs figés** : coalition NAÏVE (ment sans se soucier des faits liés) et coalition COHÉRENTE. La coalition
cohérente est l'adversaire de référence ; elle connaît les contraintes déclarées du niveau. Les faits ciblés
(couples sujet–relation) sont tirés UNE fois par graine et sont IDENTIQUES aux quatre niveaux ; pour chacun, le
menteur choisit la fausse valeur qui minimise les falsifications SUPPLÉMENTAIRES de faits liés nécessaires pour
rester sans contradiction. Il ne peut pas changer de cible entre niveaux. (Borne posée par Khaled.)

**Monde** : UN seul monde par graine, identique à tous les niveaux (même vérité, respectant toutes les
contraintes ; mêmes familles de relations partout). Seules varient les contraintes DÉCLARÉES, connues du menteur
et du graphe. Cibles identiques de d0 à d3. (Trois points validés par Khaled.)

**Grandeurs** (par fait ciblé, fait × époque comme unité de coût) :
- E(d) : part des faits ciblés × époques où un mensonge NAÏF contredit au moins une contrainte déclarée ;
- F(d) : part des faits ciblés qu'une coalition COHÉRENTE peut falsifier GRATUITEMENT (zéro falsification supplémentaire) ;
- K(d) : nombre minimal de falsifications SUPPLÉMENTAIRES par fait ciblé.
Correction : la version précédente affirmait que K croît « par construction » face à ce menteur. C'était faux
tel qu'énoncé — mais avec un monde unique et des contraintes emboîtées, la monotonie FAIBLE (F non croissant,
K non décroissant) est un THÉORÈME : tout mensonge cohérent à d3 l'est à d2. Elle sert de contrôle de code.
Seules la progression STRICTE et l'AMPLEUR sont des affirmations falsifiables.

**Formulation des résultats** (borne de Khaled) : effet d'une information structurelle déclarée croissante dans
CE monde synthétique — jamais une loi générale sur la densité des graphes, jamais une preuve sur le réel.

**Adoption future d'un organe de Cohérence** : gain significatif sur les faits exposés ; aucune perte significative
sur les faits non ciblés (garde-fou contre la contagion) ; aucune perte dans les mondes existants.

**Limite de transfert** : dans le réel, la plupart des contraintes sont souples (elles ont des exceptions). Une
contrainte dure surestime le pouvoir du graphe : une exception honnête y paraîtrait mensonge, et un menteur
pourrait s'abriter derrière une régularité présumée. Dans GrandNexus, une contrainte est une connaissance
(provenance, statut, confiance), pas une loi.

**Variante possible, NON figée** (pour isoler la densité seule) : toutes les familles de relations présentes à
tous les niveaux, mêmes fiabilités, même univers de faits ; ne varie que la part des entités soumises aux contraintes.

**Interdits** : choisir la densité qui avantage un organe ; présenter E(d) ou K(d) comme « la valeur du graphe » ;
évaluer un organe de Cohérence sur les graines qui ont servi à le concevoir. Graines neuves : à partir de 45.
