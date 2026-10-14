# Registre des hypothèses — écrites AVANT l'expérience

## H-Pesée (écrite le 2026-10-07 à 05:45 UTC, avant toute ligne de pesee.py)

Organe : Pesée — estimer fiabilité, retard des sources et vitesse de changement du monde
à partir des seuls accords/désaccords, sans connaître les vrais paramètres.

Seuils (moyenne sur 3 graines) :
- H1 — monde hostile : global ≥ 70 %   (meilleur témoin : 60 %, plafond : 82 %)
- H2 — monde hostile : Brier < 0,20    (dernier gagne : 0,487 ; majorité : 0,177 ; plafond : 0,107)
- H3 — monde facile  : global ≥ 86 %   (pas de régression : meilleur témoin 88 %)
- H4 — monde réaliste : global ≥ 80 %  (secondaire ; meilleur témoin : 74 %, plafond : 88 %)

Ablation obligatoire : chaque composant doit gagner sa place.
- A — datation seule (fiabilité et retard fixés, non appris)
- B — A + fiabilité apprise
- C — B + retard appris
Si C ≤ B, le retard appris n'est pas gardé. Si B ≤ A, la fiabilité apprise n'est pas gardée.

Échec = hypothèse rejetée, notée ici telle quelle, pas reformulée.

### Verdict H-Pesée (même jour, après une seule exécution, sans retouche de l'organe)

| variante | H1 hostile ≥70 % | H2 hostile Brier <0,20 | H3 facile ≥86 % | H4 réaliste ≥80 % |
|---|---|---|---|---|
| A datation     | 74 % ✓ | 0,184 ✓ | 88 % ✓ | 87 % ✓ |
| B +fiabilité   | 72 % ✓ | 0,201 ✗ | 91 % ✓ | 88 % ✓ |
| C +retard      | 72 % ✓ | 0,201 ✗ | 91 % ✓ | 88 % ✓ |

Ablation, selon les règles écrites avant :
- C = B partout → le retard appris N'EST PAS gardé. Il a appris 0 pour toutes les sources,
  y compris L'Almanach (vrai retard : 3).
- B < A dans le monde hostile → la fiabilité apprise N'EST PAS gardée en l'état
  (elle aide dans le monde facile : 91 % contre 88 %, Brier 0,060 contre 0,087).
- A est gardé : la Datation seule porte l'essentiel du gain (hostile 60 → 74 %, réaliste 74 → 87 %).

Diagnostic (boîte de verre, hostile, graine 0) : L'Almanach, la source la plus prolifique,
est jugée fiable à 0,88 avec retard 0. Elle façonne les croyances, puis est jugée contre elles :
auto-confirmation — le biais déclaré dans l'en-tête de pesee.py. Le Registre, vraiment le
meilleur, est sous-estimé (0,86 au lieu de 0,95). L'organe est tombé, au niveau méta,
dans le piège à majorité que le monde hostile tendait.

Prochaine hypothèse candidate (non testée) : juger chaque source contre des croyances
calculées SANS ses propres énoncés (validation croisée « un contre tous »).

## H-UnContreTous (écrite le 2026-10-07 à 14:27 UTC, avant toute modification de pesee.py)

Variante D : fiabilité et retard appris, mais chaque source est jugée contre des croyances
calculées SANS ses propres énoncés.

Seuils (moyenne sur 3 graines) :
- H5 — retard appris de L'Almanach ≥ 2 sur au moins 2 graines sur 3 (vrai : 3)
- H6 — monde hostile : global > 76 %   (A : 74 % ; plafond : 82 %)
- H7 — monde hostile : Brier < 0,18    (A : 0,184)
- Garde-fous : facile ≥ 89 %, réaliste ≥ 86 %

Règle de décision écrite d'avance : si H6 OU H7 échoue, la fiabilité apprise est abandonnée
et l'organe suivant se construit sur la Datation seule (A).

### Verdict H-UnContreTous (une seule exécution, sans retouche)

| | D un contre tous | A datation | plafond |
|---|---|---|---|
| H5 retard L'Almanach | **3 / 3 / 3** ✓ (vrai : 3) | — | — |
| H6 hostile global | **82 %** ✓ | 74 % | 82 % |
| H7 hostile Brier | **0,113** ✓ | 0,184 | 0,107 |
| garde-fou facile ≥89 % | 89 % ✓ (limite) | 88 % | 91 % |
| garde-fou réaliste ≥86 % | 88 % ✓ | 87 % | 88 % |

Décision : D est gardé (fiabilité + retard + un contre tous).

Réserves notées sans les minimiser :
- Facile : D régresse face à B/C (91 → 89 %, deux sauts 85 → 78 %). Garde-fou tenu de justesse. Non expliqué.
- Les fiabilités apprises sont biaisées vers le bas (Registre 0,80 au lieu de 0,95) ;
  l'ordre des sources et les retards, eux, sont exacts.
- D atteint le plafond parce que le modèle de l'organe (changements markoviens, erreurs
  uniformes et indépendantes, retard fixe) est EXACTEMENT celui qui a généré le monde.
  Ce résultat ne dit rien de sa robustesse quand ce modèle est faux.
- Conséquence (règle 5) : le monde hostile est résolu, il ne discrimine plus. Il faut durcir.

## H-Écho (écrite le 2026-10-07 à 15:29 UTC, avant toute modification de monde.py)

Monde « écho » : une source d'origine médiocre (La Dépêche, fiabilité 0,55) est recopiée,
erreurs comprises, par trois sources (Le Relais, L'Écho, Le Miroir) qui la reprennent 70-80 %
du temps et sont fiables (0,90) le reste du temps. Deux sources indépendantes et rares
(Le Registre 0,95 ; La Gazette 0,85). L'organe D suppose des erreurs indépendantes : c'est faux ici.

Prédiction d'ÉCHEC, et de sa forme :
- H8  — effondrement : D global ≤ plafond − 10 points (moyenne 3 graines)
- H9  — fausse confiance : fiabilité apprise de La Dépêche ≥ 0,75 (vraie : 0,55) sur ≥ 2 graines sur 3
- H10 — signature de l'écho : plus de 50 % des erreurs de D (questions actuel + historique)
         reprennent exactement la valeur affirmée par La Dépêche
- H11 — D reste utile malgré tout : D global ≥ meilleur témoin + 5 points

Le plafond, lui, connaît le mécanisme de copie (vraisemblance de mélange) : c'est la borne.

### Verdict H-Écho (une seule exécution) — prédiction juste à moitié

| | prédit | observé | |
|---|---|---|---|
| H8 effondrement | D ≤ plafond − 10 | D 64 % / plafond 83 % (−19) | ✓ |
| H9 fausse confiance | Dépêche apprise ≥ 0,75 | 0,64 / 0,62 / 0,67 | ✗ |
| H10 signature de l'écho | > 50 % des erreurs | 86 % / 93 % / 95 % | ✓ |
| H11 D reste utile | ≥ meilleur témoin + 5 | 64 % contre majorité 68 % | ✗ |

La forme de l'échec est PIRE que prévu, et différente :
- Ce n'est pas l'origine qui est surévaluée, ce sont les sources honnêtes qui sont rabaissées
  à son niveau : Le Registre (vrai 0,95) est jugé 0,60-0,63, au niveau ou sous La Dépêche (vrai 0,55).
  Les trois copieurs sont classés en tête (0,70-0,74). Le consensus s'est inversé.
- D est pire que la simple majorité, et sûr de lui à tort (Brier 0,330 contre 0,210).
- La datation seule (A, 66 %) fait mieux que D (64 %) : dans un monde d'écho, apprendre
  qui croire à partir des accords AGGRAVE le jugement.

Piste (non testée) : on reconnaît un copieur à ses FAUTES, pas à ses bonnes réponses.
Deux sources indépendantes partagent rarement la même erreur ; des copieurs, constamment.

## H-Filiation (écrite le 2026-10-07 à 15:40 UTC, avant toute ligne de filiation.py)

Organe : Filiation — pour chaque paire de sources, estimer si l'une recopie l'autre à partir
de leurs ERREURS partagées (au-delà du hasard), puis traiter un énoncé recopié par une
vraisemblance de mélange (copie OU témoignage), sans connaître le mécanisme réel.

Seuils (moyenne sur 3 graines sauf mention) :
- H12 — détection, sur 3 graines sur 3 : Le Relais, L'Écho et Le Miroir ont chacun un parent
         détecté dans la clique {Dépêche, Relais, Écho, Miroir} ; Le Registre et La Gazette
         n'ont aucun parent et ne sont le parent de personne.
         (La direction exacte et un éventuel parent attribué à La Dépêche sont rapportés, non exigés.)
- H13 — monde écho : global ≥ 75 %   (majorité : 68 % ; D : 64 % ; plafond : 83 %)
- H14 — monde écho : Brier < 0,20    (majorité : 0,210 ; D : 0,330)
- H15 — sans régression : hostile ≥ 80 %, réaliste ≥ 86 %, facile ≥ 89 %

Risque principal, écrit d'avance : circularité. Si la clique domine les croyances de départ,
ce sont les sources honnêtes qui sembleront « partager des erreurs », et l'organe accusera
Le Registre et La Gazette. Ce cas ferait échouer H12 et serait noté tel quel.

Règle de décision : si H13 ou H15 échoue, la Filiation n'est pas gardée.

### Verdict H-Filiation (une seule exécution, sans retouche)

| | seuil | observé | |
|---|---|---|---|
| H12 détection | 3 copieurs → clique, honnêtes intacts, 3/3 graines | 3/3 : chaque copieur → La Dépêche, taux 0,71-0,83 (vrais 0,7-0,8), aucune erreur de sens | ✓ |
| H13 écho global | ≥ 75 % | **83 %** (= plafond) | ✓ |
| H14 écho Brier | < 0,20 | **0,092** (plafond 0,087) | ✓ |
| H15 hostile | ≥ 80 % | 80 % (D : 82 %) | ✓ limite |
| H15 réaliste | ≥ 86 % | 89 % | ✓ |
| H15 facile | ≥ 89 % | **82 %** (D : 89 %) | ✗ |

Décision, selon la règle écrite d'avance : la Filiation (v1) N'EST PAS gardée.

Diagnostic : fausses accusations hors du monde écho — facile : Le Registre « copie » La Gazette (0,89) ;
réaliste : La Gazette « copie » Le Registre (0,33) ; hostile : L'Almanach « copie » Le Registre (0,41).
Cause : l'estimateur pondère chaque accord par le doute résiduel sur la valeur. Quand les erreurs sont
rares, la somme des petits doutes sur des valeurs VRAIES domine : deux sources qui disent la même vérité
ont l'air de partager des erreurs. Et un retard ressemble à une copie (on répète le passé de l'autre).
Le signal était juste dans un monde riche en erreurs, faux dans un monde où presque tout le monde a raison.

## H-Filiation-v2 (écrite le 2026-10-07 à 15:44 UTC, avant toute modification de filiation.py)

Changement unique : le taux de copie est estimé par maximum de vraisemblance du mélange
P(X dit o) = c·[o = dernier de Y] + (1 − c)·P_indépendant(o), avec P_indépendant calculé à
l'époque effective de X (son retard compris). Un accord sur une valeur probablement VRAIE
n'est alors plus une preuve de copie.

Risque de sur-ajustement : v2 est conçue après avoir vu les graines 0-2. Elle est donc jugée
UNIQUEMENT sur des graines neuves (3, 4, 5), jamais vues, dans les quatre mondes.

Seuils (graines 3-5) :
- H12' détection écho : comme H12, sur 3 graines sur 3
- H16  aucune fausse accusation : dans facile, réaliste, hostile, aucune source n'a de parent
- H13' écho ≥ 75 % ; H14' écho Brier < 0,20
- H15' sans régression face à D sur les mêmes graines : facile, réaliste, hostile ≥ D − 1 point
Règle : si H13', H15' ou H16 échoue, la Filiation n'est pas gardée et le monde écho reste ouvert.

### Verdict H-Filiation-v2 (graines neuves 3-5, une seule exécution)

| | seuil | observé | |
|---|---|---|---|
| H12' détection écho | copieurs → clique, honnêtes intacts | 3 copieurs → La Dépêche sur 3/3 ; mais graine 5 : La Gazette « copie » Le Registre (0,33) | ✗ |
| H13' écho global | ≥ 75 % | **87 %** (D : 60 %, majorité : 65 %) | ✓ |
| H14' écho Brier | < 0,20 | 0,116 | ✓ |
| H15' facile | ≥ D − 1 (93 %) | 91 % (D : 94 %) | ✗ |
| H15' réaliste / hostile | ≥ D − 1 | 87 % = D / 86 % (D : 85 %) | ✓ |
| H16 aucune fausse accusation | 0 | facile 3/3 graines (Registre → Gazette jusqu'à 0,83), hostile 2/3 (Almanach → Registre), écho 1/3 | ✗ |

Décision : la Filiation v2 N'EST PAS gardée. Le monde écho reste ouvert.

Diagnostic : changer l'estimateur n'a pas supprimé les fausses accusations du monde facile. La cause est
en amont : les fiabilités apprises par la Pesée D sont biaisées vers le bas (réserve notée au verdict
H-UnContreTous, jugée alors sans conséquence). Si l'on croit les sources honnêtes moins exactes qu'elles
ne le sont, leur accord paraît trop bon pour être indépendant : on les soupçonne de collusion.
Mécanisme probable du pessimisme : chaque source est jugée contre des croyances bâties par les autres,
dont la fiabilité est elle-même sous-estimée ; ces croyances sont sous-confiantes ; d'où une nouvelle
sous-estimation — un point fixe en dessous de la vérité. (C : auto-confirmation ; D : auto-défiance.)

Limite d'instrument constatée : sur graines neuves, le plafond est dépassé (écho 87 % contre 84 % ; deux
sauts 72 % contre 62 %). Le plafond n'est optimal que saut par saut, et 60 questions par type donnent
± 5 points de bruit par colonne. L'écart-type sur la colonne « global » est d'environ 1,3 point.

## I-Instrument-v1 (écrit le 2026-10-07 à 16:30 UTC, avant toute modification)

Trois changements, aucun organe touché :
1. 1 200 questions par monde au lieu de 240 (300 par type). Le corpus reste identique à graine égale.
2. Plafond optimal sur les chaînes : pour « deux sauts », il somme sur toutes les organisations
   possibles au lieu de prendre la plus probable puis de continuer.
3. Intervalles de confiance à 95 % sur la colonne globale, et comparaisons APPARIÉES
   (mêmes questions, différence question par question) pour juger un organe contre un autre.

Critères d'acceptation de l'instrument :
- I1 — le plafond est ≥ à tout système (témoins, D, Filiation v2) sur « global » et « deux sauts »,
       dans chaque monde, sur les graines 0-5, à une marge de bruit près (≤ 1 intervalle de confiance).
       Cas qui a motivé le changement : Filiation v2, monde écho, graines 3-5 (87 % contre 84 %).
- I2 — demi-largeur de l'intervalle à 95 % d'une comparaison appariée ≤ 1,5 point (3 graines).
Si I1 échoue, le plafond n'en est pas un et aucun verdict futur ne s'y réfère.

### Verdict I-Instrument-v1 — REJETÉ

I1 échoue sur le cas même qui l'avait motivé : écho, graines 3-5, Filiation v2 dépasse le plafond
sur « deux sauts » de 5,8 points ± 2,6 (apparié), malgré le plafond optimal sur les chaînes.

Diagnostic (vérifié, pas supposé) : fait par fait, le plafond reste meilleur sur « travaille »
(89,9 % contre 86,0 %, 1 440 faits) ; sur « dirige », 93,8 % contre 95,5 % sur 288 faits (bruit).
Mais les 900 questions « deux sauts » ne reposent que sur 24 faits distincts (8 organisations ×
3 graines). Deux d'entre eux — dont un où le plafond hésitait à 0,50 — font basculer 109 questions.
L'intervalle supposait des questions indépendantes : elles ne le sont pas. Multiplier les questions
a produit de la fausse précision, pas de l'information. Conséquence rétroactive : toutes les
colonnes « deux sauts » des verdicts précédents reposaient sur ~8 faits par graine.

## I-Instrument-v2 (écrit avant toute modification)

1. L'unité de preuve devient le FAIT, pas la question : chaque question porte l'identifiant du fait
   qui décide de sa réponse ; les intervalles sont calculés par bootstrap en grappes sur ces faits.
2. Pas de doublon : un même fait n'est demandé qu'une fois par type.
3. Monde agrandi pour multiplier les faits distincts : 80 personnes, 24 organisations
   (au lieu de 40 et 8). Tous les chiffres antérieurs cessent d'être comparables : nouvelle base.
4. Plafond optimal sur les chaînes (conservé de v1).

Critères :
- I1 — plafond ≥ tout système sur « global » et « deux sauts », chaque monde, graines 0-5,
       à un intervalle de confiance EN GRAPPES près.
- I2 — on rapporte honnêtement la demi-largeur des comparaisons appariées en grappes (3 graines),
       sans seuil : la précision affichée doit être réelle, quelle qu'elle soit.

### Verdict I-Instrument-v2 — ACCEPTÉ

I1 ✓ dans les quatre mondes, graines 0-5 : aucun système ne dépasse le plafond à un intervalle en
grappes près (6 × 4 vérifications, 5 systèmes). Le cas qui avait motivé v1 (Filiation v2, écho) :
plafond +1,0 % ± 0,7 en global, +4,0 % ± 3,5 sur les deux sauts.

I2 (précision réelle, 6 graines, apparié) : global ± 0,4 à ± 2,0 points ; deux sauts ± 1,6 à ± 7,2.
La colonne « deux sauts » reste faible : ~23 faits distincts par graine. Elle ne doit servir qu'à
constater de grands écarts.

Nouvelle base de référence (global, graines 0-5, IC 95 % en grappes) :

| | facile | réaliste | hostile | écho |
|---|---|---|---|---|
| dernier gagne | 88,8 ± 0,9 | 62,1 ± 1,9 | 56,3 ± 1,8 | 61,1 ± 1,6 |
| majorité | 77,5 ± 1,5 | 67,5 ± 1,6 | 58,6 ± 1,7 | 64,9 ± 1,7 |
| mots-clés | 60,2 ± 1,9 | 47,2 ± 1,8 | 42,1 ± 1,7 | 46,2 ± 1,7 |
| Pesée D | 95,0 ± 0,7 | 89,9 ± 1,2 | 83,8 ± 1,4 | 68,0 ± 1,6 |
| Filiation v2 | 92,7 ± 1,0 | 89,9 ± 1,2 | 83,8 ± 1,4 | 88,6 ± 1,2 |
| plafond | 95,6 ± 0,7 | 90,7 ± 1,1 | 84,3 ± 1,3 | 89,6 ± 1,1 |

Relecture des verdicts antérieurs (questions corrélées, ~8 faits par colonne « deux sauts ») :
les grands écarts tiennent (C → D en hostile, Filiation en écho, effondrement de D en écho) ;
les petits ne sont pas lisibles (B contre A en facile, garde-fous « à la limite »).
Les graines 0-5 sont désormais VUES. Toute hypothèse future se juge sur graines neuves, à partir de 6.

## Exploration préalable (graines VUES 0-2, permise) — deux mécanismes réfutés, un confirmé

- Réfuté : « croyances sous-confiantes ». Les réponses de D sont calibrées (0,99 annoncé → 0,99 réel ;
  au milieu de l'échelle, légèrement trop sûres d'elles).
- Réfuté : « monde cru trop stable ». Figer le taux de changement sur sa vraie valeur ne change rien
  au biais de fiabilité (−0,060 → −0,060). À l'inverse, avec les vraies fiabilités, le taux de
  changement redevient juste : son biais est une conséquence, pas une cause.
- Confirmé : ATTÉNUATION. L'accord moyen avec des croyances calibrées mais non certaines vaut
  A = f·S + (1 − f)(1 − S)/(K − 1), où S = netteté moyenne (Σπ²) des croyances des autres.
  Tant que S < 1, f est tiré vers le bas — même sans aucune erreur de calibration.
  Inverser la formule : biais −0,060 → +0,004 (facile, S = 0,93) ; −0,101 → −0,002 (hostile, S = 0,87).
  (Analogue de la correction d'atténuation de Spearman, 1904.)

## H-Désatténuation (écrite le 2026-10-07 à 16:54 UTC, avant toute modification des organes)

Changement unique : dans l'étape M, la fiabilité est estimée par l'inversion de l'atténuation,
f = (A − (1 − S)·u) / (S − (1 − S)·u), u = moyenne de 1/(K − 1), au lieu de f = A.
Pesée E = D + désatténuation. Filiation v3 = Filiation v2 bâtie sur la Pesée E.

Jugé UNIQUEMENT sur graines neuves 6, 7, 8 ; comparaisons appariées, IC 95 % en grappes de faits.
- H17 mécanisme : erreur absolue moyenne |f appris − f vrai| ≤ 0,03 pour la Pesée E (facile,
      réaliste, hostile) et pour la Filiation v3 (quatre mondes).  (D : 0,06 à 0,10.)
- H18 paranoïa supprimée : Filiation v3 n'accuse personne en facile, réaliste, hostile — 3 graines sur 3.
- H19 écho conservé : les 3 copieurs détectés, Le Registre et La Gazette intacts — 3 graines sur 3.
- H20 performance, Filiation v3 − D : facile, réaliste, hostile non significativement négatif
      (borne haute de l'IC ≥ 0) ; écho ≥ +15 points.

Règle : la Filiation v3 remplace D comme système de référence si et seulement si H18 et H20 passent.
Si H17 passe mais H18 échoue, l'atténuation n'était pas la cause de la paranoïa ; noté tel quel.

Prédiction de l'expérimentateur (pour calibrer le prédicteur lui-même) :
H17 ≈ 85 %, H18 ≈ 60 %, H19 ≈ 80 %, H20 ≈ 60 %.

### Verdict H-Désatténuation (graines neuves 6-8, une seule exécution, sans retouche) — TOUT PASSE

| | seuil | observé | prédit | |
|---|---|---|---|---|
| H17 mécanisme | erreur ≤ 0,03 | Pesée E : 0,007 / 0,014 / 0,010 ; Filiation v3 : 0,007 / 0,014 / 0,010 / 0,012 (D : 0,066 à 0,204) | 85 % | ✓ |
| H18 paranoïa | 0 accusation, 3/3 | aucune, 9/9 (facile, réaliste, hostile). Sur les MÊMES graines, v2 accuse encore en facile g6 et g7 | 60 % | ✓ |
| H19 écho | 3 copieurs, 3/3 | 3/3, structure exacte, honnêtes intacts | 80 % | ✓ |
| H20 performance v3 − D | ≥ 0 / écho ≥ +15 | facile +0,1 ± 1,1 ; réaliste +0,8 ± 0,5 ; hostile +1,0 ± 0,9 ; écho +21,7 ± 2,7 | 60 % | ✓ |

Décision : la Filiation v3 devient le système de référence.
Elle égale le plafond dans les quatre mondes (plafond − v3 : +0,2 ; −0,1 ; 0,0 ; −0,2 ; tous dans l'IC).

Preuve causale : entre v2 et v3, un seul changement (la désatténuation), mêmes données. Les fausses
accusations disparaissent. Le biais d'atténuation était bien la cause de la paranoïa.

Interaction notée : la Pesée E SEULE dégrade le monde écho (−1,9 ± 1,2 face à D). Mieux mesurer la
fiabilité, dans un monde où le modèle d'indépendance est faux, n'aide pas. Les deux organes ne valent
qu'ensemble.

Calibration de l'expérimentateur : 4 prédictions, 4 réalisées, Brier 0,096. Sous-confiant sur H18 et H20
cette fois. Une seule série ne dit rien : à poursuivre.

Réserve qui demeure : les quatre mondes, y compris la copie, suivent exactement les modèles des organes.

# Phase 2 — casser les modèles des organes, une hypothèse à la fois

## H-Plausible (écrite le 2026-10-07 à 17:14 UTC, avant toute modification de monde.py)

Hypothèse cassée : les erreurs sont uniformes. Monde « plausible » : chaque valeur a un « sosie »
fixe (valeur avec laquelle on la confond) ; une source qui se trompe choisit le sosie de la vérité
70 % du temps, une autre valeur au hasard sinon. Quatre sources INDÉPENDANTES (aucun copieur) :
Le Registre 0,90 ; La Gazette 0,80 ; Radio Quartier 0,70 ; Le Forum 0,60.
Le plafond connaît les sosies et la règle des 70 %. Les organes, non.

Graines neuves 9, 10, 11. Comparaisons appariées, IC 95 % en grappes.
Prédictions (avec la probabilité que j'y attache) :
- H21 fausses accusations : la Filiation v3 attribue un parent à au moins une source honnête
       sur ≥ 2 graines sur 3.                                                      — 75 %
- H22 écart au plafond : Filiation v3 ≤ plafond − 3 points (global).               — 60 %
- H23 la paranoïa coûte : Filiation v3 − Pesée E significativement négatif.        — 55 %
- H24 fiabilités encore justes : erreur moyenne |f appris − f vrai| ≤ 0,03 (Pesée E). — 50 %
Aucune règle de décision : c'est un test de robustesse, on mesure la forme de la casse.

### Verdict H-Plausible (graines 9-11, une seule exécution) — l'organe casse, mais pas où je l'attendais

Global : majorité 64,5 % ; Pesée D 84,3 % ; Pesée E 85,4 % ; Filiation v3 85,4 % ; plafond 90,6 %.

| | prédit | observé | ma proba | |
|---|---|---|---|---|
| H21 fausses accusations ≥ 2/3 | oui | AUCUNE, 0/3 | 75 % | ✗ |
| H22 v3 ≤ plafond − 3 | oui | −5,2 ± 1,6 | 60 % | ✓ |
| H23 la paranoïa coûte | oui | v3 − E = 0,0 ± 0,0 (aucune accusation, aucun coût) | 55 % | ✗ |
| H24 fiabilités justes ≤ 0,03 | oui | 0,015 / 0,012 / 0,020 | 50 % | ✓ |

Forme réelle de la casse (vérifiée) : 48 % des erreurs de la Filiation v3 sont exactement le sosie de
la vérité (le hasard en donnerait 2 à 17 %), et sur 46 % de ces erreurs le plafond avait juste.
Ce n'est pas de la paranoïa : c'est de l'information jetée. L'organe suppose des erreurs uniformes,
donc il lit un vote pour le sosie comme une preuve forte en faveur du sosie. Le plafond sait que
ce vote est du bruit attendu autour de la vérité — et même qu'il POINTE vers elle.
La Filiation, elle, a résisté : les erreurs plausibles partagées ne l'ont pas fait accuser.

Calibration de l'expérimentateur : cette série Brier 0,319 (2/4). Cumul sur 8 prédictions : 0,207.
Mon erreur de fond : j'attendais la casse dans l'organe le plus récent (Filiation) ; elle était dans
le plus ancien (la vraisemblance de la Pesée).

Piste (non testée) : apprendre la FORME des erreurs du monde — une matrice de confusion partagée par
relation (quelles valeurs fausses accompagnent quelles vérités), estimée par EM comme le reste.

## H-Thématique (écrite le 2026-10-07 à 17:17 UTC, avant toute modification de monde.py)

Hypothèse cassée : une source a UNE fiabilité. Monde « thématique » : la fiabilité dépend du sujet.
Erreurs uniformes, aucun copieur, aucun retard (une seule hypothèse cassée).
                 habite  travaille  dirige  naissance
  Le Registre     0,95     0,95      0,55     0,95     (administratif : bon sur l'état civil, mauvais sur les dirigeants)
  La Gazette      0,55     0,85      0,95     0,60     (économique : l'inverse)
  Radio Quartier  0,85     0,60      0,60     0,80
  Le Forum        0,65     0,65      0,65     0,65
Le plafond connaît ces fiabilités par sujet. Les organes n'en apprennent qu'une par source.

Raisonnement : « dirige » ne pèse que 24 faits sur 264 par époque ; la fiabilité unique apprise
sera dominée par l'état civil. Le Registre paraîtra excellent (~0,9) et La Gazette médiocre (~0,7),
précisément l'inverse de la vérité sur les dirigeants.

Graines neuves 12, 13, 14. Exactitude par relation mesurée sur TOUS les faits × époques (pas
seulement les questions), pour avoir assez de points sur « dirige ».
- H25 v3 ≤ plafond − 3 points (global, questions)                                    — 80 %
- H26 la casse se concentre sur « dirige » : écart v3/plafond ≥ 10 points sur « dirige »,
       ≤ 3 points sur « habite » et « travaille »                                         — 60 %
- H27 deux sauts : v3 ≤ plafond − 10 points                                            — 55 %
- H28 aucune fausse accusation de la Filiation                                          — 70 %
- H29 v3 reste ≥ majorité + 10 points (global)                                         — 85 %

### Verdict H-Thématique (graines 12-14) — l'organe ne casse pas ; le monde ne lui en donnait pas l'occasion

Global : majorité 67,8 % ; Filiation v3 89,7 % ; plafond 90,1 %.
| | observé | ma proba | |
|---|---|---|---|
| H25 v3 ≤ plafond − 3 | +0,4 ± 1,2 | 80 % | ✗ |
| H26 casse concentrée sur « dirige » (≥ 10 pts) | dirige +1,3 ; habite +0,4 ; travaille +0,3 (faits × époques) | 60 % | ✗ |
| H27 deux sauts ≤ plafond − 10 | +1,2 ± 7,1 | 55 % | ✗ |
| H28 aucune fausse accusation | aucune, 3/3 | 70 % | ✓ |
| H29 v3 ≥ majorité + 10 | +21,9 ± 2,6 | 85 % | ✓ |

La boîte de verre montre bien le malentendu prévu (Le Registre ~0,91, La Gazette ~0,70, à l'inverse
de la vérité sur « dirige »), mais il ne coûte presque rien : avec des erreurs uniformes sur un grand
domaine (79 personnes possibles) et ~1,2 énoncé par fait et par époque, la vérité est la seule valeur
qui se répète. Les poids n'ont de levier que si les preuves sont rares ou les erreurs concentrées.
Conclusion honnête : ce monde ne mettait pas l'hypothèse à l'épreuve.

Calibration de l'expérimentateur : série Brier 0,283 (2/5). Cumul 13 prédictions : 0,236.
Constat : je raisonne bien sur QUEL mécanisme est violé, mal sur l'AMPLEUR de ses effets — qui dépend
de la redondance des preuves et de la dispersion des erreurs, que je n'ai pas calculées.

## H-Thématique-rare (écrite le 2026-10-07 à 17:20 UTC, avant d'exécuter)

Même monde, même casse, mais preuves rares : couverture 0,10 par source au lieu de 0,30
(~0,4 énoncé par fait et par époque). Le plafond et les organes inchangés. Graines neuves 15, 16, 17.
- H30 v3 ≤ plafond − 3 points (global)                                   — 55 %
- H31 écart v3/plafond sur « dirige » (faits × époques) ≥ 5 points        — 50 %
- H32 écart sur « dirige » > écart sur « habite » + « travaille » réunis  — 65 %

### Verdict H-Thématique-rare (graines 15-17) — robuste, même quand les poids ont du levier

Global : majorité 57,4 % ; Pesée D 68,4 % ; Filiation v3 72,4 % ; plafond 73,4 % (écart +1,0 ± 1,4).
Par relation (faits × époques) : habite +1,4 ; travaille +1,2 ; dirige −1,0 (v3 au-dessus, bruit) ; naissance +0,1.
| | ma proba | |
|---|---|---|
| H30 v3 ≤ plafond − 3 | 55 % | ✗ |
| H31 écart « dirige » ≥ 5 | 50 % | ✗ |
| H32 « dirige » > habite + travaille | 65 % | ✗ |

Conclusion : une fiabilité unique par source, même fausse sujet par sujet, coûte ≈ 1 point ici.
Les conflits directs entre deux sources sur un même fait à une même époque sont rares, et le filtre
temporel agrège beaucoup d'époques : la mauvaise pondération a peu d'occasions de trancher à tort.

Observation hors registre (non prédite, à confirmer) : la désatténuation vaut +4,0 ± 1,4 sur D quand
les preuves sont rares, contre ~+1 ailleurs — cohérent avec la formule (S plus bas → atténuation plus forte).

Calibration de l'expérimentateur : série 0/3, Brier 0,325. Cumul 16 prédictions : Brier 0,253.
Un prédicteur qui répondrait toujours 50 % obtiendrait 0,250. Mes prédictions de robustesse ne valent,
pour l'instant, pas mieux qu'un pile ou face.

Carte des casses, à ce stade :
- erreurs uniformes → FAUX dans le monde réel : coût 5,2 points (plausible). Vulnérabilité réelle.
- une fiabilité par source → FAUX : coût ≈ 0-1 point, même avec preuves rares. Robuste ici.
- reste à cartographier : le menteur stratégique ; puis les interactions (fiabilité par sujet ×
  erreurs plausibles : là, les erreurs concentrées donneraient enfin du levier aux poids).

## H-Menteur (écrite le 2026-10-07 à 18:15 UTC, avant toute modification de monde.py)

Hypothèse cassée : les erreurs d'une source sont indépendantes d'un énoncé à l'autre.
Monde « menteur » : Le Notable, prolifique (couverture 0,40), fiable à 0,95 PARTOUT sauf sur 15 % des
faits (habite, travaille, dirige) tirés au hasard, où il affirme toujours la même fausse valeur, à
chaque époque. Autres sources honnêtes et indépendantes : Le Registre 0,90 (0,25), La Gazette 0,80
(0,25), Radio Quartier 0,70 (0,30). Erreurs uniformes, pas de copie, pas de retard.
Le plafond connaît le MÉCANISME (proportion de faits ciblés, mensonge constant) mais pas les cibles :
il pèse, fait par fait, « ce fait est-il ciblé ? » par vraisemblance de mélange.

Graines neuves 18, 19, 20. Exactitude sur faits × époques, séparée faits ciblés / non ciblés.
Probabilités : ressentie → corrigée vers 50 % (Brier cumulé 0,253 ≈ pile ou face).
- H33 faits ciblés : v3 ≤ plafond − 10 points                        — 75 % → 65 %
- H34 global (questions) : v3 ≤ plafond − 2 points                   — 65 % → 58 %
- H35 fiabilité apprise du Notable ≥ 0,80 (il reste parmi les plus crus) — 80 % → 65 %
- H36 aucune fausse accusation de la Filiation                       — 70 % → 60 %

### Verdict H-Menteur (graines 18-20, une seule exécution) — la casse la plus grave

Global : majorité 65,9 % ; Filiation v3 86,3 % ; plafond 91,0 % (écart +4,8 ± 1,3).
Faits × époques : faits ciblés — plafond 90,3 %, v3 **55,3 %** (écart +35,0) ;
non ciblés — plafond 93,3 %, v3 92,5 % (écart +0,8). 93 % des erreurs de v3 sur les faits ciblés
reprennent exactement le mensonge.

| | proba ressentie → corrigée | |
|---|---|---|
| H33 faits ciblés ≥ 10 pts sous le plafond | 75 → 65 % | ✓ (35 pts) |
| H34 global ≥ 2 pts sous le plafond | 65 → 58 % | ✓ (4,8) |
| H35 fiabilité apprise du Notable ≥ 0,80 | 80 → 65 % | ✓ (0,88-0,89 : classé PREMIER) |
| H36 aucune fausse accusation | 70 → 60 % | ✓ |

Forme de la casse : capture de réputation. Le menteur est jugé la source la plus fiable du monde, et
les honnêtes qui le contredisent sur ses cibles sont DÉPRÉCIÉS (Le Registre 0,84-0,85 au lieu de 0,90).
Un menteur crédible ne propage pas seulement ses mensonges : il discrédite ceux qui disent vrai.
L'organe ne peut pas représenter « fiable en général, pas sur ce fait-là » : sa réputation est par
source. Le plafond, lui, se demande fait par fait si une valeur constante, contredite par les autres
même quand le monde change, est un mensonge — et retrouve 90 %.

Calibration : 4/4. Brier ressenti 0,079 ; corrigé 0,145 — la correction a coûté cette fois.
Cumul 20 prédictions (ressenti) : 0,218. Une série ne valide ni n'invalide la correction.

Contraste instructif avec H-Thématique : affiner la réputation par SUJET ne servait à rien ; l'affiner
par FAIT est décisif — parce que l'erreur du menteur est persistante, pas dispersée.

Carte complète des casses isolées :
| hypothèse cassée | coût global | coût local | réparation candidate |
|---|---|---|---|
| erreurs uniformes (plausible) | −5,2 | 48 % des erreurs = sosie | Méprise : forme des erreurs (confusion partagée) |
| une fiabilité par source (thématique) | ≈ −1 | ≈ −1 sur « dirige » | aucune nécessaire |
| sources indépendantes (écho) | résolu | — | Filiation v3 |
| erreurs indépendantes dans le temps (menteur) | −4,8 | −35 sur les faits ciblés | Soupçon : compromission par (source × fait) |
Cause commune des deux casses actives : le modèle d'erreur tient en UN nombre par source.

## Observation : la contagion du menteur (graines 18-20, contrefactuel exact)
Mêmes corpus, mensonges du Notable remplacés par la vérité. Réputations (Filiation v3) :
Registre 0,85 → 0,90 ; Gazette 0,76 → 0,80 ; Radio Quartier 0,68 → 0,71 ; Notable 0,88 → 0,96.
Exactitude sur les faits NON ciblés : 95,15 % → 95,69 % (+0,55 point).
La contagion passe par la confiance de tout le panier, pas (ou peu) par les autres faits : la baisse
est à peu près proportionnelle, l'ordre des sources préservé, la redondance absorbe le reste.

## H-Soupçon (écrite le 2026-10-07 à 18:25 UTC, avant toute ligne de code)

Organe : Soupçon — pour chaque fait, se demander si UNE source y est compromise.
Spécification écrite avant le code :
- Candidats : une source dont TOUS les énoncés sur ce fait affirment la même valeur (≥ 2 énoncés).
- Hypothèses par fait : « personne n'est compromis » ou « exactement la source s l'est ».
- Si s est compromise sur ce fait : ses énoncés n'informent pas sur la vérité ; ils valent 1/(K−1)
  (un mensonge tiré une fois, puis répété).
- A priori q_s par source, appris par EM : moyenne de P(s compromise | données) sur ses faits. Départ 0,02.
- La fiabilité de s s'estime sur ses énoncés pondérés par (1 − P(compromise)).
- Bâti sur la Filiation v3 (copie, désatténuation, retard, un contre tous inchangés).
Risque déclaré : PARANOÏA — une source honnête qui répète correctement un fait stable, ou une source
en retard qui répète une valeur ancienne (L'Almanach, monde hostile), a la signature d'un menteur.

Graines neuves 21, 22, 23 pour TOUS les mondes. Probabilités ressentie → corrigée.
- H37 détection (menteur) : en marquant « compromis » si P > 0,5, précision ≥ 80 % ET rappel ≥ 80 %
       sur les couples (Notable, fait ciblé)                                          — 60 → 55 %
- H38 réparation locale : exactitude sur faits ciblés ≥ 80 % (v3 : 55 % ; plafond : 90 %) — 65 → 58 %
- H39 réputations restaurées : erreur moyenne |f appris − f vrai| des trois honnêtes ≤ 0,03
       (v3 : ~0,045 ; pour le Notable, f vrai = 0,95 hors cibles)                       — 60 → 55 %
- H40 pas de paranoïa : dans facile, hostile, écho, moins de 1 % des couples candidats marqués
       compromis, ET Soupçon − v3 non significativement négatif (global, apparié)       — 50 → 50 %
- H41 global (menteur) : Soupçon ≥ plafond − 1,5 point                                  — 55 → 53 %
Règle : le Soupçon remplace la Filiation v3 si et seulement si H38 et H40 passent.

### Verdict H-Soupçon (graines neuves 21-23, une seule exécution, sans retouche) — TOUT PASSE

| | seuil | observé | proba | |
|---|---|---|---|---|
| H37 détection | précision et rappel ≥ 80 % | précision 100 / 100 / 100 % ; rappel 90 / 87 / 87 % | 55 % | ✓ |
| H38 faits ciblés | ≥ 80 % | **84,6 %** (v3 : 44,1 % ; plafond : 79,8 %) | 58 % | ✓ |
| H39 réputations | erreur honnêtes ≤ 0,03 | 0,010 / 0,016 / 0,023 (v3 : 0,053 / 0,056 / 0,019) ; Notable 0,949 (vrai hors cibles 0,95) | 55 % | ✓ |
| H40 paranoïa | < 1 % marqués, pas de perte | marqués : facile 1/1175, hostile 0/716, écho 0/1041. Pertes : facile −0,20 % (borne haute +0,009 %), hostile 0,0, écho +0,4 ± 0,6 | 50 % | ✓ (limite) |
| H41 global menteur | ≥ plafond − 1,5 | 90,3 % = plafond (+0,1 ± 0,3) ; +4,6 ± 1,3 sur v3 | 53 % | ✓ |

Décision : le Soupçon remplace la Filiation v3 comme système de référence.

Réserves :
- H40 passe d'un cheveu dans le monde facile : 4 questions changent sur 3 graines, toutes perdues.
  Effet minuscule (−0,2 point), signe défavorable, non significatif. À surveiller.
- Sur les faits ciblés, le Soupçon (84,6 %) dépasse le plafond (79,8 %). ~117 faits ciblés, très corrélés
  par fait : probablement du bruit (≈ 6 faits), peut-être les approximations du plafond (mensonge tiré
  en 1/K, mélange appliqué dès un seul énoncé). Non revendiqué.
- Propension apprise du Notable : 0,106 = 15 % de ses faits sur trois relations sur quatre (attendu ≈ 0,105).

Calibration de l'expérimentateur : 5/5. Brier ressenti 0,179 ; corrigé 0,210. Deuxième série où la
correction vers 50 % coûte. Cumul 25 prédictions (ressenti) : 0,210.

Système de référence : Pesée E (datation, fiabilité, retard, un contre tous, désatténuation)
+ Filiation (copie) + Soupçon (compromission locale). Casse restante connue : erreurs plausibles (−5,2).

## Exploration préalable à la Méprise (graines VUES : plausible 9-10, facile 0-1, hostile 0, écho 0)
- Apprenable : à partir des seules croyances du Soupçon, le sosie est retrouvé pour 97-99 % des valeurs
  ayant au moins deux erreurs attendues.
- Apophénie réelle : dans le monde facile (erreurs uniformes), les confusions apprises culminent à
  3-9 × le hasard (selon le lissage), à partir de coïncidences.
- Remède mesuré : juger chaque erreur contre les comptes calculés SANS elle, et apprendre par relation
  la part λ des erreurs qui suit une forme plutôt que le hasard. λ : plausible 0,69-0,91 ;
  facile 0,00-0,13 ; MAIS hostile « habite » 0,38, écho « habite » 0,26 (structure réelle ou fantôme ?).

## H-Méprise (écrite le 2026-10-07 à 19:13 UTC, avant toute ligne de code)

Spécification :
- Par relation r : P(o | v, erreur) = λ_r · S_r[v][o] + (1 − λ_r)/(K − 1), avec
  S_r[v][o] = (N[v][o] + α/(K−1)) / (N_v + α), α = 1, N = comptes d'erreurs attendus d'après les croyances
  complètes, pondérés par (non-copie) × (non-compromission).
- λ_r appris par EM sur la vraisemblance prédictive « un contre tous » (chaque erreur jugée sans elle).
- Vraisemblance d'un énoncé : f si o = v, sinon (1 − f) · P(o | v, erreur).
- Désatténuation généralisée : f = (A − Γ)/(S − Γ), Γ = espérance de l'accord par erreur sous la forme apprise.
- Départ : λ = 0 (erreurs uniformes) ; apprise à chaque étape M, après les autres organes.
- Approximations conservées : la Filiation et le Soupçon gardent leur modèle d'erreur uniforme.
Bâtie sur le Soupçon.

Graines neuves 24, 25, 26. Probabilités NON corrigées (la correction a coûté deux séries sur deux).
- H42 plausible : Méprise ≥ plafond − 1,5 point (global)                                   — 70 %
- H43 plausible : Méprise − Soupçon ≥ +3 points                                            — 75 %
- H44 pas d'apophénie : facile, hostile, écho, menteur — Méprise − Soupçon non significativement
       négatif (borne haute de l'IC ≥ 0)                                                    — 55 %
- H45 λ appris : plausible ≥ 0,5 sur toutes les relations ; facile ≤ 0,2 sur toutes      — 75 %
Règle : la Méprise remplace le Soupçon si et seulement si H42 et H44 passent.

### Verdict H-Méprise (graines neuves 24-26, une seule exécution, sans retouche) — REJETÉE par la règle

| | seuil | observé | proba | |
|---|---|---|---|---|
| H42 plausible ≥ plafond − 1,5 | | plafond − Méprise = +2,44 ± 1,13 | 70 % | ✗ |
| H43 plausible : Méprise − Soupçon ≥ +3 | | +3,75 ± 1,36 | 75 % | ✓ |
| H44 pas d'apophénie (borne haute ≥ 0) | | facile +0,00 (+0,15) ; hostile −0,15 (+0,14) ; écho −0,10 (+0,40) ; menteur −0,10 (+0,21) | 55 % | ✓ |
| H45 λ : plausible ≥ 0,5 ; facile ≤ 0,2 | | plausible 0,70-0,95 ✓ ; facile g24 « habite » 0,45 ✗ | 75 % | ✗ |

Décision, selon la règle écrite d'avance (H42 ET H44) : la Méprise NE remplace PAS le Soupçon.

Lecture honnête : la Méprise referme 60 % de l'écart au plafond dans le monde plausible (6,1 → 2,4 points)
sans perte significative ailleurs. La règle exigeait d'atteindre le plafond, pas d'améliorer : elle
confondait « complet » et « utile ». Je ne la change pas après coup. Une adoption sur la base de H43 + H44
exigerait une nouvelle confirmation pré-enregistrée sur graines neuves.

Apophénie : λ « habite » (K = 6) monte à 0,45 dans un monde facile (g24), 0,33-0,43 en hostile, 0,15-0,21
en écho — sans coût mesurable. Petit domaine : les coïncidences s'y accumulent. Inexpliqué, inoffensif ici.

Calibration : 2/4, Brier 0,329. Cumul 29 prédictions : 0,227. Les deux échecs portent encore sur des
AMPLEURS : j'avais mesuré l'identification des sosies (97 %), puis extrapolé son effet sur les réponses.
Mesurer un mécanisme ne suffit pas ; il faut mesurer la grandeur qu'on prédit.

## Correction d'instrument (signalée par Khaled) — métrique de H37
Le calcul de précision de H37 comptait des FAITS au dénominateur, sans l'identité de la source, alors
que l'affirmation porte sur des couples (source, fait). Il n'était juste que par un invariant implicite
(hypothèses mutuellement exclusives → au plus une source marquée par fait), ni énoncé ni vérifié.
Recalcul explicite sur couples, graines 21-23 : invariant vérifié (max 1 source marquée par fait) ;
précision 26/26, 26/26, 20/20 = 100 % (confirmée) ; rappel sur tous les couples ciblés 90 / 87 / 87 %
(inchangé) ; rappel sur les seuls couples candidats (≥ 2 énoncés du Notable) 96 / 96 / 95 %.
Les couples manqués sont surtout des faits où le menteur n'avait qu'un énoncé : jamais candidats.
test_soupcon.py corrigé : métrique sur couples + assertion de l'invariant.

## H-Méprise-confirmation (écrite le 2026-10-08 à 09:19 UTC, avant d'exécuter)
Question unique : la Méprise doit-elle être adoptée ? Rien n'est modifié dans l'organe.
Nouvelle règle d'adoption, posée AVANT de voir ces graines (la règle H42 confondait complet et utile) :
- H46 plausible : Méprise − Soupçon significativement positif (borne basse de l'IC > 0)     — 90 %
- H47 facile, hostile, écho, menteur : Méprise − Soupçon non significativement négatif
       dans CHACUN (borne haute ≥ 0)                                                         — 65 %
Graines neuves 27, 28, 29. Adoption si et seulement si H46 et H47 passent.

### Verdict H-Méprise-confirmation (graines neuves 27-29, sans retouche) — ADOPTÉE

| | observé | proba | |
|---|---|---|---|
| H46 plausible, gain significatif | +4,01 ± 1,57 (borne basse +2,44) | 90 % | ✓ |
| H47 aucune perte significative | facile +0,15 ; hostile +0,10 ; écho +0,15 ; menteur +0,20 (bornes hautes toutes > 0) | 65 % | ✓ |

Décision : la Méprise remplace le Soupçon comme système de référence.
Le gain se reproduit (+3,75 sur 24-26, +4,01 sur 27-29) : ce n'était pas un coup de chance.
Fantôme toujours présent : λ « habite » jusqu'à 0,58 (écho, g29), 0,25-0,37 (hostile), sans coût.

Calibration : 2/2, Brier 0,066. Cumul 31 prédictions : 0,216.
Motif confirmé : prédictions de SENS ou de réplication — bonnes ; prédictions d'AMPLEUR — mauvaises.

Système de référence : Pesée E (datation, fiabilité, retard, un contre tous, désatténuation)
+ Filiation (copie) + Soupçon (compromission locale) + Méprise (forme des erreurs).

## Correction d'instrument (signalée par Khaled) — caches non versionnés
Les caches (/tmp/cache_*) étaient indexés par (monde, graine, système), pas par version du code : un script
corrigé pouvait relire un résultat écrit par l'ancien code et l'afficher comme neuf. Le recalcul de H37
publié plus haut n'en dépendait pas (script autonome, relancé de zéro), mais test_soupcon.py corrigé, lui,
aurait relu l'ancienne métrique. Correctif : cache.py — le répertoire porte l'empreinte SHA-256 du code
source de toutes les dépendances et du script appelant. Relance de test_soupcon.py sur cache neuf
(/tmp/cache_soupcon_86f5bdde79d1) : résultats identiques au verdict H-Soupçon ; par graine, précision
100 / 100 / 100 %, rappel 90 / 87 / 87 %, rappel sur candidats 96 / 96 / 95 %.

## H-ÉchoMenteur (écrite le 2026-10-08 à 16:23 UTC, avant toute modification de monde.py)

Interaction : un menteur stratégique RECOPIÉ par une chambre d'écho. Le mensonge devient « corroboré ».
Sources : Le Registre 0,90 (0,25) et La Gazette 0,80 (0,25), honnêtes et indépendants ; Le Notable 0,95
(0,40), menteur constant sur 15 % des faits ; Le Relais et L'Écho (0,35 chacun) recopient Le Notable
80 % du temps — mensonges compris — et sont fiables à 0,90 sinon. Erreurs uniformes, pas de retard.
Sur un fait ciblé, les énoncés mensongers sont environ deux fois plus nombreux que les vrais.
Le plafond connaît les deux mécanismes. Système testé : la référence (Méprise).
Mécanisme redouté : circularité — si le mensonge est cru, les copies paraissent dire vrai, la copie
n'est pas détectée, les copies corroborent, le mensonge est cru davantage.

Graines neuves 30, 31, 32. Cache versionné.
- H48 global : plafond − référence significativement positif (borne basse > 0)              — 60 %
- H49 la Filiation rattache Le Relais ET L'Écho au Notable, 3 graines sur 3                    — 55 %
- H50 Soupçon : rappel des couples (Notable, fait ciblé) ≥ 50 % (moyenne)                      — 50 %  [ampleur]
- H51 faits ciblés : plafond − référence significativement positif (IC en grappes par fait)    — 65 %
- H52 global : référence ≥ majorité + 10 points                                               — 85 %  [ampleur]

### Verdict H-ÉchoMenteur (graines 30-32, une exécution, cache /tmp/cache_echo_menteur_1fcfb0e1ee4b) — le danger ne s'est pas matérialisé

Global : majorité 63,0 % ; référence 92,0 % ; plafond 91,9 %.
Faits ciblés × époques : majorité **27,7 %** (le mensonge corroboré gagne le vote) ; référence 80,9 % ; plafond 81,5 %.

| | observé | proba | |
|---|---|---|---|
| H48 plafond − référence > 0 (global) | −0,2 ± 0,5 | 60 % | ✗ |
| H49 copieurs rattachés au Notable 3/3 | 3/3, taux 0,76-0,79 (vrai 0,8) | 55 % | ✓ |
| H50 rappel Soupçon ≥ 50 % | 90 / 93 / 81 % (précision 100 / 100 / 95 %) | 50 % | ✓ |
| H51 plafond − référence > 0 (faits ciblés) | +0,6 ± 0,9 (borne basse −0,3 ; 94 faits) | 65 % | ✗ |
| H52 référence ≥ majorité + 10 | +29,0 ± 2,6 | 85 % | ✓ |

Les organes coopèrent sans une ligne de code supplémentaire : la référence égale le plafond.
Pourquoi la circularité redoutée ne s'est pas formée : la copie est un comportement GLOBAL (les
copieurs recopient tout, sur 85 % de faits non ciblés où les croyances sont saines), tandis que le
mensonge est LOCAL (15 % des faits). La Filiation apprend « qui recopie qui » là où les données sont
propres, puis l'applique là où elles sont sales ; le Soupçon ne voit plus alors qu'un menteur isolé.

Calibration : 3/5, Brier 0,252. Cumul 36 prédictions : 0,221. Mes deux échecs sont mes deux prédictions
de DANGER : j'ai imaginé la circularité sans mesurer d'où vient le signal de copie.

Danger suivant, déduit de ce mécanisme (non testé) : une chambre d'écho COMPLICE, qui ne recopie le
menteur QUE sur ses cibles et reste indépendante partout ailleurs. Le signal global de copie disparaît.

## H-Complices (écrite le 2026-10-08 à 17:40 UTC, avant toute modification de monde.py)

Monde « complice » : coordination, pas copie. Le Notable 0,95 (0,40) ment avec constance sur 15 % des faits.
Le Relais et L'Écho (0,35 chacun) affirment EXACTEMENT le même mensonge sur ces mêmes faits, et sont des
témoins honnêtes et indépendants (0,90) partout ailleurs — ils ne recopient rien. Le Registre 0,90 (0,25)
et La Gazette 0,80 (0,25) sont honnêtes. Sur un fait ciblé, ~2,6 énoncés mensongers pour 1 vrai.
Le plafond connaît la coalition et la proportion de faits ciblés (pas les cibles).

Argument (structurel, pas une spirale imaginée) : le Soupçon n'envisage qu'UNE source compromise par fait.
Une coalition de trois n'a pas de place dans son espace d'hypothèses. Et la Filiation ne verra pas de
copie : hors des cibles, les complices sont indépendants ; sur les cibles, la part de faits (15 %)
reste sous son seuil, et si le mensonge est cru, l'accord paraît un accord sur la vérité.
Mes deux dernières prédictions de danger ont échoué ; celle-ci repose sur une impossibilité, pas une ampleur.

Graines neuves 33, 34, 35. Cache versionné.
- H53 faits ciblés : plafond − référence significativement positif (IC en grappes par fait)       — 75 %
- H54 la Filiation ne rattache NI Le Relais NI L'Écho au Notable, sur ≥ 2 graines sur 3              — 70 %
- H55 global : plafond − référence significativement positif                                       — 65 %
- H56 global : référence ≥ majorité + 10 points                                                     — 80 %  [ampleur]
- H57 la fiabilité apprise des complices reste ≥ 0,85 (leur honnêteté ailleurs les protège)         — 60 %  [ampleur]

### Verdict H-Complices (graines 33-35, une exécution, cache /tmp/cache_complice_f8499560aae7) — casse majeure, et retournement

Global : majorité 61,6 % ; référence 83,6 % ; plafond 92,6 % (écart +9,0 ± 1,9).
Faits ciblés × époques : majorité 10,7 % ; référence **7,4 %** ; plafond 75,6 % (écart +68,2 ± 7,7 ; 70 faits).

| | observé | proba | |
|---|---|---|---|
| H53 faits ciblés, écart significatif | +68,2 ± 7,7 | 75 % | ✓ |
| H54 complices non rattachés au Notable ≥ 2/3 | aucun parent, 3/3 | 70 % | ✓ |
| H55 global, écart significatif | +9,0 ± 1,9 | 65 % | ✓ |
| H56 référence ≥ majorité + 10 | +22,0 ± 2,3 | 80 % | ✓ |
| H57 fiabilité des complices ≥ 0,85 | 0,89-0,93 | 60 % | ✓ |

Forme de la casse — RETOURNEMENT DU SOUPÇON : sur les faits ciblés, le Soupçon ne marque pas le menteur
(précision 0 / 0 / 29 %, rappel 0 / 0 / 15 %) : il marque LE REGISTRE et LA GAZETTE. Face à trois sources
qui disent la même chose, l'explication « exactement une source ment » la plus probable est que le témoin
honnête isolé est le menteur. L'outil anti-mensonge est retourné contre ceux qui disent vrai.
Réputations : honnêtes dépréciés (Registre 0,84-0,85 au lieu de 0,90 ; Gazette 0,73-0,74 au lieu de 0,80),
coalition intacte (Notable 0,96 ; complices 0,90-0,93). La référence fait PIRE que la majorité sur les cibles.

[AFFIRMATION RETIRÉE — fausse, réfutée par la mesure ci-dessous] « Plafond à 75,6 % : là où la vérité ne change
jamais, une coalition constante est indiscernable d'une majorité honnête ; seuls les faits qui changent la trahissent. »

Calibration : 5/5, Brier 0,095. Cumul 41 : 0,206. Précision de mon modèle de moi-même : les prédictions
fondées sur une IMPOSSIBILITÉ dans l'espace des hypothèses tiennent ; celles fondées sur une spirale
imaginée, non.


### Correction (mesure, graines 33-35) — ce qui rend la coalition détectable n'est pas le temps
Plafond sur faits ciblés : vérité immobile (14 faits) 90 % ; vérité qui change (56 faits) 72 %.
L'affirmation précédente était l'inverse de la réalité. Ce que le plafond exploite, c'est de SAVOIR QUI
appartient à la coalition : connaissant le bloc, un seul conflit suffit à désigner le menteur. Sur les faits
qui changent, il est limité par la rareté des énoncés honnêtes (deux sources, couverture 0,25), pas par
l'indiscernabilité. Deuxième affirmation de mécanisme non mesurée de la session ; à proscrire.
Conséquence : la vraie question est « l'appartenance à la coalition est-elle apprenable sans oracle ? ».
Sans asymétrie entre les deux blocs, non : deux camps qui s'opposent sur les mêmes faits sont symétriques.

## Exploration préalable au Litige (graines VUES : complice 33, menteur 18, facile 0, hostile 0, écho 0, plausible 9, écho-menteur 30)
- v1 « deux camps constants » : ZÉRO litige détecté, y compris chez les complices. Les honnêtes rapportent une
  vérité qui bouge : ils ne forment jamais un camp figé. La définition encodait une fausse symétrie.
- v2 « bloc figé contre dissidents » : complices 11/22 faits ciblés détectés, sûr-et-faux 90,5 → 39,3 % ;
  mais 20 faux litiges dans le monde écho (La Dépêche et ses copieurs forment un « bloc »), et du doute ajouté
  là où la Filiation avait déjà tranché (écho-menteur : exactitude ciblés 84,6 → 82,9 %).
- v3 « une voix répétée reste une voix » (bloc et dissidents comptés après fusion des copieurs avec leur
  source) : faux litiges écho 20 → 3-5 ; écho-menteur 20 → 2, sans coût. Dissidents à ≥ 1 énoncé (total ≥ 3) :
  complices 14/22, sûr-et-faux 90,5 → 25,0 %, Brier ciblés 0,905 → 0,420. Ailleurs : ΔBrier ≤ 0,001.

## H-Litige (écrite le 2026-10-08 à 19:43 UTC, avant toute ligne de litige.py)

Spécification (v3 de l'exploration, figée) :
- Litige sur un fait si : un BLOC d'au moins deux sources effectives (copieurs fusionnés avec leur source
  détectée) est figé (≥ 80 % de ses énoncés, au moins 2 chacune) sur une valeur v, ET au moins deux
  DISSIDENTS effectifs (≥ 1 énoncé chacun, majoritairement ≠ v, au moins 3 énoncés au total).
- Effet : la croyance sur ce fait devient le mélange à parts ÉGALES de « le bloc ment » (énoncés du bloc
  retirés) et « les dissidents mentent » (énoncés des dissidents retirés). Le Litige n'accuse personne,
  ne modifie ni réputations ni apprentissage : il s'applique après la Méprise, sur ses croyances finales.
- Division du travail : un menteur isolé relève du Soupçon ; le Litige ne traite que les blocs ≥ 2.

Graines neuves 36, 37, 38. Comparaisons appariées sur le MÊME entraînement (Méprise, puis Méprise + Litige).
« Sûr-et-faux » = confiance ≥ 0,8 et réponse fausse. IC en grappes par fait.
- H58 [sens]   complices, faits ciblés : sûr-et-faux significativement réduit                    — 85 %
- H59 [ampleur] complices, faits ciblés : sûr-et-faux ≤ 40 % (Méprise ≈ 90 %)                      — 60 %
- H60 [sens]   complices, Brier par question : significativement meilleur                         — 70 %
- H61 [sens]   aucune régression dans facile, hostile, écho, menteur, plausible, écho-menteur :
               exactitude non significativement plus basse ET Brier non significativement pire     — 60 %
- H62 [sens]   complices, faits ciblés : exactitude NON significativement changée (le Litige doute,
               il ne choisit pas)                                                                  — 70 %
Règle : le Litige est adopté si et seulement si H58, H60 et H61 passent.

### Verdict H-Litige (graines 36-38, une exécution, cache /tmp/cache_litige_209d619cc4f9) — REJETÉ par la règle

| | observé | type | proba | |
|---|---|---|---|---|
| H58 complices : sûr-et-faux réduit | 94,3 → 44,4 % (Δ −49,9 ± 11,1) | sens | 85 % | ✓ |
| H59 complices : sûr-et-faux ≤ 40 % | 44,4 % | ampleur | 60 % | ✗ |
| H60 complices : Brier meilleur | 0,161 → 0,111 (Δ −0,050 ± 0,010) | sens | 70 % | ✓ |
| H61 aucune régression | exactitude : aucune baisse significative ; Brier : menteur PIRE, +0,0020 ± 0,0013 [+0,0008 ; +0,0033] | sens* | 60 % | ✗ |
| H62 complices : exactitude ciblés inchangée | 4,9 → 7,6 % (Δ +2,7 ± 1,7, significatif) | sens* | 70 % | ✗ |

Décision, selon la règle (H58, H60, H61) : le Litige N'EST PAS adopté.

Lecture honnête :
- Là où il le doit, il fait ce qu'on voulait : moitié moins de réponses sûres et fausses, Brier −31 %,
  exactitude même légèrement meilleure.
- La régression du monde menteur est minuscule (0,002 de Brier) mais systématique. Sa cause : la règle
  assouplie « un dissident peut n'avoir parlé qu'une fois », choisie en exploration pour le rappel. Un honnête
  avec UNE erreur devient dissident, s'allie au menteur isolé, et le Litige doute là où le Soupçon avait raison.
  Le signal ÉTAIT dans l'exploration (menteur g18, Brier ciblés 0,057 → 0,063) ; je l'ai résumé à tort en
  « ΔBrier ≤ 0,001 ailleurs ». Je l'ai vu et minimisé.
- Graine 36 : zéro litige sur 32 faits ciblés. Cause mesurée : la Filiation a accusé LA GAZETTE de recopier
  LE REGISTRE (0,32, juste au-dessus du seuil). Sur les faits ciblés, les deux honnêtes s'accordent sur une
  vérité que les croyances tiennent pour fausse : leur accord ressemble à une copie. Les dissidents fusionnent
  alors en une seule voix, et le Litige ne voit plus de litige. La coalition a fait passer les honnêtes pour
  une chambre d'écho : deuxième retournement d'une défense contre ceux qui disent vrai.

Calibration : 2/5, Brier 0,265. Cumul 46 : 0,212.
(*) Correction de mon propre étiquetage : H61 et H62 prédisent une ABSENCE d'effet. Ce sont des prédictions
d'ampleur déguisées (« l'effet est plus petit que ce qu'on peut détecter »). Reclassées, mes prédictions de
sens réelles (H58, H60) passent toutes les deux.

## Exploration du monde à contraintes (graines d'exploration 39-40 ; aucune hypothèse testée)
Contrainte unique : « qui dirige une organisation y travaille ». Vérité vérifiée cohérente (0 violation).
Coalition naïve (complices, mensonges indépendants de la contrainte).
1. Exposition : seuls 17 % (g39) et 33 % (g40) des faits ciblés × époques touchent la contrainte. Les mensonges
   sur « habite » ne contredisent rien : aucun graphe ne les verra tant qu'aucune contrainte ne les relie.
2. Un pas de passage de messages (« Bob dirige X » ↔ « Bob travaille chez X ») : faits ciblés exposés
   0 → 29 % (g39), 0 → 9 % (g40). Mais faits NON ciblés 96,8 → 95,9 % (g40) : la contrainte PROPAGE le mensonge
   (si la coalition fait croire « Bob dirige X », elle pousse aussi à croire « Bob travaille chez X »).
   Monde honnête : 91,0 → 91,9 % (la cohérence aide quand personne ne ment en bloc).
3. Auto-contradiction (une même source dit « p dirige X » et « p travaille ailleurs », ±1 époque) :
   coalition 30-54 % ; honnêtes 18-47 % ; monde honnête 18-60 %. Le taux brut NE SÉPARE PAS : une source
   honnête se contredit à proportion de ses erreurs (≈ 1 − f² attendu). Le signal n'existe qu'en EXCÈS sur ce
   que la fiabilité prédit — exploitable seulement par une inférence jointe des faits liés, pas par un compte.
Conclusion provisoire : le graphe apporte une information que la coalition ne contrôle pas, mais (a) seulement
là où des contraintes existent, (b) elle se propage dans les deux sens, (c) l'exploiter demande une inférence
JOINTE probabiliste, pas un module de règles.

## Gel de la grille de densité (2026-10-08 à 20:41 UTC, avant tout code de génération)
Grille figée (CHARTE.md §8) : d0, d1, d2, d3 × coalition naïve / coalition cohérente. Graines neuves ≥ 45.
Requalification validée par Khaled : il s'agit d'une « échelle de mondes synthétiques à contraintes imbriquées ».
Les conclusions porteront sur cette progression (emploi → siège → résidence → couple), pas sur la densité seule,
car chaque niveau ajoute aussi des familles de relations. Les contraintes de d2 et d3 sont des régularités
contingentes, dures par construction : aucune conclusion ne vaut pour des contraintes souples du réel.
Variante « densité seule » consignée comme possible, non figée.

## Gel du menteur cohérent (2026-10-08 à 20:51 UTC, avant tout code)
Validé par Khaled : le menteur connaît les contraintes déclarées et choisit la façon cohérente qui lui coûte le moins.
Borne de Khaled : faits ciblés tirés une fois par graine, identiques aux quatre niveaux ; seule la fausse valeur
est choisie, pour minimiser les falsifications SUPPLÉMENTAIRES. Aucun autre adversaire, aucune complexification.

### Points soumis à validation avant code (découverts en spécifiant le menteur)
1. ERREUR DE LA CHARTE : « K(d) croît par construction » est faux pour un menteur qui minimise son coût. À d1, nommer
   comme dirigeant quelqu'un qui travaille déjà dans l'organisation ne coûte rien ; le menteur exploite la structure
   existante. K n'est donc pas tautologique.
2. AFFIRMATION VIDE : « part des mensonges maintenables sans contradiction » vaut 100 % par définition (le menteur
   peut toujours falsifier assez de faits liés). Proposition : mesurer le PRIX — F(d) = part des mensonges gratuits
   (zéro falsification supplémentaire) ; K(d) = falsifications supplémentaires moyennes par fait ciblé.
   Affirmation falsifiable : F décroît et K croît le long de l'échelle — ou non.
3. PROPOSITION DE GÉNÉRATION : un seul monde par graine, identique à tous les niveaux (même vérité, respectant toutes
   les contraintes ; mêmes familles de relations partout) ; seules varient les contraintes DÉCLARÉES. La comparaison
   entre niveaux ne mélangerait plus deux mondes différents. Ne modifie pas la grille d0-d3.

## Validation des trois points (Khaled, 2026-10-08) — figés
1. Correction de la charte sur K. 2. F(d) et K(d) remplacent le critère vide. 3. Un monde et des cibles fixes par
graine ; seules varient les contraintes connues du menteur et du graphe. Borne de formulation : effet d'une
information structurelle déclarée croissante dans ce monde synthétique ; ni loi générale, ni preuve sur le réel.

## Découverte en spécifiant (avant tout code) — la monotonie faible est un théorème
Monde unique + cibles fixes + contraintes emboîtées (d0 ⊂ d1 ⊂ d2 ⊂ d3) : tout mensonge cohérent à d(k+1) l'est à
d(k), donc pour chaque cible coût_min(d(k+1)) ≥ coût_min(d(k)). « F décroît, K croît » au sens faible est garanti.
Ce n'est plus une hypothèse : c'est un contrôle de code (une seule violation = bogue). Restent falsifiables :
la progression STRICTE (significative) et l'AMPLEUR.

## Spécification du monde à contraintes imbriquées (figée avant tout code)
Entités : 80 personnes, 24 organisations, 6 quartiers, 12 époques (comme ailleurs).
Relations présentes à TOUS les niveaux : habite, travaille, dirige, naissance, + siège (organisation → quartier,
fixe dans le temps), + conjoint (personne → personne, symétrique, fixe ; 50 % des personnes en couple).
Vérité, à chaque époque, respectant toutes les contraintes :
  C1 dirige(o) = p ⇒ travaille(p) = o ;
  C2 dirige(o) = p ⇒ habite(p) = siège(o) ;
  C3 conjoint(p) = q ⇒ habite(p) = habite(q).
Dynamique : dirigeants renouvelés comme dans le monde à contraintes ; un dirigeant et son conjoint habitent le
quartier du siège ; on n'appointe pas quelqu'un dont le conjoint dirige déjà ; les autres déménagent (en couple,
ensemble) et changent d'emploi selon les taux habituels.
Niveaux : d0 aucune contrainte déclarée ; d1 {C1} ; d2 {C1, C2} ; d3 {C1, C2, C3}.
Sources : celles du monde « complice » (Registre 0,90 ; Gazette 0,80 ; coalition Notable 0,95 + Relais, Écho 0,90).
Cibles : 15 % des faits (habite, travaille, dirige), tirées par un générateur dédié : IDENTIQUES aux quatre niveaux.

Menteur naïf : valeur fausse constante, tirée au hasard (≠ vérité à l'époque 0).
Menteur cohérent : pour chaque cible, il choisit la valeur constante v (≠ vérité à l'époque 0) qui minimise
Σ_époques coût_t(v), où coût_t(v) = nombre minimal de faits (de l'époque t, autres que la cible) à falsifier pour que
le monde de l'époque t respecte les contraintes déclarées. Recherche exacte jusqu'à B = 4 falsifications par époque ;
au-delà, l'époque est comptée « intenable » (coût B + 1). Chaque cible est évaluée ISOLÉMENT (le reste du monde vrai).

Grandeurs, graines neuves 45 à 49, intervalles par bootstrap sur les cibles (appariés entre niveaux) :
E(d) ; F(d) ; K(d) ; part d'époques intenables.

## H-Échelle (écrite le 2026-10-08 à 21:02 UTC, avant toute ligne de code et toute graine)
Contrôle (théorème) : pour chaque cible, coût_min non décroissant de d0 à d3. Une violation = bogue, test invalidé.
- H63 [sens, stricte]  F(d1) − F(d3) significativement > 0                                        — 85 %
- H64 [ampleur]        F(d3) ≤ 30 %                                                               — 50 %
- H65 [ampleur]        K(d2) − K(d1) ET K(d3) − K(d2) significativement > 0 (chaque marche coûte)  — 60 %
- H66 [ampleur]        E(d3) ≥ 50 % (un mensonge naïf contredit le plus souvent une contrainte)    — 55 %
- H67 [instrument]     époques intenables ≤ 5 % à d3 ; sinon K est rapporté comme borne inférieure — 75 %
Aucune règle d'adoption : c'est une mesure du monde, pas d'un organe.

## Contrôles d'implémentation (graine de DÉVELOPPEMENT 44 ; ni F ni K affichés)
- Vérité : C1, C2, C3 respectées à toutes les époques. Cibles identiques à la régénération (21 cibles).
- Théorème de monotonie : 0 violation sur 21 cibles.
- Recherche par classes équivalentes vs énumération complète des remplaçants (borne 3, d3) : 0 écart sur 126 cas.
- Détail d'implémentation non écrit dans la spécification : dissoudre un couple (2 faits) est une réparation
  permise pour C3 — c'est ce qu'un menteur minimisant son coût ferait ; le siège peut être falsifié époque par
  époque (sa stabilité dans le temps n'est pas une contrainte déclarée).

### Verdict H-Échelle (graines neuves 45-49, 136 cibles, cache /tmp/cache_echelle_c5e9e510c6c7)
Formulation (borne de Khaled) : effet d'une information structurelle déclarée croissante dans CE monde synthétique.

| niveau | E(d) mensonge naïf exposé | F(d) mensonges gratuits | K(d) falsifications supplémentaires |
|---|---|---|---|
| d0 | 0,0 % | 100,0 % | 0,00 |
| d1 | 21,1 % [14,7 ; 27,6] | 76,5 % [69,9 ; 83,1] | 1,96 [1,29 ; 2,63] |
| d2 | 33,2 % [26,0 ; 40,4] | 64,0 % [55,9 ; 72,1] | 4,56 [3,40 ; 5,74] |
| d3 | 46,4 % [38,5 ; 54,0] | 48,5 % [39,7 ; 57,4] | 7,20 [5,70 ; 8,65] |

| | observé | type | proba | |
|---|---|---|---|---|
| Contrôle (théorème) | 0 violation sur 136 cibles | — | — | ✓ |
| H63 F(d1) − F(d3) > 0 | +27,9 % [+20,6 ; +36,0] | sens | 85 % | ✓ |
| H64 F(d3) ≤ 30 % | 48,5 % | ampleur | 50 % | ✗ |
| H65 chaque marche coûte | K +2,60 [+1,90 ; +3,32] puis +2,64 [+1,69 ; +3,71] | ampleur | 60 % | ✓ |
| H66 E(d3) ≥ 50 % | 46,4 % [38,5 ; 54,0] | ampleur | 55 % | ✗ |
| H67 intenables ≤ 5 % | 0,0 % | instrument | 75 % | ✓ |

Descriptif par relation (F : d0 → d1 → d2 → d3 ; K idem) :
  dirige (n = 11)    F 100 → 9 → 9 → 9 %     K 0 → 3,5 → 9,0 → 9,0
  habite (n = 62)    F 100 → 100 → 73 → 39 % K 0 → 0 → 2,7 → 8,5
  travaille (n = 63) F 100 → 65 → 65 → 65 %  K 0 → 3,6 → 5,7 → 5,7
Chaque marche ne protège que la famille de faits qu'elle touche : C1 rend presque tout mensonge sur « dirige »
coûteux dès d1 ; C3 ne protège que « habite » ; l'emploi des non-dirigeants n'est touché par aucune contrainte,
et 65 % de ces mensonges restent gratuits jusqu'en haut de l'échelle. Au sommet, un mensonge sur deux reste
gratuit pour un menteur qui choisit bien sa fausse valeur.

Réserves : intervalles par bootstrap sur les cibles, supposées indépendantes alors que les cibles d'une même
graine partagent un monde (5 graines seulement) — les intervalles sont probablement un peu optimistes.
Chaque cible est évaluée isolément (réparations partagées entre mensonges ignorées).

Calibration : 3/5, Brier 0,160. Cumul 51 prédictions : 0,207. Mes deux échecs sont, encore, des ampleurs.

# PAUSE — point de reprise
Décision (Khaled) : pause ici ; pas d'organe de Cohérence tant que le rôle de la couverture n'est pas isolé.
Prochaine étape : variante « densité seule » — mêmes familles de relations, même monde, seule varie la COUVERTURE
des contraintes. Avant tout code : définir la couverture, figer la grille, pré-enregistrer (graines neuves ≥ 50).
Rappel : si les niveaux de couverture sont emboîtés, la monotonie faible sera à nouveau un théorème ; seules la
progression stricte et l'ampleur seront falsifiables.
Système de référence : Méprise (Pesée E → Filiation v3 → Soupçon → Méprise). Rejetés et limites : CHARTE.md.

# Fil « ancres et révision » (décidé après la pause ; la variante « densité seule » reste en attente)

## H-Ancres (écrite le 2026-10-11 à 20:55 UTC, avant toute ligne de code)
Question : combien de faits vérifiés de l'extérieur faut-il pour casser une coalition, et les organes actuels
généralisent-ils quelques ancres aux autres mensonges de la coalition ?
Monde : « complice » (coalition Notable + Relais + Écho ; Registre et Gazette honnêtes). Graines neuves 50, 51, 52.
Ancre : source « L'Ancre », fiabilité FIXÉE à 0,99 (jamais apprise), retard 0, jamais candidate au Soupçon ni à
la Filiation ; pour chaque fait ancré, elle donne la vraie valeur à chacune des 12 époques.
Choix des ancres : parmi les faits CIBLÉS (cas le plus favorable à la généralisation : si rien ne transfère
ici, rien ne transférera avec des ancres tirées au hasard). Ordre des cibles tiré une fois par graine
(générateur dédié) ; niveaux emboîtés : 0 %, 10 %, 25 %, 50 % des cibles ancrées.
Système : la référence (Méprise) + une seule capacité nouvelle, « sources fixes » (fiabilité figée ; exclues du
Soupçon et de la Filiation). Sans source fixe, le système doit rester identique (non-régression).
Mesures (faits × époques, IC en grappes par fait, comparaisons appariées sur les MÊMES faits) :
- H68 [instrument] faits ancrés : exactitude ≥ 90 % à chaque niveau > 0                                   — 85 %
- H69 [ampleur : absence d'effet] faits ciblés NON ancrés à 50 % : exactitude(50 %) − exactitude(0 %)
       NON significativement > 0 (les ancres ne se généralisent pas)                                       — 70 %
- H70 [sens] fiabilité moyenne apprise des trois membres de la coalition plus basse à 50 % qu'à 0 %,
       sur chacune des trois graines                                                                       — 70 %
- H71 [sens] erreur |f appris − f vrai| des deux honnêtes plus basse à 50 % qu'à 0 %, sur chacune des graines — 65 %
- H72 [ampleur : absence d'effet] faits non ciblés : exactitude(50 %) − exactitude(0 %) non significativement < 0 — 75 %
Règle : la capacité « sources fixes » est conservée si H68 et H72 passent.

### Verdict H-Ancres (graines neuves 50-52, une exécution, cache /tmp/cache_ancres_bc4b756a6fcf) — LES ANCRES SE GÉNÉRALISENT

| ancrage | ancres | faits ancrés | faits ciblés non ancrés | non ciblés | f coalition / honnêtes |
|---|---|---|---|---|---|
| 0 % | 0 | — | 7,5 % | 97,7 % | 0,922 / 0,779 |
| 10 % | 9 | 98,1 % | 17,6 % | 97,6 % | 0,902 / 0,793 |
| 25 % | 22 | 98,9 % | 46,0 % | 97,5 % | 0,877 / 0,813 |
| 50 % | 43 | 99,4 % | 43,3 % | 97,5 % | 0,875 / 0,830 |

| | observé | type | proba | |
|---|---|---|---|---|
| H68 faits ancrés ≥ 90 % | 98,1 / 98,9 / 99,4 % ; l'ancre n'est jamais soupçonnée | instrument | 85 % | ✓ |
| H69 pas de généralisation | +35,3 ± 13,1 points sur les MÊMES 42 faits non ancrés | ampleur (absence) | 70 % | ✗ |
| H70 coalition dépréciée, 3/3 | 0,917 → 0,901 ; 0,930 → 0,865 ; 0,919 → 0,859 | sens | 70 % | ✓ |
| H71 honnêtes mieux estimés, 3/3 | erreur 0,050 → 0,017 ; 0,101 → 0,041 ; 0,061 → 0,003 | sens | 65 % | ✓ |
| H72 pas de perte hors cibles | −0,22 ± 0,21 point (borne haute −0,01) | ampleur (absence) | 75 % | ✗ |

Décision, selon la règle (H68 et H72) : la capacité « sources fixes » N'EST PAS conservée.

Lecture honnête :
- Le résultat principal contredit ma prédiction : quelques ancres sur des mensonges de la coalition améliorent
  l'exactitude sur les AUTRES mensonges (7,5 → 43 %). Le mécanisme n'est PAS établi. Candidats, non mesurés :
  baisse globale de la réputation de la coalition ; réputations honnêtes restaurées qui rendent au Soupçon
  sa capacité de désigner le bon camp. À mesurer avant d'en dire plus.
- La perte hors cibles est minuscule (−0,22 point) mais significative. Piste, non mesurée : la coalition est
  punie GLOBALEMENT (0,87 au lieu de 0,90-0,95 hors cibles), donc son témoignage honnête ailleurs est sous-pesé.
  Le même défaut que le Soupçon corrigeait : une réputation globale là où il faudrait une défiance locale.
- Défaut de MÉTHODE révélé (à corriger pour l'avenir, sans effet rétroactif) : un garde-fou formulé « non
  significativement négatif » devient impossible à passer avec assez de données, quel que soit l'effet. Il faut
  une MARGE de non-infériorité fixée d'avance (ex. : perte < 0,5 point), comme dans les essais cliniques.
  Les deux échecs « d'absence d'effet » de cette série relèvent de ce défaut ou de mon ampleur mal prédite.

Calibration : 3/5, Brier 0,258. Cumul 56 : 0,212. Les deux échecs sont des prédictions d'absence d'effet.

## H-Mécanisme-ancres (écrite le 2026-10-11 à 21:56 UTC, avant tout calcul)
Question : POURQUOI quelques ancres améliorent-elles les mensonges non ancrés (+35 points, H-Ancres) ?
Méthode — décomposition par GREFFE de paramètres : on entraîne le système sans ancre (0 %) et avec ancres (50 %)
sur la même graine ; puis on greffe dans le modèle 0 % tout ou partie des paramètres appris par le modèle 50 %,
et on recalcule ses croyances (étape E seule). Sur les faits ciblés NON ancrés, les énoncés sont identiques dans
les deux corpus : seule la greffe peut expliquer une différence. Greffes : fiabilités (f) ; propensions au
mensonge du Soupçon (q) ; filiations (parents et taux de copie) ; tout (f, q, filiations, retards, taux de
changement, forme des erreurs).
Calcul préalable (avant mesure) : un simple glissement de réputation (coalition 0,92 → 0,875, honnêtes 0,78 → 0,83)
laisse encore à la coalition ~3 fois plus de poids sur un fait ciblé : il ne devrait pas suffire.
Mécanisme suspecté : les ancres transforment les accords de la coalition en ERREURS PARTAGÉES, signal de la
Filiation, qui traite alors les complices comme des copies (une seule voix) que le Soupçon peut isoler.
Graines 50-52 (celles du phénomène à expliquer) ; réplication du phénomène sur graines NEUVES 53-55.
- H73 [instrument] la greffe « tout » reproduit le modèle 50 % sur les faits non ancrés, à ±2 points       — 90 %
- H74 [sens] la greffe des filiations seules récupère plus du gain que la greffe des fiabilités seules        — 60 %
- H75 [sens] dans le modèle 50 %, Le Relais et L'Écho ont un parent détecté dans la coalition (≥ 2 graines sur 3) — 60 %
- H76 [ampleur] la greffe des filiations seules récupère ≥ 50 % du gain                                    — 45 %
- H77 [sens] réplication sur 53-55 : gain sur les faits ciblés non ancrés (50 % − 0 %) significativement > 0    — 80 %

### Verdict H-Mécanisme-ancres (cache /tmp/cache_mecanisme_ancres_3892821b2258)

Faits ciblés non ancrés, graines 50-52 : sans ancre 7,9 % ; avec 50 % d'ancres 43,3 % (gain +35,3).
| greffe dans le modèle sans ancre | exactitude | part du gain |
|---|---|---|
| fiabilités seules | 7,9 % | +0 % |
| propensions au mensonge seules | 8,3 % | +1 % |
| filiations seules | 23,0 % | +43 % |
| tout | 43,3 % | +100 % |

| | observé | type | proba | |
|---|---|---|---|---|
| H73 « tout » reproduit le modèle ancré ±2 pts | 43,3 % = 43,3 % | instrument | 90 % | ✓ |
| H74 filiations > fiabilités | 43 % contre 0 % du gain | sens | 60 % | ✓ |
| H75 Relais et Écho rattachés au Notable ≥ 2/3 | g50 non ; g51 oui (0,53-0,54) ; g52 oui (0,47-0,53) | sens | 60 % | ✓ |
| H76 filiations seules ≥ 50 % du gain | 43 % | ampleur | 45 % | ✗ |
| H77 réplication sur graines neuves 53-55 | 3,4 → 65,8 % ; +62,4 ± 11,5 (47 faits) ; complices rattachés 3/3 | sens | 80 % | ✓ |

Établi (dans ce monde) : le glissement de réputation n'explique RIEN du gain. Le levier principal identifié est
la Filiation : sans ancre, elle ne voit aucune copie ; avec des ancres, les accords de la coalition sur des valeurs
reconnues fausses deviennent des erreurs partagées, et les complices sont rattachés au Notable (une seule voix).
Les 57 % restants viennent d'effets CONJOINTS des paramètres, non décomposés ici (aucune greffe isolée hors
filiations ne pèse) — non établi.
Observation : graine 54, le modèle sans ancre accusait La Gazette de recopier Le Registre (0,36) ; avec les ancres,
cette fausse accusation disparaît et la vraie coordination est détectée. Les ancres corrigent l'inversion.
Descriptif : hors cibles, la greffe des fiabilités seules fait passer 97,75 → 97,62 % (perte totale du modèle ancré :
97,52 %) — compatible avec l'hypothèse d'une punition globale de la coalition, non établi.
Réserve : la coalition de ce monde répète exactement le MÊME mensonge ; une coalition qui coordonnerait des
mensonges différents ne partagerait pas d'erreurs — mais ne se renforcerait pas non plus.

Calibration : 4/5, Brier 0,115. Cumul 61 : 0,204.

## Précision d'attribution (relecture avec Khaled)
La capacité des ancres a été rejetée par H72 (garde-fou sans marge), PAS par H76. H76 (43 % < 50 %) porte sur le
mécanisme — la part du gain expliquée par la Filiation seule — et non sur l'efficacité des ancres, établie par
H69 (puis H77). Aucune requalification de l'un ou l'autre essai.

## H-Ancres-confirmation (écrite le 2026-10-11 à 22:33 UTC, avant toute exécution)
Périmètre PRÉCIS : monde « complice » ; ancres = source à fiabilité fixe 0,99 donnant la vraie valeur à chaque
époque ; ancres choisies PARMI LES FAITS CIBLÉS (sélection idéale, irréaliste) ; 50 % des cibles ancrées.
Rien de ce test ne couvre une sélection réaliste des ancres (objet du test suivant).
Marge de non-infériorité : 0,5 point, fixée avant le test. Justifications : (1) inférieure à la plus petite
demi-largeur d'IC jamais résolue par le banc en exactitude globale (± 0,7) ; (2) au moins dix fois plus petite que
le bénéfice net attendu sur l'ensemble des faits. Critère : borne BASSE de l'IC de (exactitude avec ancres −
exactitude sans) sur les faits non ciblés > −0,5 point.
Graines neuves 56 à 60 (cinq, pour la précision). IC en grappes par fait, appariés sur les mêmes faits.
- H78 [sens] faits ciblés non ancrés : gain significativement > 0 (borne basse > 0)              — 90 %
- H79 [ampleur, non-infériorité] faits non ciblés : borne basse de la différence > −0,5 point    — 70 %
- H80 [instrument] faits ancrés : exactitude ≥ 90 %                                              — 90 %
Règle : l'usage des ancres entre dans la référence, POUR CE PÉRIMÈTRE SEULEMENT, si H78, H79 et H80 passent.

### Verdict H-Ancres-confirmation (graines neuves 56-60, cache /tmp/cache_ancres_confirmation_966f2e43928c)
| | observé | type | proba | |
|---|---|---|---|---|
| H78 gain sur ciblés non ancrés | +29,0 ± 10,1 (borne basse +18,8 ; 69 faits) | sens | 90 % | ✓ |
| H79 non-infériorité hors cibles (marge 0,5) | −0,43 ± 0,25 (borne basse −0,68 < −0,50 ; 1 116 faits) | ampleur | 70 % | ✗ |
| H80 faits ancrés ≥ 90 % | 99,9 % ; ancre jamais soupçonnée | instrument | 90 % | ✓ |

Décision : l'usage des ancres N'ENTRE PAS dans la référence, même pour ce périmètre.
La perte hors cibles n'est pas un accident : −0,22 (graines 50-52), −0,43 (graines 56-60). Elle est petite au regard
du gain, mais elle est réelle, et la marge justifiée d'avance ne la couvre pas. Les ancres soignent les faits
ciblés et abîment légèrement les autres : des dégâts collatéraux, au sens exact du test.
Piste de mécanisme (NON établie) : dans H-Mécanisme, la greffe des seules fiabilités expliquait environ la moitié
de la perte ; une autre partie pourrait venir de la Filiation appliquée GLOBALEMENT (les complices, honnêtes hors
cibles, voient leurs accords avec Le Notable escomptés comme des copies même quand tous disent vrai).
Calibration : 2/3, Brier 0,170. Cumul 64 : 0,202.

## H-Collatéral (écrite le 2026-10-11 à 22:50 UTC, avant tout calcul)
Question : d'où vient la perte hors cibles causée par les ancres (−0,43 point, graines 56-60) ?
Méthode : décomposition par greffe (comme H-Mécanisme), mesurée sur les faits NON ciblés, graines 56-60 (celles
du phénomène). Greffes dans le modèle sans ancre : fiabilités (f) ; filiations ; propensions (q) ; f + filiations ;
tout. Diagnostic : parmi les faits × époques justes sans ancre et faux avec ancres, part comportant un énoncé d'un
complice escompté comme copie du Notable (sa valeur égale la dernière valeur dite par Le Notable).
Diagnostic seulement : aucune règle d'adoption.
- H81 [instrument] la greffe « tout » reproduit la perte à ±0,1 point                                   — 90 %
- H82 [sens] la greffe des filiations seules produit une perte (exactitude < sans ancre)                  — 65 %
- H83 [sens] la greffe des fiabilités seules produit une perte                                            — 70 %
- H84 [ampleur] fiabilités + filiations ensemble expliquent ≥ 75 % de la perte                           — 50 %

### Verdict H-Collatéral (graines 56-60, cache /tmp/cache_collateral_6bb83f452b59)
Faits non ciblés × époques : 13 392 ; sans ancre 97,917 % ; avec ancres 97,491 % (perte −0,426).
| greffe | écart à la base | part de la perte |
|---|---|---|
| fiabilités seules | −0,060 | 14 % |
| filiations seules | −0,149 | 35 % |
| propensions seules | 0,000 | 0 % |
| fiabilités + filiations | −0,224 | 53 % |
| tout | −0,426 | 100 % |

| | observé | type | proba | |
|---|---|---|---|---|
| H81 « tout » reproduit la perte ±0,1 | exact | instrument | 90 % | ✓ |
| H82 filiations seules → perte | −0,149 | sens | 65 % | ✓ |
| H83 fiabilités seules → perte | −0,060 | sens | 70 % | ✓ |
| H84 fiabilités + filiations ≥ 75 % | 53 % | ampleur | 50 % | ✗ |

Établi : la Filiation est la plus grande source identifiée de la perte (35 %), comme elle était la plus grande source
identifiée du gain (43 %, H-Mécanisme). Le même levier soigne les faits ciblés et abîme les autres. 47 % de la perte
restent non décomposés (retards, taux de changement, forme des erreurs, interactions).
Observation : dans 3 graines sur 5, la Filiation inverse le sens (« Le Notable recopie L'Écho / Le Relais »). Une
coordination n'a pas de sens ; la Filiation en suppose un.
DIAGNOSTIC RETIRÉ : « 100 % des bascules comportent un énoncé de complice escompté comme copie » ne dit rien —
taux de base mesuré a posteriori sur g56 : 98 % de TOUS les faits non ciblés. Conçu sans point de comparaison.

Calibration : 3/4, Brier 0,118. Cumul 68 : 0,197.

# Fil « où vérifier » — sélection d'information externe sous budget
Décision (avec Khaled) : les ancres restent un outil de recherche, HORS de la référence. Ce test mesure la
SÉLECTION d'information externe ; il ne prouve pas que le système « sait ce qu'il ne sait pas ». Le pont vers
« dire pourquoi » n'est solide que si chaque choix est justifié par des sources, dépendances et contraintes
traçables, enregistrées AU MOMENT du choix.

## H-Sélection (écrite le 2026-10-12 à 06:01 UTC, avant toute ligne de code)
Mondes : complice, menteur, plausible (un sélecteur qui ne reconnaîtrait que les coalitions serait pénalisé ailleurs).
Graines neuves 61, 62, 63. Système : la référence (Méprise) + capacité « sources fixes ».
Vérification : un FAIT (sujet, relation) ; l'ancre (fiabilité fixe 0,99) donne sa vraie valeur aux 12 époques.
Budget : B = 10 faits vérifiés par graine. Candidats : tous les faits (habite, travaille, dirige, naissance).
Bras (sélections calculées sur le modèle SANS ancre de la même graine) :
- ALÉATOIRE : 10 faits tirés uniformément (générateur dédié).
- SIGNAUX : score = nombre de groupes de sources EFFECTIVES (copieurs fusionnés avec leur source détectée,
  par transitivité) dont la majorité des énoncés sur ce fait contredit la réponse actuelle du système aux
  époques correspondantes ; départage par l'incertitude moyenne (1 − probabilité de la réponse). Justification
  enregistrée au moment du choix : sources contradictrices, fusions appliquées, incertitude.
- ORACLE : connaît les erreurs : les 10 faits ayant le plus d'époques fausses dans le modèle sans ancre.
- INCERTITUDE SEULE (descriptif, sans réentraînement) : les 10 faits les plus incertains ; on rapporte seulement
  leur « pureté » (part d'époques fausses parmi les faits choisis).
Mesures (sur TOUS les faits × époques, appariées au modèle sans ancre de la même graine) :
- corrections nettes par vérification = (faux → juste) − (juste → faux), divisé par le nombre de faits vérifiés ;
  décomposées en directes (faits vérifiés) et indirectes (autres faits) ;
- dégâts collatéraux par vérification = (juste → faux) sur les faits NON vérifiés ;
- pureté de chaque sélection. IC par bootstrap sur les faits.
Prédictions :
- H85 [sens] complice : SIGNAUX > ALÉATOIRE en corrections nettes par vérification (significatif)           — 80 %
- H86 [sens] menteur : SIGNAUX > ALÉATOIRE (significatif)                                                  — 50 %
- H87 [sens] plausible : SIGNAUX > ALÉATOIRE (significatif)                                                — 55 %
- H88 [sens] ORACLE ≥ SIGNAUX dans chacun des trois mondes (point estimé)                                  — 75 %
- H89 [ampleur] complice : SIGNAUX atteint ≥ 50 % des corrections nettes de l'ORACLE                      — 50 %
- H90 [sens] complice : pureté de l'INCERTITUDE SEULE < pureté des SIGNAUX (l'incertitude rate la coalition) — 75 %
Aucune règle d'adoption : c'est une mesure de sélection, pas un organe.

### Verdict H-Sélection (graines neuves 61-63, budget 10 faits/graine, cache /tmp/cache_selection_0d62c0b24ac0)
Corrections nettes par fait vérifié (directes + indirectes) ; dégâts collatéraux par fait vérifié ; pureté :
| monde | ALÉATOIRE | SIGNAUX | ORACLE | pureté incertitude seule |
|---|---|---|---|---|
| complice | +1,07 (dégâts 0,00 ; pureté 9 %) | **+16,03** (dir. 9,70 + ind. 6,33 ; dégâts 1,30 ; pureté 81 %) | +20,60 (dégâts 1,27 ; pureté 100 %) | 16 % |
| menteur | +0,77 (0,03 ; 6 %) | +3,00 (0,03 ; 24 %) | +5,43 (0,07 ; 45 %) | 33 % |
| plausible | +0,43 (0,10 ; 4 %) | +1,87 (0,13 ; 14 %) | +5,13 (0,33 ; 42 %) | 25 % |

| | observé | type | proba | |
|---|---|---|---|---|
| H85 complice : SIGNAUX > ALÉATOIRE | +14,97 ± 5,03 | sens | 80 % | ✓ |
| H86 menteur : SIGNAUX > ALÉATOIRE | +2,23 ± 1,53 | sens | 50 % | ✓ |
| H87 plausible : SIGNAUX > ALÉATOIRE | +1,43 ± 1,07 | sens | 55 % | ✓ |
| H88 ORACLE ≥ SIGNAUX, 3 mondes | +4,57 ; +2,43 ; +3,27 | sens | 75 % | ✓ |
| H89 complice : SIGNAUX ≥ 50 % de l'ORACLE | 78 % | ampleur | 50 % | ✓ |
| H90 complice : incertitude moins pure que SIGNAUX | 16 % contre 81 % | sens | 75 % | ✓ |

Établi (dans ces mondes) : la sélection fondée sur des contradictions par sources indépendantes bat le hasard dans
les trois mondes ; face à la coalition, elle atteint 78 % de l'oracle, avec une forte généralisation indirecte.
Les dégâts collatéraux accompagnent le fait de TOUCHER la coalition (SIGNAUX 1,30 ≈ ORACLE 1,27 ; ALÉATOIRE ≈ 0) :
c'est le prix du levier Filiation, pas un défaut du sélecteur ; ratio corrections/dégâts ≈ 12.
Descriptif, NON établi (pureté sans réentraînement) : hors coalition, l'incertitude seule est PLUS pure que les
contradictions (menteur 33 % contre 24 % ; plausible 25 % contre 14 %), et moins pure face à la coalition
(16 % contre 81 %). Piste : chaque signal correspond à un type de défaillance ; aucun n'est le meilleur partout.
Justifications (traçabilité) : graine 61, chaque fait choisi est contredit par La Gazette ET Le Registre, mais
compté comme UNE seule voix, parce que la Filiation (sans ancre) juge à tort que La Gazette recopie Le Registre.
Le score s'effondre (1 voix partout), le choix retombe sur l'incertitude, 6 cibles sur 10 au lieu de 10/10
(graines 62 et 63 : 10/10 et 9/10). La justification enregistrée rend cette fausse accusation VISIBLE : un humain
qui la lit peut la corriger. C'est le seul pont vers « dire pourquoi » que ce test établit — un choix lisible, dont
l'erreur est repérable dans ses propres raisons.

Calibration : 6/6, Brier 0,145. Cumul 74 : 0,193.

# Fil « dire pourquoi » (décidé : avant « savoir ce qu'on ne sait pas », qu'il doit alimenter)
Raison : la confiance affichée mesure l'incertitude DANS le modèle ; une justification expose les hypothèses sur
lesquelles cette confiance repose. Préalable : une justification n'a de valeur que si elle est FIDÈLE —
sinon c'est un récit.

## H-Fidélité (écrite le 2026-10-12 à 06:30 UTC, avant toute ligne de code)
Système : la référence (Méprise), sans ancre. Fidélité LOCALE : paramètres appris fixés, on n'explique que la
décision prise avec eux. Mondes : facile, écho, menteur, plausible, complice. Graines neuves 64, 65, 66.
Échantillon : 60 réponses (fait × époque) par monde et par graine, tirées par un générateur dédié.
Justification courte : chaque énoncé sur le fait reçoit une contribution = [log P(énoncé | réponse retenue) −
log P(énoncé | valeur concurrente la plus probable)] × (1 − taux de changement)^|écart d'époque|, avec la vraisemblance
EFFECTIVE de l'organe (copie, forme des erreurs incluses). La justification cite les k = 3 énoncés de plus forte
contribution POSITIVE.
Recalcul exact (filtre avant-arrière sur ce fait, paramètres fixés) :
- SUFFISANCE : en ne gardant que les k énoncés cités, la réponse reste-t-elle la même ?
- NÉCESSITÉ : en retirant les k énoncés cités, la réponse change-t-elle ?
Taux de base (règle 10) : k énoncés tirés au hasard parmi ceux de contribution positive. Si une réponse a moins de
k énoncés positifs, on les prend tous (pour les deux bras). Descriptif : k = 1 et k = 5 ; réponses fausses à part.
- H91 [sens] suffisance(3) citée > suffisance(3) au hasard, dans chacun des 5 mondes (point estimé)      — 80 %
- H92 [sens] nécessité(3) citée > nécessité(3) au hasard, dans chacun des 5 mondes (point estimé)        — 75 %
- H93 [ampleur] suffisance(3) citée ≥ 80 % en moyenne sur les mondes                                     — 50 %
- H94 [ampleur] nécessité(3) citée ≥ 50 % en moyenne sur les mondes                                      — 35 %
Aucune règle d'adoption : c'est une mesure de la justification, pas un organe.

### Verdict H-Fidélité (graines neuves 64-66, 900 réponses, cache /tmp/cache_fidelite_897bbda92ff7)
| monde | suffisance citée | hasard | nécessité citée | hasard | (k = 3) |
|---|---|---|---|---|---|
| facile | 100 % | 98 % | 18 % | 12 % | |
| écho | 100 % | 88 % | 36 % | 11 % | |
| menteur | 100 % | 93 % | 27 % | 9 % | |
| plausible | **93 %** | **96 %** | 19 % | 8 % | |
| complice | 100 % | 98 % | 11 % | 6 % | |

| | observé | type | proba | |
|---|---|---|---|---|
| H91 suffisance citée > hasard, 5 mondes | 4/5 ; plausible 93 % < 96 % | sens | 80 % | ✗ |
| H92 nécessité citée > hasard, 5 mondes | 5/5 | sens | 75 % | ✓ |
| H93 suffisance citée ≥ 80 % | 99 % | ampleur | 50 % | ✓ |
| H94 nécessité citée ≥ 50 % | 22 % | ampleur | 35 % | ✗ |

Établi (fidélité locale, paramètres fixés) : trois énoncés cités suffisent presque toujours à reproduire la décision
(99 %), mais sont rarement nécessaires (22 %) : les réponses sont SURDÉTERMINÉES (médiane : 16 énoncés par fait,
13 qui soutiennent la réponse). Une justification honnête doit pouvoir dire « ces raisons suffisent, aucune n'est
indispensable ». Les énoncés cités sont plus nécessaires que des énoncés pris au hasard dans les 5 mondes.
Échec H91 : dans le monde plausible, les énoncés cités sont un peu MOINS suffisants que le hasard (93 % contre 96 %,
~5 réponses sur 180, possiblement du bruit). Cause non établie ; le score de contribution y utilise la forme des
erreurs apprise, ce qui en fait le monde le plus délicat pour un score énoncé par énoncé.
DESCRIPTIF, NON PRÉDIT (piste forte pour « savoir ce qu'on ne sait pas ») : sur les 68 réponses FAUSSES, la nécessité
citée vaut 59 %, contre ~19 % sur les réponses justes (taux de base). Les réponses fausses reposent sur peu de
raisons : en retirer trois les renverse le plus souvent. À tester comme prédicteur d'erreur, pré-enregistré.
Calibration : 2/4, Brier 0,269. Cumul 78 : 0,197.

## H-Fragilité (écrite le 2026-10-12 à 06:41 UTC, avant toute ligne de code)
Question : quels signaux internes repèrent les réponses FAUSSES, et lesquels selon le type de défaillance ?
Système : la référence (Méprise), sans ancre. Mondes : facile, écho, menteur, plausible, complice. Graines neuves 67-69.
Échantillon : 300 réponses (fait × époque) par monde et graine (générateur dédié), pour avoir assez d'erreurs.
Trois signaux de risque, calculés sur le seul modèle :
- INCERTITUDE = 1 − probabilité de la réponse ;
- FRAGILITÉ = nombre R d'énoncés de plus forte contribution (score de H-Fidélité) qu'il faut retirer pour renverser
  la réponse, cherché parmi R ∈ {1, 2, 3, 5, 8} (sinon R = 9) ; plus R est petit, plus la réponse est fragile ;
- CONTESTATION = nombre de groupes de sources effectives (copieurs fusionnés) dont la majorité des énoncés sur ce
  fait contredit la réponse (le score de H-Sélection).
Mesures : AUC de chaque signal pour séparer réponses fausses et justes (ex æquo comptés pour moitié) ; différences
d'AUC appariées, IC par bootstrap sur les faits ; part des erreurs capturées en examinant 10 % des réponses.
Calcul préalable (avant mesure) : face à la coalition, un mensonge est soutenu par ~3 sources × ~12 époques ;
retirer ses 3 meilleurs soutiens ne le renversera pas. Attendu : la fragilité voit le bruit, pas la coordination.
- H95 [sens] AUC(fragilité) significativement > 0,5 dans chacun des 4 mondes hors coalition                 — 65 %
- H96 [sens] complice : AUC(contestation) > AUC(fragilité), significatif                                    — 75 %
- H97 [sens] complice : AUC(contestation) > AUC(incertitude), significatif                                  — 80 %
- H98 [sens] hors coalition : AUC(fragilité) > AUC(incertitude) (point estimé) dans au moins 3 mondes sur 4   — 45 %
- H99 [ampleur] hors coalition : à 10 % de couverture, la fragilité capture ≥ 40 % des erreurs (moyenne)    — 45 %
Aucune règle d'adoption : c'est une carte des signaux, pas un organe.

### Verdict H-Fragilité (graines neuves 67-69, 4 500 réponses, cache /tmp/cache_fragilite_a6f99c113ddd)
| monde | erreurs | AUC incertitude | AUC fragilité | AUC contestation | capture à 10 % (inc. / frag. / cont.) |
|---|---|---|---|---|---|
| facile | 34 | **0,98** | 0,86 | 0,51 | 97 / 65 / 12 % |
| écho | 64 | **0,94** | 0,82 | 0,50 | 59 / 44 / 5 % |
| menteur | 39 | **0,97** | 0,88 | 0,55 | 85 / 59 / 10 % |
| plausible | 45 | **0,94** | 0,82 | 0,53 | 69 / 36 / 9 % |
| complice | 101 | 0,68 | 0,63 | **0,88** | 23 / 13 / 61 % |

| | observé | type | proba | |
|---|---|---|---|---|
| H95 fragilité > 0,5, 4 mondes hors coalition | AUC 0,82-0,88, IC tous > 0 | sens | 65 % | ✓ |
| H96 complice : contestation > fragilité | [+0,16 ; +0,33] | sens | 75 % | ✓ |
| H97 complice : contestation > incertitude | [+0,11 ; +0,28] | sens | 80 % | ✓ |
| H98 fragilité > incertitude, ≥ 3/4 mondes | 0/4 : l'incertitude l'emporte partout, significativement | sens | 45 % | ✗ |
| H99 fragilité capture ≥ 40 % à 10 % | 51 % en moyenne (incertitude : 78 %) | ampleur | 45 % | ✓ |

Établi (dans ces mondes) : deux types de défaillance, deux signaux. Les erreurs de BRUIT sont repérées par
l'incertitude affichée (AUC 0,94-0,98) ; les mensonges COORDONNÉS lui échappent (0,68) et sont repérés par la
contestation — des sources indépendantes, copieurs fusionnés, qui contredisent la réponse (0,88 ; 61 % des erreurs
en examinant 10 % des réponses). Aucun signal n'est bon partout : la contestation ne voit rien du bruit (≈ 0,5).
La fragilité est informative mais REDONDANTE avec l'incertitude, et moins bonne qu'elle partout.
Leçon de méthode : la piste de H-Fidélité (réponses fausses 3 × plus fragiles) était réelle par rapport au taux de
base, mais je ne l'avais pas comparée au meilleur signal EXISTANT. Un signal nouveau se juge contre le meilleur
concurrent, pas seulement contre le hasard.
Sur le pont « dire pourquoi » → « savoir ce qu'on ne sait pas » : il tient, mais par la STRUCTURE de la
justification (qui contredit, avec quelle indépendance), pas par le nombre de raisons.
Calibration : 4/5, Brier 0,146. Cumul 83 : 0,194.

## H-Combiné (écrite le 2026-10-12 à 07:32 UTC, avant toute ligne de code)
Signal combiné, PRINCIPAL (règle lexicographique, lisible) : d'abord les réponses contestées par au moins DEUX voix
effectives (copieurs fusionnés) — seuil minimal d'une contestation corroborée, une seule voix pouvant n'être qu'une
erreur — puis, à l'intérieur de chaque groupe, par incertitude décroissante. Chaque réponse signalée porte un motif
énonçable : « contestée par deux sources indépendantes » ou « peu de preuves ».
Descriptif (sans hypothèse) : le maximum des deux rangs-centiles (combinaison neutre, sans seuil).
Système : la référence (Méprise), sans ancre. Mondes : facile, écho, menteur, plausible, complice.
Graines neuves 70, 71, 72. TOUTES les réponses (faits × époques). AUC par rangs ; IC par bootstrap sur les faits.
Marge de non-infériorité : 0,02 d'AUC — plus petite que le plus petit écart significatif mesuré entre deux signaux
dans H-Fragilité (borne la plus proche de 0 : 0,05).
- H100 [sens] pire monde : AUC minimale du combiné > AUC minimale de l'incertitude ET de la contestation     — 80 %
- H101 [sens] complice : AUC(combiné) > AUC(incertitude), significatif                                      — 85 %
- H102 [ampleur, non-infériorité] dans chacun des 4 mondes hors coalition : borne basse de
       AUC(combiné) − AUC(incertitude) > −0,02                                                              — 55 %
- H103 [ampleur] en examinant 10 % des réponses, le combiné capture ≥ 70 % des erreurs (moyenne des 5 mondes) — 50 %
Aucune règle d'adoption.

### Verdict H-Combiné (graines neuves 70-72, toutes les réponses, cache /tmp/cache_combine_b539d61658b6)
| monde | erreurs | AUC incertitude | AUC contestation | AUC combiné | capture 10 % (inc. / cont. / comb.) |
|---|---|---|---|---|---|
| facile | 234 | 0,982 | 0,494 | 0,982 | 100 / 12 / 100 % |
| écho | 583 | 0,950 | 0,526 | 0,927 | 72 / 12 / 61 % |
| menteur | 430 | 0,964 | 0,553 | 0,939 | 82 / 13 / 69 % |
| plausible | 515 | 0,929 | 0,546 | 0,903 | 69 / 14 / 46 % |
| complice | 960 | 0,736 | 0,881 | **0,950** | 31 / 71 / **79 %** |

| | observé | type | proba | |
|---|---|---|---|---|
| H100 pire monde | combiné 0,903 ; incertitude 0,736 ; contestation 0,494 | sens | 80 % | ✓ |
| H101 complice : combiné > incertitude | [+0,183 ; +0,250] | sens | 85 % | ✓ |
| H102 non-infériorité hors coalition (marge 0,02) | facile 0 ; écho [−0,033 ; −0,014] ; menteur [−0,037 ; −0,016] ; plausible [−0,055 ; +0,005] | ampleur | 55 % | ✗ |
| H103 capture moyenne ≥ 70 % | 71 % (incertitude seule : 71 %) | ampleur | 50 % | ✓ |

Établi (dans ces mondes) : le signal combiné ne s'effondre nulle part (pire AUC 0,90 contre 0,74 et 0,49) et il
transforme le monde de la coalition (79 % des erreurs capturées contre 31 %). Mais il COÛTE dans les mondes de bruit :
des réponses justes contestées par deux voix (erreurs ordinaires qui coïncident, surtout avec des erreurs plausibles)
passent devant de vraies erreurs incertaines (plausible : capture 69 → 46 %). Sa capture moyenne égale celle de
l'incertitude seule : il échange de la performance dans un régime contre de la robustesse dans l'autre.
Lecture : un score unique mêle deux questions différentes — « où sont mes erreurs ? » et « où ma croyance est-elle
contestée ? ». Une réponse juste mais contestée par deux voix indépendantes n'est pas une fausse alarme du point de vue
de la traçabilité : elle EST contestée. Fusionner les deux doutes en un rang perd cette information.
Calibration : 3/4, Brier 0,154. Cumul 87 : 0,192.

# L'objet-réponse : deux doutes séparés, chacun avec son motif

## H-ObjetRéponse (écrite le 2026-10-12 à 08:18 UTC, avant toute ligne de code)
Objet-réponse (par fait et époque) : valeur ; confiance ; DOUTE « preuves » (motif « peu de preuves » si confiance
< 0,9 — convention fixée d'avance : une chance sur dix de se tromper) ; DOUTE « contestation » (motif « contestée »
si au moins deux voix effectives contredisent la réponse) avec la liste des contradicteurs et des fusions appliquées
(qui est compté avec qui, et à quel taux de copie estimé) ; justification courte (3 énoncés de plus forte
contribution) ; hypothèses structurelles appliquées au fait (copies, soupçons). Aucun score fusionné.
Ce qu'il doit apporter qu'un score fusionné ne peut pas : un MOTIF JUSTE — « contestée » doit désigner les mensonges
coordonnés, « peu de preuves » le bruit.
Monde nouveau « mixte » : la coalition des complices ET des erreurs plausibles (sosies, 70 %) chez toutes les sources.
Les deux défaillances coexistent ; le type vrai de chaque erreur est connu (fait ciblé = coordination ; sinon = bruit).
Contrôles : complice et plausible (régimes purs). Graines neuves 73, 74, 75. Toutes les réponses. IC par bootstrap sur les faits.
- H105 [sens] mixte : parmi les erreurs portant le motif « contestée », la part de coordination dépasse
       significativement son taux de base parmi toutes les erreurs                                        — 80 %
- H106 [sens] mixte : parmi les erreurs portant SEULEMENT le motif « peu de preuves », la part de bruit dépasse
       significativement son taux de base                                                                — 75 %
- H107 [sens] mixte : à budget égal (10 % des réponses), la politique « moitié file contestée, moitié file peu sûre »
       repère au moins autant d'erreurs que l'incertitude seule (point estimé)                             — 70 %
- H108 [ampleur] mixte : au moins 80 % des erreurs portent au moins un motif                              — 50 %

### Verdict H-ObjetRéponse (graines neuves 73-75, toutes les réponses, cache /tmp/cache_objet_e5d4ef6e9524)
| monde | erreurs (coordination / bruit) | portant un motif | « contestée » → coordination (base) | « peu de preuves » seul → bruit (base) | capture 10 % : incertitude / objet |
|---|---|---|---|---|---|
| mixte | 1 131 (938 / 193) | 89 % | 100 % (83 %) | 96 % (17 %) | 26 % / **52 %** |
| complice | 1 010 (814 / 196) | 91 % | 100 % (81 %) | 86 % (19 %) | 33 % / 61 % |
| plausible | 405 (0 / 405) | 83 % | — (47 erreurs contestées, toutes de bruit) | 100 % (100 %) | **78 %** / 64 % |

| | observé | type | proba | |
|---|---|---|---|---|
| H105 « contestée » → coordination au-delà du taux de base | [+13 % ; +22 %] | sens | 80 % | ✓ |
| H106 « peu de preuves » seul → bruit au-delà du taux de base | [+73 % ; +83 %] | sens | 75 % | ✓ |
| H107 objet ≥ incertitude seule, à budget égal (mixte) | 52 % contre 26 % | sens | 70 % | ✓ |
| H108 ≥ 80 % des erreurs portent un motif (mixte) | 89 % | ampleur | 50 % | ✓ |

Établi (dans ces mondes) : les deux motifs de l'objet-réponse sont JUSTES. Quand les deux défaillances coexistent,
« contestée » désigne les mensonges coordonnés (100 %) et « peu de preuves » le bruit (96 %) ; 89 % des erreurs portent
au moins un motif. Le lecteur sait où regarder ET quel genre de problème il trouvera — ce qu'aucun score fusionné
ne peut dire. À budget égal, deux files séparées repèrent deux fois plus d'erreurs que l'incertitude seule.
Limite : la répartition fixe « moitié-moitié » coûte dans un monde de bruit pur (78 → 64 %) ; la répartition du budget
entre les files est une décision d'usage, que l'objet ne tranche pas.
Exemple réel (mixte, g73) : « Kalo, confiance 1,00 — contestée par La Gazette et Le Registre — soupçon sur La Gazette
0,94 — pourquoi : Le Notable, Le Relais ». Le système est certain d'un mensonge, mais l'objet rend l'erreur LISIBLE :
ses raisons ne viennent que de la coalition, ses contradicteurs sont les deux indépendants, et il soupçonne à tort un
honnête. « Certitude contestée » apparaît comme la signature visible de la coordination.
Calibration : 4/4, Brier 0,111. Cumul 91 : 0,188.

## Jalon : charte mise à jour (objet-réponse et piliers ; ancres hors référence)

# La boucle de bout en bout : choisir → vérifier → ancrer → réviser → rechoisir

## H-Boucle (écrite le 2026-10-12 à 17:54 UTC, avant toute ligne de code)
Mondes : mixte (coordination + bruit) ; plausible (bruit seul, contrôle). Graines neuves 76, 77, 78.
Deux tours de vérification, 10 faits par tour (20 au total). Au tour 2, l'objet-réponse est recalculé sur le système
révisé ; les faits déjà vérifiés sont exclus. Ancres : fiabilité fixe 0,99, vraie valeur aux 12 époques, cumulées.
Politiques (choix fondés sur l'objet-réponse du système courant, au niveau du fait) :
- CONTESTÉE : faits contestés par ≥ 2 voix effectives, par nombre de voix décroissant puis confiance croissante ;
  si la file est plus courte que le budget, le reste N'EST PAS dépensé ;
- INCERTITUDE : faits de plus faible confiance moyenne ;
- DEUX FILES : moitié CONTESTÉE (le reste, si la file est courte, va à l'incertitude), moitié INCERTITUDE ;
- ALÉATOIRE : faits tirés uniformément (générateur dédié).
Mesures, toutes les réponses, par rapport au système sans ancre de la même graine :
corrections nettes PAR VÉRIFICATION RÉELLEMENT FAITE ; dégâts collatéraux par vérification (juste → faux sur faits non
vérifiés) ; apport du tour 2 seul ; erreurs résiduelles par type (mixte). IC par bootstrap sur les faits, appariés.
- H109 [sens] mixte : CONTESTÉE > ALÉATOIRE (corrections nettes par vérification, significatif)              — 85 %
- H110 [sens] mixte : CONTESTÉE > INCERTITUDE (significatif)                                                 — 70 %
- H111 [sens] plausible : INCERTITUDE > CONTESTÉE (point estimé)                                             — 75 %
- H112 [sens] mixte : DEUX FILES ≥ INCERTITUDE (point estimé)                                                — 70 %
- H113 [ampleur] mixte : dégâts collatéraux de CONTESTÉE ≤ 1/5 de ses corrections nettes                     — 60 %
- H114 [sens] mixte : le tour 2 de CONTESTÉE apporte des corrections nettes significativement > 0             — 65 %
Aucune règle d'adoption : c'est une mesure de la boucle, pas un organe.

### Verdict H-Boucle (graines neuves 76-78, 2 tours × 10 faits, cache /tmp/cache_boucle_fa1718b294d4)
| monde | politique | vérifications faites | corrections nettes / vérif | dégâts / vérif | apport du tour 2 / vérif |
|---|---|---|---|---|---|
| mixte | CONTESTÉE | 44 | **+11,27** | 0,66 | +5,73 |
| mixte | INCERTITUDE | 60 | +1,92 | 0,03 | +0,53 |
| mixte | DEUX FILES | 60 | +5,05 | 0,27 | +2,35 |
| mixte | ALÉATOIRE | 60 | +2,25 | 0,23 | +0,93 |
| plausible | CONTESTÉE | 49 | +1,33 | 0,08 | +0,12 |
| plausible | INCERTITUDE | 60 | **+2,57** | 0,03 | +1,12 |
| plausible | DEUX FILES | 60 | +2,52 | 0,10 | +1,13 |
| plausible | ALÉATOIRE | 60 | +0,63 | 0,02 | +0,38 |

Erreurs résiduelles, mixte, après 2 tours (coordination / bruit) : sans vérification 1 040 / 186 ; CONTESTÉE 545 / 185 ;
INCERTITUDE 1 007 / 104 ; DEUX FILES 788 / 135 ; ALÉATOIRE 927 / 164.

| | observé | type | proba | |
|---|---|---|---|---|
| H109 mixte : CONTESTÉE > ALÉATOIRE | +9,02 ± 3,07 | sens | 85 % | ✓ |
| H110 mixte : CONTESTÉE > INCERTITUDE | +9,36 ± 3,20 | sens | 70 % | ✓ |
| H111 plausible : INCERTITUDE > CONTESTÉE | +2,57 contre +1,33 | sens | 75 % | ✓ |
| H112 mixte : DEUX FILES ≥ INCERTITUDE | +3,13 ± 1,63 | sens | 70 % | ✓ |
| H113 mixte : dégâts de CONTESTÉE ≤ 1/5 de ses corrections | 0,66 / 11,27 ≈ 1/17 | ampleur | 60 % | ✓ |
| H114 mixte : le tour 2 de CONTESTÉE apporte significativement | +252 ± 101 corrections nettes | sens | 65 % | ✓ |

Établi (dans ces mondes) : la boucle fonctionne de bout en bout. Chaque file répare SON type de défaillance :
la file contestée réduit de moitié les erreurs de coordination sans toucher au bruit (1 040 → 545 ; 186 → 185) ; la file
incertitude réduit presque de moitié le bruit sans toucher à la coordination (186 → 104 ; 1 040 → 1 007). Les motifs de
l'objet-réponse désignent donc aussi la bonne RÉPARATION. Le second tour, choisi sur le système révisé, apporte encore
la moitié du gain : la boucle ne s'épuise pas après les cas évidents. Dégâts collatéraux : environ 1 pour 17 corrections.
Limite : la file contestée n'a dépensé que 44 vérifications sur 60 (mixte) — elle s'épuise ; la répartition du budget
entre files reste une décision d'usage.
Calibration : 6/6, Brier 0,091. Cumul 97 : 0,182.

# Chantier « désordre réel » — 1. le témoin LLM

## H-TémoinLLM (écrite le 2026-10-12 à 19:15 UTC, avant toute ligne de code)
Contrainte matérielle : aucun LLM n'est accessible depuis l'environnement de calcul. Le témoin passe par une page
publiée dont la capacité « sample » interroge Claude sur le compte de Khaled (consentement à chaque session) ;
les réponses sont écrites dans la base de la page, puis relues pour notation. Le témoin est un modèle Claude ; il
ne voit ni cette conversation ni le générateur. Modèle effectivement appliqué : enregistré à chaque appel.
Limite par appel : 256 Ko de texte → mondes à la taille d'origine (40 personnes, 8 organisations), graine neuve 79 :
facile (96 Ko), écho (177 Ko), menteur (119 Ko), complice (155 Ko). 57 questions par monde (15 actuel, 15 historique,
15 deux sauts, 12 sans réponse). Le témoin reçoit TOUT le corpus brut du monde, la consigne (« maintenant » = époque 11 ;
INCONNU si l'information est absente ; confiance entre 0 et 1 ; sortie JSON), et les questions par lots de 19 :
3 appels par monde, 12 au total. Aucune analyse ne lui est fournie.
Comparé à GrandNexus (référence, Méprise) sur les mêmes questions, mêmes mondes.
Puissance faible (57 questions par monde) : seuls de grands écarts seront lisibles ; IC par bootstrap sur les questions.
- H115 [ampleur] facile : exactitude du témoin LLM ≥ 85 %                                               — 60 %
- H116 [sens] complice : sur les questions dont la réponse dépend d'un fait ciblé par la coalition, le témoin
       se trompe au moins aussi souvent que GrandNexus (point estimé)                                   — 70 %
- H117 [sens] historique (4 mondes réunis) : exactitude GrandNexus > témoin LLM (point estimé)           — 65 %
- H118 [sens] sans réponse (4 mondes réunis) : GrandNexus s'abstient correctement plus souvent que le témoin — 60 %
- H119 [sens] calibration (4 mondes réunis) : Brier du témoin > Brier de GrandNexus                    — 70 %
- H120 [sens] menteur : exactitude GrandNexus > témoin LLM (point estimé)                              — 60 %

### Verdict H-TémoinLLM (graine 79, 4 mondes × 57 questions, réponses relues depuis la base de la page)
Exécution : 12 appels en ~2 minutes, aucun lot tronqué ni illisible, aucune réponse manquante. Modèle : modèle par défaut
du compte, non identifié par la page. Le témoin lit le TEXTE ; GrandNexus reçoit les TRIPLETS (perception parfaite).
| monde | témoin LLM | GrandNexus | GN − LLM [IC 95 %] |
|---|---|---|---|
| facile | 82 % | 96 % | +14 [+5 ; +23] |
| écho | 74 % | 75 % | +2 [−9 ; +12] |
| menteur | 81 % | 82 % | +2 [−5 ; +9] |
| complice | 86 % | 91 % | +5 [−4 ; +14] |
Par type (4 mondes) : actuel 80 / 87 % ; historique 80 / 93 % (+13 [+3 ; +25]) ; deux sauts 67 / 68 % ; sans réponse 100 / 100 %.
Brier : témoin 0,175 ; GrandNexus 0,088 (LLM − GN +0,087 [+0,058 ; +0,116]).

| | observé | type | proba | |
|---|---|---|---|---|
| H115 facile : témoin ≥ 85 % | 82 % | ampleur | 60 % | ✗ |
| H116 complice ciblés : témoin se trompe au moins autant | témoin 3/6 justes, GrandNexus 1/6 | sens | 70 % | ✗ |
| H117 historique : GrandNexus > témoin | +13 [+3 ; +25] | sens | 65 % | ✓ |
| H118 sans réponse : GrandNexus s'abstient mieux | 100 % = 100 % (le témoin n'hallucine jamais) | sens | 60 % | ✗ |
| H119 Brier : témoin > GrandNexus | 0,175 contre 0,088 | sens | 70 % | ✓ |
| H120 menteur : GrandNexus > témoin | 82 % contre 81 % | sens | 60 % | ✓ (point, non significatif) |

Lecture :
- Dans ces petits mondes, dont tout le corpus tient dans le contexte, un modèle de langage qui lit tout est un témoin
  SÉRIEUX. GrandNexus n'est significativement meilleur que sur le monde facile, les questions historiques et la
  calibration. Partout ailleurs, la puissance (57 questions) ne permet pas de les départager.
- Le témoin ne tombe pas dans la chambre d'écho (74 % contre 75 %), là où le vote majoritaire s'effondrait.
- Le témoin n'invente jamais : les 48 questions sans réponse reçoivent toutes INCONNU. Ma prédiction contraire était fausse.
- Coalition (n = 6, illisible statistiquement) : les deux se trompent le plus souvent ; GrandNexus est certain (1,00) de
  ses 5 erreurs, le témoin reste plus prudent (0,50-0,85) et en évite 2. À ne pas interpréter au-delà.
- Calibration du témoin : bandes de confiance ordonnées (≥ 0,9 → 88 % ; 0,7-0,9 → 82 % ; < 0,7 → 64 %), légèrement
  sous-confiant (0,71 annoncé, 76 % réel) ; son Brier plus élevé vient d'une confiance moins tranchée, pas d'un excès.
- Biais du test en faveur de GrandNexus : il reçoit les triplets, le témoin doit lire. C'est ce que l'Accueil devra mesurer.
- Ce test ne dit rien des avantages revendiqués de GrandNexus hors contexte : corpus plus grand que la fenêtre,
  persistance, traçabilité (objet-réponse).
Calibration de l'expérimentateur : 3/6, Brier 0,264. Cumul 103 : 0,187.

## Précision (Khaled) sur H-TémoinLLM
Selon Khaled, le modèle du témoin était « Opus 5.5, effort élevé » (réglage de son compte ; non vérifié par la page).
Lecture : un modèle de pointe a joué sans connaître les règles du monde et en lisant du texte ; GrandNexus a joué avec
des organes construits pour ces mondes et des triplets déjà découpés. Le jeu égal est un signal encourageant pour un
organe de jugement spécialisé, pas une preuve de robustesse hors de son monde.

# Chantier « désordre réel » — 2. l'Accueil (lire des phrases)
Trois versions, dans cet ordre (décision de Khaled) : (1) lecteur à RÈGLES, sans LLM ; (2) LLM comme organe des SENS ;
(3) HYBRIDE : règles d'abord, LLM pour le reste, chaque lecture du LLM traitée comme un canal dont GrandNexus apprend la
fiabilité. Critères « pas un wrapper », à rendre testables : le jugement reste hors du LLM ; GrandNexus fonctionne sans
le LLM ; GrandNexus mesure la fiabilité du LLM et s'en méfie quand il se trompe.

## Étape 0 — génération du désordre (spécification, 2026-10-12 à 19:41 UTC, avant toute génération)
400 énoncés tirés des mondes « complice » et « plausible » (40 personnes, 8 organisations, graine neuve 80), stratifiés par
relation (habite, travaille, dirige, naissance). Réécrits par Claude (capacité « sample » d'une page, compte de Khaled) en
français désordonné, en conservant EXACTEMENT le même fait. Métadonnées (source, époque) conservées hors de la phrase,
comme celles d'un document. Vérité de référence : le triplet d'origine (si la réécriture altère le fait, les deux lecteurs
en pâtiront également — limite notée). Partage FIGÉ avant génération : lots 0-3 = DÉVELOPPEMENT (200 phrases, seules
lues pour construire le lecteur) ; lots 4-7 = TEST (200 phrases, ouvertes uniquement par le script de test).

## Accueil v1 — lecteur à règles, construit sur la moitié de DÉVELOPPEMENT seulement
Désordre généré par Claude (8 lots, aucun tronqué). Styles observés en développement : familier, paraphrase libre,
rumeur, administratif, ordre inversé, périphrase, incise, faute de frappe.
Lecteur : liste des entités du monde (avantage déclaré : un graphe connaît ses entités ; le lecteur LLM ne l'aura pas),
fautes tolérées (une lettre, ou deux lettres interverties, sur les noms d'au moins 5 lettres), relation déduite du type
des entités, direction/emploi tranchés par mots-clés ; chaque lecture porte une confiance et ses raisons.
Développement : 1er passage 92 % ; 5 défauts mécaniques corrigés (mot-clé dans un mot, quartier dans un nom, fautes sur
noms courts, interversions, tournures manquantes) → 99 % ; 2 derniers (élision, « boss » mot entier) → 100 %.
Ce 100 % ne vaut rien : le développement a servi à corriger. Lecteur FIGÉ : accueil_regles.py, empreinte 31e708a5e7ddb7fe.

## H-AccueilRègles (écrite le 2026-10-12 à 20:08 UTC, avant d'ouvrir les lots de test 4-7)
- H121 [ampleur] test : triplets exacts ≥ 90 %                                                    — 65 %
- H122 [sens] test : les lectures de confiance ≥ 0,95 sont plus souvent justes que les autres     — 80 %
- H123 [ampleur] test : au moins 97 % des phrases sont lues (une lecture, juste ou non)          — 70 %
- H124 [sens] test : exactitude < développement (100 %) — le lecteur est sur-ajusté               — 85 %
Après notation, la moitié de test devient VUE : elle ne pourra plus servir de test.

### Verdict H-AccueilRègles (moitié de test, 200 phrases, lecteur figé 31e708a5e7ddb7fe) — la moitié de test est désormais VUE
Lues 100 % ; triplets exacts 199/200 (99,5 %). Confiance ≥ 0,95 : 194 lectures, toutes justes ; confiance < 0,95 : 6 lectures,
5 justes. Unique erreur : « La Maison Kalimi, celle que mène Rika Quilmigor » — « mène » absent des mots de direction ;
le lecteur l'a signalée lui-même (confiance 0,5, « aucun mot-clé : emploi par défaut »).
| | observé | type | proba | |
|---|---|---|---|---|
| H121 triplets exacts ≥ 90 % | 99,5 % | ampleur | 65 % | ✓ |
| H122 confiance haute plus juste | 100 % contre 83 % (n = 6) | sens | 80 % | ✓ |
| H123 ≥ 97 % lues | 100 % | ampleur | 70 % | ✓ |
| H124 test < développement | 99,5 % < 100 % (une erreur) | sens | 85 % | ✓ (de justesse) |
Calibration : 4/4, Brier 0,069. Cumul 107 : 0,183.

Lecture honnête — EFFET PLAFOND : ce désordre est stylistique, pas structurel. Chaque phrase porte UN fait, des entités
connues, nommées en entier ; la consigne (« exactement le même fait ») le contraignait. Un lecteur de 109 lignes le lit à
99,5 %. Ce test montre que la variation de STYLE ne justifie pas un LLM ; il ne dit rien du désordre réel : plusieurs faits
par phrase, pronoms d'une phrase à l'autre, corrections (« non, en fait… »), temps relatif, entités inconnues ou nommées
à moitié, descriptions au lieu de noms (« le patron de Maison X »). Règle 5 : une épreuve que tout le monde réussit se
durcit avant d'en tirer quoi que ce soit — en particulier avant de comparer au lecteur LLM.

## Accueil — étape 0 bis : désordre STRUCTUREL (spécification, 2026-10-12 à 21:47 UTC, avant génération)
Scénarios tirés des mondes « complice » et « plausible » (40 personnes, 8 organisations, graine neuve 81) : 160 scénarios de
2 à 4 faits liés (une personne : domicile, employeur, naissance, organisation dirigée ; parfois un collègue). Claude écrit pour
chacun un court paragraphe (2 à 4 phrases) qui affirme EXACTEMENT ces faits, avec deux procédés imposés parmi : PRONOMS,
DESCRIPTION (rôle au lieu du nom), CORRECTION (fausse valeur énoncée puis corrigée — à ne pas lire), NOM PARTIEL, PLUSIEURS
FAITS dans une phrase. Un scénario sur cinq contient une personne INCONNUE du graphe (nom inventé, absent de la liste des
entités). Vérité de référence : la liste des faits du scénario. Notation au niveau du fait : précision, rappel, F1 ; lire la
fausse valeur d'une correction compte comme une erreur. Partage FIGÉ : lots 0-3 développement (80 paragraphes), lots 4-7 test.

## Accueil v1 bis — lecteur de PARAGRAPHES à règles (développement seulement)
Principes génériques : rattacher chaque valeur typée au sujet le plus proche (nom complet, nom partiel déjà rencontré, pronom
ou périphrase renvoyant à la personne la plus proche avant, description « le salarié de Maison X » renvoyant à la personne
liée à X) ; la dernière valeur l'emporte (corrections) ; un nom propre inconnu est une BARRIÈRE (quelqu'un d'autre : on ne lui
attribue rien et on ne lit rien sur lui — aucune extraction sur les inconnus, comme annoncé).
Développement (80 paragraphes, 247 faits) : 1er passage P 94 % / R 79 % ; barrières, descriptions, pronoms → P 91 % / R 70 %
(régression : un défaut caché — chaque nom n'était repéré qu'une fois par phrase, or une correction répète le nom) ; toutes
occurrences → P 99 % / R 83 % ; descriptions non résolues → P 99 % / R 84 % (97 % hors inconnus), pièges lus 0/33.
FIGÉ : accueil_paragraphes.py, empreinte 33accea15603db46.

## Accueil v2 — lecteur LLM (consigne figée avant que quiconque ait vu le test ; aucune phase de développement)
Capacité « sample » de la page du désordre structurel ; lit les lots 4-7 dans la base de la page ; 4 appels de 20 paragraphes.
Ne reçoit PAS la liste des entités (avantage déclaré du lecteur à règles). Consigne : extraire les faits que chaque paragraphe
AFFIRME, selon quatre relations (habite, travaille, dirige avec sujet = organisation, naissance), noms écrits en entier tels
qu'ils apparaissent en entier dans le paragraphe, ne garder que la version corrigée d'une information corrigée, ne rien
inventer ni déduire, confiance entre 0 et 1, sortie JSON.

## H-AccueilParagraphes (écrite le 2026-10-13 à 07:28 UTC, avant d'ouvrir les lots de test 4-7)
Notation au niveau du fait, moitié de test (80 paragraphes). Personne inconnue = nom absent de la liste des entités.
- H125 [ampleur] règles : précision ≥ 95 %                                                        — 75 %
- H126 [ampleur] règles : rappel hors personnes inconnues ≥ 90 %                                  — 60 %
- H127 [ampleur] règles : au plus 3 pièges de correction lus                                      — 70 %
- H128 [sens]    LLM : rappel (tous faits) > rappel des règles (les inconnus lui sont accessibles) — 85 %
- H129 [sens]    LLM : F1 > F1 des règles                                                         — 70 %
- H130 [sens]    LLM : précision < précision des règles (point estimé)                            — 55 %
- H131 [ampleur] LLM : au plus 3 pièges de correction lus                                         — 70 %

### Verdict H-AccueilParagraphes (moitié de test : 80 paragraphes, 241 faits, 39 pièges ; règles figées 33accea15603db46)
| | précision | rappel | rappel hors inconnus | F1 | pièges lus |
|---|---|---|---|---|---|
| lecteur à règles (sans LLM) | 100 % | 84 % | 97 % | 91 % | 0 / 39 |
| lecteur LLM (sans liste d'entités) | 100 % | **100 %** | 100 % | **100 %** | 0 / 39 |
Complémentarité : 202 faits trouvés par les deux ; 0 par les règles seules ; 39 par le LLM seul (surtout les personnes inconnues) ;
0 par aucun. Faits en trop : aucun, pour les deux. Confiance des règles : toutes leurs lectures sont justes, quelle que soit la bande.
| | observé | type | proba | |
|---|---|---|---|---|
| H125 règles : précision ≥ 95 % | 100 % | ampleur | 75 % | ✓ |
| H126 règles : rappel hors inconnus ≥ 90 % | 97 % | ampleur | 60 % | ✓ |
| H127 règles : ≤ 3 pièges | 0 | ampleur | 70 % | ✓ |
| H128 LLM : rappel > règles | 100 % contre 84 % | sens | 85 % | ✓ |
| H129 LLM : F1 > règles | 100 % contre 91 % | sens | 70 % | ✓ |
| H130 LLM : précision < règles | 100 % = 100 % | sens | 55 % | ✗ |
| H131 LLM : ≤ 3 pièges | 0 | ampleur | 70 % | ✓ |
Calibration : 6/7, Brier 0,117. Cumul 114 : 0,179.

Lecture :
- Sur ce désordre structurel, le lecteur LLM est PARFAIT ; le lecteur à règles est parfait sur ce qu'il lit et n'est aveugle que
  sur les personnes qu'il ne connaît pas. Il n'apporte aucun fait que le LLM aurait manqué.
- Biais à garder en tête : le désordre a été ÉCRIT par Claude et LU par Claude. Un modèle lit facilement ce qu'un modèle de la
  même famille écrit ; des paragraphes courts, aux indices explicites. Ce n'est pas du texte humain réel.
- Sur la crainte du wrapper : la perception est, ici, mieux faite par le LLM ; mais le JUGEMENT ne l'est pas — sur les mêmes
  mondes, GrandNexus a deux fois moins d'erreur de calibration qu'Opus jugeant seul (H-TémoinLLM). L'architecture qui se dessine
  est celle du paradigme initial : le LLM perçoit, GrandNexus juge. Un wrapper délègue le jugement ; ici on ne délègue que la lecture.
- Le critère anti-wrapper « GrandNexus mesure la fiabilité du LLM et s'en méfie quand il se trompe » reste NON TESTÉ : le LLM ne s'est
  pas trompé. Il faudra un canal de lecture qui se trompe pour le mettre à l'épreuve.

# Chantier « désordre réel » — 3. de bout en bout : deux architectures à armes égales

## H-BoutEnBout (écrite le 2026-10-13 à 07:45 UTC, avant toute génération)
Monde « complice », 30 personnes, 6 organisations, graine neuve 82 : 1 748 énoncés, 55 questions. Chaque énoncé appartient à une
DÉPÊCHE (une source, une époque) ; les énoncés d'une même (source, époque) sont regroupés par 5 → 376 dépêches. Claude écrit chaque
dépêche en français désordonné, avec deux procédés parmi pronoms, description, nom partiel, plusieurs faits, correction (piège).
Source et époque restent des métadonnées hors du texte. Tout passe par une page (capacité « sample », compte de Khaled).
Cinq montages, mêmes 55 questions :
- A « Opus seul » : le témoin lit TOUTES les dépêches (avec leurs métadonnées) et répond (consigne de H-TémoinLLM) ;
- B « Opus lit, GrandNexus juge » : lecteur par défaut (consigne de l'Accueil v2, inchangée) → énoncés → Méprise ;
- C « petit modèle lit, GrandNexus juge » : même consigne, niveau « quick » ;
- D « GrandNexus sur faits parfaits » (référence) ;
- E « hybride à canaux » : chaque dépêche lue au hasard par B ou C (générateur dédié) ; GrandNexus voit « source · lecteur » comme
  deux canaux distincts et apprend leur fiabilité. Aucun appel supplémentaire.
Risque déclaré pour E : deux canaux d'une même source disent souvent la même vérité ; la Filiation pourrait les prendre pour des copies.
Mesures : exactitude, Brier (comme H-TémoinLLM) ; perception de B et C (précision, rappel sur les énoncés vrais ; pièges lus).
- H132 [sens] exactitude B > A (point estimé)                                                        — 65 %
- H133 [sens] Brier B < Brier A                                                                      — 80 %
- H134 [ampleur] perception B : rappel ≥ 95 %                                                       — 70 %
- H135 [sens] perception C moins bonne que B (précision ou rappel plus bas)                           — 85 %
- H136 [sens] exactitude D ≥ B ≥ C (point estimé)                                                    — 60 %
- H137 [sens] E : pour au moins 4 sources sur 5, fiabilité apprise du canal « petit modèle » < canal « Opus » — 60 %

### Verdict H-BoutEnBout (graine 82 ; 376 dépêches, 1 748 faits, 163 pièges, 55 questions ; aucun lot tronqué ni illisible)
Coût mesuré (communiqué par Khaled) : ≈ 40 % d'une session et ≈ 10 % de l'utilisation hebdomadaire de son forfait, pour 60 appels.
| montage | exactitude | actuel | historique | deux sauts | sans réponse | Brier |
|---|---|---|---|---|---|---|
| A Opus seul (lit et juge) | 84 % | 93 % | 80 % | 67 % | 100 % | 0,173 |
| B Opus lit, GrandNexus juge | 84 % | 93 % | 93 % | 53 % | 100 % | 0,156 |
| C petit modèle lit, GrandNexus juge | 80 % | 93 % | 87 % | 47 % | 100 % | 0,175 |
| D GrandNexus, faits parfaits | 84 % | 93 % | 93 % | 53 % | 100 % | 0,156 |
| E hybride à canaux | 82 % | 93 % | 93 % | 47 % | 100 % | 0,152 |
B − A : exactitude +0 % [−7 ; +7] ; Brier −0,017 [−0,067 ; +0,038].
Perception : lecteur par défaut précision 100 %, rappel 100 %, 0/163 pièges ; petit modèle précision 93,9 %, rappel 83,8 %, 0/163.
| | observé | type | proba | |
|---|---|---|---|---|
| H132 exactitude B > A | 84 % = 84 % | sens | 65 % | ✗ |
| H133 Brier B < A | 0,156 < 0,173 (non significatif) | sens | 80 % | ✓ |
| H134 perception B : rappel ≥ 95 % | 100 % | ampleur | 70 % | ✓ |
| H135 perception C moins bonne | P 93,9 %, R 83,8 % | sens | 85 % | ✓ |
| H136 D ≥ B ≥ C | 84 = 84 ≥ 80 | sens | 60 % | ✓ |
| H137 E : canal « petit modèle » moins cru, ≥ 4/5 sources | 3/5 (écarts de 0,01 à 0,04) | sens | 60 % | ✗ |
Calibration : 4/6, Brier 0,183. Cumul 120 : 0,179.

Lecture :
- Opus a lu les 1 748 faits sans une erreur ni un piège : B est IDENTIQUE à D. Dans ce monde, la perception n'est pas le goulot.
- « Opus lit, GrandNexus juge » ne bat PAS « Opus seul » en exactitude (84 % = 84 %) ; un peu mieux calibré, sans significativité.
  Profils différents : GrandNexus meilleur sur le passé (93 % contre 80 %), Opus meilleur sur les deux sauts (67 % contre 53 %), n = 15 chacun.
- Le petit lecteur perd surtout par OMISSION (rappel 84 %) ; GrandNexus n'y perd que 4 points.
- Critère anti-wrapper non démontré : GrandNexus n'apprend pas nettement à se méfier du petit lecteur. Raison probable (non
  établie) : la fiabilité apprise mesure l'ACCORD des énoncés lus ; une omission ne produit aucun énoncé, donc aucun désaccord.
  L'erreur principale d'un canal de lecture est invisible, par construction, à l'apprentissage de fiabilité.
- Coût : dans un petit monde qui tient dans le contexte, « Opus seul » demande 3 appels ; « Opus lit, GrandNexus juge » en demande 19
  de plus pour la lecture. Ici, l'architecture divisée est plus chère sans être plus juste.

## H-DoutesBoutEnBout (écrite le 2026-10-13 à 12:06 UTC, avant tout calcul ; AUCUN appel)
Question : sur les données de bout en bout (graine 82), chaque architecture sait-elle signaler SES erreurs ?
Opus seul (A) ne dispose que de sa confiance ; GrandNexus (B) dispose de l'objet-réponse (motifs « contestée » et « peu de preuves »).
Pour une question à deux sauts, le motif « contestée » s'applique si l'un des deux faits de la chaîne est contesté.
PUISSANCE TRÈS FAIBLE : ~10 erreurs par architecture sur 55 questions. Résultat descriptif.
- H138 [sens] parmi les réponses de B, la part portant « contestée » est plus élevée chez les fausses que chez les justes   — 75 %
- H139 [sens] « un motif de B » (contestée OU confiance < 0,9) signale une plus grande part des erreurs de B que
       « confiance < 0,9 » ne signale des erreurs d'Opus seul (point estimé)                                              — 55 %

### Verdict H-DoutesBoutEnBout (45 questions à réponse ; 9 erreurs chacune ; aucun appel)
| | « contestée » chez les fausses | chez les justes | erreurs signalées | réponses justes signalées (fausses alertes) |
|---|---|---|---|---|
| B (objet-réponse) | 5/9 | 2/36 | 9/9 (contestée ou confiance < 0,9) | 9/36 (25 %) |
| A (Opus, confiance < 0,9) | — | — | 9/9 | 26/36 (72 %) |
| | observé | type | proba | |
|---|---|---|---|---|
| H138 « contestée » plus fréquent chez les fausses | 5/9 contre 2/36 | sens | 75 % | ✓ |
| H139 B signale une plus grande part de ses erreurs | 9/9 = 9/9 | sens | 55 % | ✗ |
Descriptif (non pré-enregistré, très faible puissance) : les deux signalent toutes leurs erreurs, mais Opus doute presque partout
(72 % de ses réponses justes sous 0,9) ; ses doutes ne distinguent guère. Les signaux de GrandNexus sont plus sélectifs :
18 réponses signalées dont 9 fausses, contre 35 dont 9 pour Opus. Cinq erreurs de GrandNexus sont « certaines et contestées »
(confiance ≥ 0,99) — la signature de la coalition ; Opus y était moyennement confiant (0,75-0,85).
Calibration : 1/2, Brier 0,183. Cumul 122 : 0,179.

# Chantier « désordre réel » — 4. le coureur de fond : un monde plus grand que la fenêtre de lecture

## H-Fond (écrite le 2026-10-13 à 12:18 UTC, avant toute ligne de code de la page et tout appel)
But (Khaled) : savoir TÔT si GrandNexus est inapte ; un résultat négatif n'est pas un échec.
Monde « complice », 80 personnes, 24 organisations, graine neuve 83. Les dépêches arrivent époque par époque. Trois points de
contrôle t = 3, 7, 11 (corpus : 106 Ko, 214 Ko, 319 Ko de texte) ; « maintenant » = t. Questions générées pour chaque t (mêmes types
qu'ailleurs ; historiques tirées uniformément parmi les époques < t) : 38 à t = 3, 38 à t = 7, 114 à t = 11.
Trois concurrents :
- OPUS-FENÊTRE : Opus lit les énoncés les plus récents (époque ≤ t) qui tiennent dans 230 Ko ; à t = 11, il n'en voit qu'une partie
  (la consigne lui dit que les énoncés peuvent ne pas couvrir toutes les époques) ;
- OPUS-RECHERCHE (adversaire de référence, le plus fort raisonnable) : pour chaque question, tous les énoncés d'époque ≤ t qui
  mentionnent la personne ou l'organisation demandée ; pour les deux sauts, aussi ceux des organisations où la personne a été
  dite travailler (les plus récents si plus de 12 Ko par question) ;
- GRANDNEXUS (Méprise) sur les faits d'époque ≤ t. Faits fournis directement, justifié par H-BoutEnBout (Opus a extrait 1 748 faits
  sans erreur : B = D) ; l'avantage de perception est donc nul dans ce régime, pas supposé.
Appels : 10 (fenêtre) + 10 (recherche), modèle par défaut, page à capacité « sample ».
Mesures : exactitude, Brier, par point de contrôle et par type ; différences appariées par bootstrap sur les questions.

VERDICT D'APTITUDE, écrit avant (point t = 11, corpus plus grand que la fenêtre) :
- APTE (coureur de fond, dans ce monde) : GrandNexus significativement meilleur qu'OPUS-RECHERCHE ET qu'OPUS-FENÊTRE (bornes basses > 0).
- AVANTAGE LIMITÉ : significativement meilleur qu'OPUS-FENÊTRE seulement — il ne bat qu'un LLM mal outillé ; sa valeur se réduit
  alors à la calibration, la traçabilité et l'objet-réponse.
- INAPTE sur l'exactitude : OPUS-RECHERCHE significativement meilleur (borne haute < 0) — on cesse de revendiquer l'exactitude.
- Sinon : INDÉTERMINÉ.
Prédictions :
- H140 [sens] OPUS-FENÊTRE moins exact à t = 11 qu'à t = 7 (point estimé)                                — 75 %
- H141 [sens] t = 11 : GrandNexus > OPUS-FENÊTRE, significatif                                        — 70 %
- H142 [sens] t = 11 : GrandNexus > OPUS-RECHERCHE (point estimé)                                     — 45 %
- H143 [sens] t = 11 : Brier de GrandNexus < Brier de chacun des deux bras Opus                        — 65 %
- H144 [ampleur] t = 11, questions historiques : OPUS-FENÊTRE ≤ 60 %                                   — 55 %

## Contexte de lecture de H-Fond (Khaled, 13 octobre 2026 — n'altère aucun critère écrit)
« Coureur de fond », « apte / inapte » sont des analogies ; le verdict reste celui écrit plus haut. Mais il se lira ainsi : l'adversaire
est Opus 5.5 (modèle de pointe ; au-dessus existent Fable et Mythos). « Inapte sur l'exactitude » signifierait « pas meilleur qu'un
modèle de pointe outillé d'une recherche », pas « sans valeur ». L'avantage espéré tient à la nature du graphe (« polymorphe ») :
mémoire au-delà de la fenêtre, intégration du seul nouveau, provenance, révision. Usage au lancement : 22 % de la semaine utilisés.

### Verdict H-Fond (graine 83 ; 190 questions ; 20 appels sans troncature ni illisibilité ; coût : ≈ 46 % d'une session, ≈ 3 % de la semaine)
| | t | exactitude | actuel | historique | deux sauts | sans réponse | Brier |
|---|---|---|---|---|---|---|---|
| GrandNexus | 3 | 76 % | 50 % | 80 % | 80 % | 100 % | 0,208 |
| Opus-fenêtre | 3 | 71 % | 60 % | 70 % | 60 % | 100 % | 0,159 |
| Opus-recherche | 3 | 82 % | 80 % | 80 % | 70 % | 100 % | 0,148 |
| GrandNexus | 7 | 87 % | 90 % | 90 % | 70 % | 100 % | 0,093 |
| Opus-fenêtre | 7 | 87 % | 80 % | 90 % | 80 % | 100 % | 0,122 |
| Opus-recherche | 7 | 89 % | 70 % | 100 % | 90 % | 100 % | 0,094 |
| GrandNexus | 11 | **87 %** | 87 % | 90 % | 73 % | 100 % | **0,129** |
| Opus-fenêtre | 11 | 66 % | 80 % | 57 % | 33 % | 100 % | 0,145 |
| Opus-recherche | 11 | 82 % | 83 % | 83 % | 63 % | 100 % | 0,138 |
t = 11 : GrandNexus − Opus-fenêtre +21,1 % [+13,2 ; +28,9] ; GrandNexus − Opus-recherche +5,3 % [+0,9 ; +10,5].
Brier : différences non significatives (−0,016 [−0,070 ; +0,039] ; −0,009 [−0,047 ; +0,031]).

VERDICT, selon la règle écrite d'avance : **APTE (coureur de fond, dans ce monde)** — significativement meilleur que les deux,
de justesse contre Opus-recherche (borne basse +0,9 point).
| | observé | type | proba | |
|---|---|---|---|---|
| H140 Opus-fenêtre moins exact à 11 qu'à 7 | 66 % < 87 % | sens | 75 % | ✓ |
| H141 GrandNexus > Opus-fenêtre, significatif | +21,1 [+13,2 ; +28,9] | sens | 70 % | ✓ |
| H142 GrandNexus > Opus-recherche | +5,3 (point) | sens | 45 % | ✓ |
| H143 Brier GrandNexus < chacun des deux | 0,129 < 0,145 et < 0,138 (non significatif) | sens | 65 % | ✓ |
| H144 Opus-fenêtre, historique ≤ 60 % | 57 % | ampleur | 55 % | ✓ |
Calibration : 5/5, Brier 0,156. Cumul 127 : 0,178.

Ce que le verdict ne dit PAS (réserves écrites avec lui) :
- UNE graine, UN monde, 114 questions au point décisif ; la marge contre l'adversaire de référence est d'un point au-dessus du seuil.
  Un seul résultat aussi serré ne s'établit pas sans réplication.
- GrandNexus joue à domicile : ses organes ont été construits pour ce type de monde ; il reçoit les faits extraits (justifié sur une
  autre graine, H-BoutEnBout, pas sur celle-ci).
- La recherche d'Opus est celle que j'ai conçue (par nom, plafonnée à 12 Ko par question — plafond jamais atteint ici, 11 Ko au plus) ;
  une meilleure recherche est concevable.
- Profil temporel : GrandNexus est le MOINS bon au début (t = 3 : 76 %, Brier 0,208), à égalité au milieu, meilleur à la fin ; ses
  paramètres s'apprennent sur la durée. Opus-recherche plafonne puis recule ; Opus-fenêtre s'effondre quand le corpus déborde.

## H-FondRéplication (écrite le 2026-10-13 à 12:45 UTC, avant toute ligne de code de la page et tout appel)
Protocole IDENTIQUE à H-Fond (points t = 3, 7, 11 ; 38 / 38 / 114 questions ; Opus-fenêtre 230 Ko ; Opus-recherche par nom,
12 Ko par question ; GrandNexus Méprise sur les faits d'époque ≤ t ; même consigne ; modèle par défaut), dans deux mondes :
- RÉPLICATION : « complice », 80 personnes, 24 organisations, graine neuve 84 (corpus à t = 11 : 321 Ko) ;
- GÉNÉRALISATION : « plausible » (sans coalition ni copie ; erreurs vers des sosies), 100 personnes, 30 organisations, graine neuve 85
  — taille choisie pour déborder de la fenêtre autant que le premier (325 Ko), à la taille habituelle il ne débordait que de justesse.
Même règle de verdict à t = 11, appliquée à chaque monde. Lecture d'ensemble, écrite avant :
- « COUREUR DE FOND ÉTABLI dans le monde de la coalition » si la réplication donne APTE ;
- « AVANTAGE GÉNÉRAL » si les deux mondes donnent APTE ;
- si la réplication ne donne pas APTE, le résultat de la graine 83 est considéré comme NON reproduit.
Secondaire : GrandNexus − Opus-recherche à t = 11, les trois graines (83, 84, 85) réunies.
- H145 [sens] complice 84 : GrandNexus > Opus-recherche, significatif (le verdict se reproduit)                 — 50 %
- H146 [sens] complice 84 : GrandNexus > Opus-recherche (point estimé)                                        — 70 %
- H147 [sens] plausible 85 : GrandNexus > Opus-recherche (point estimé)                                       — 45 %
- H148 [sens] plausible 85 : GrandNexus > Opus-fenêtre, significatif                                          — 75 %
- H149 [sens] dans chacun des deux mondes, exactitude de GrandNexus à t = 11 ≥ à t = 3 (profil de la tortue)    — 80 %
- H150 [sens] trois graines réunies, t = 11 : GrandNexus − Opus-recherche significativement > 0                — 60 %
Amendement AVANT tout appel (12:46 UTC) : avec le plafond de 12 Ko, 8 contextes sur 190 auraient été tronqués dans le
monde de la coalition (aucun dans H-Fond, où le plafond n'avait jamais été atteint). Pour que la réplication ne handicape pas
l'adversaire davantage que l'original, le plafond est SUPPRIMÉ : chaque question reçoit tous les énoncés qui la concernent.
Amendement prudent (il ne peut qu'avantager Opus-recherche). Prédictions inchangées.

### Verdict H-FondRéplication (40 appels ; coût : la session a atteint 100 %, ≈ 4 % de la semaine, et ≈ 2,5 € de crédits de secours)
| monde | t | GrandNexus | Opus-fenêtre | Opus-recherche |
|---|---|---|---|---|
| coalition (84) | 3 / 7 / 11 | 82 / 82 / 80 % | 71 / 61 / 57 % | 74 / 74 / 75 % |
| erreurs ordinaires (85) | 3 / 7 / 11 | 89 / 87 / 88 % | 61 / 63 / 63 % | 63 / 74 / 75 % |
t = 11, GrandNexus − Opus-recherche : coalition 84 +5,3 [−0,9 ; +12,3] ; erreurs ordinaires 85 +13,2 [+5,3 ; +21,1].
t = 11, GrandNexus − Opus-fenêtre : +22,8 [+14,9 ; +31,6] ; +24,6 [+14,9 ; +35,1].
Un lot illisible (fenêtre, erreurs ordinaires, t = 11, lot 3) : sans ses 19 questions, GrandNexus − Opus-fenêtre +14,7 [+5,3 ; +25,3],
GrandNexus − Opus-recherche +11,6 [+4,2 ; +20,0] — le verdict ne change pas.
Trois graines réunies (83, 84, 85), t = 11, GrandNexus − Opus-recherche : +7,9 [+3,8 ; +11,7] (342 questions).
VERDICTS selon les règles écrites d'avance :
- coalition, graine 84 : AVANTAGE LIMITÉ → le « APTE » de la graine 83 est formellement NON REPRODUIT (même direction, même écart
  de +5,3 points, mais l'intervalle touche zéro) ;
- erreurs ordinaires, graine 85 : APTE ;
- lecture d'ensemble : ni « coureur de fond établi dans la coalition », ni « avantage général » au sens strict ; le critère secondaire
  (trois graines réunies) est significatif.
| | observé | type | proba | |
|---|---|---|---|---|
| H145 coalition 84, significatif | +5,3 [−0,9 ; +12,3] | sens | 50 % | ✗ |
| H146 coalition 84, point | +5,3 | sens | 70 % | ✓ |
| H147 erreurs ordinaires, point | +13,2 | sens | 45 % | ✓ |
| H148 erreurs ordinaires > fenêtre, significatif | +24,6 | sens | 75 % | ✓ |
| H149 profil de la tortue (t = 11 ≥ t = 3) dans les deux | 80 < 82 ; 88 < 89 | sens | 80 % | ✗ |
| H150 trois graines réunies, significatif | +7,9 [+3,8 ; +11,7] | sens | 60 % | ✓ |
Calibration : 4/6, Brier 0,251. Cumul 133 : 0,181.
Lecture : sur trois graines, GrandNexus devance TOUJOURS Opus-recherche quand le monde déborde de la fenêtre (+5,3 ; +5,3 ; +13,2),
de façon significative deux fois sur trois et sur l'ensemble. Le « profil de la tortue » ne se reproduit pas : dans ces deux mondes,
GrandNexus est bon dès le début ; c'est surtout Opus qui se dégrade ou plafonne. Réserves inchangées : organes faits pour ces mondes,
faits fournis sans lecture, recherche conçue par moi, une seule taille de monde.

# Chantier « désordre réel » — 5. hors du modèle : l'avantage vient-il du graphe ou de la forme du monde ?

## H-HorsModèle (écrite le 2026-10-13 à 17:42 UTC, avant tout appel et avant de voir aucun score)
Monde « hors modèle » (hors_modele.py, graine neuve 86, 80 personnes, 24 organisations, 4 sources, AUCUNE coalition) où toutes
les hypothèses des organes sont fausses à la fois : retours à l'ancienne adresse (non markovien), emplois par vagues, retard variable
(Registre, 0-2), fiabilité qui se dégrade (Gazette 0,90 → 0,55 après l'époque 5), erreurs vers des valeurs fétiches (Radio), copie
avec délai variable (Forum). Aucune ligne de GrandNexus n'est modifiée.
Protocole de H-Fond (t = 3, 7, 11 ; 38 / 38 / 114 questions ; recherche par nom SANS plafond). Opus-fenêtre retiré (il s'effondre
à chaque fois ; économie d'usage) : seul l'adversaire de référence, Opus-recherche, est appelé (10 appels).
VERDICT écrit avant, à t = 11, GrandNexus − Opus-recherche :
- ROBUSTE HORS MODÈLE si significativement > 0 ;
- AVANTAGE DÉPENDANT DU MODÈLE si l'intervalle contient 0 ;
- BATTU HORS MODÈLE si significativement < 0.
- H151 [sens] t = 11 : GrandNexus > Opus-recherche (point estimé)                                      — 45 %
- H152 [sens] t = 11 : GrandNexus > Opus-recherche, significatif                                      — 25 %
- H153 [ampleur] t = 11 : exactitude de GrandNexus < 80 % (il souffre de la mauvaise spécification)    — 60 %
Note avant appel : corpus à t = 11 de 243 Ko (3 612 énoncés) — sans importance ici, Opus-recherche reçoit tous les énoncés de chaque question (lot le plus lourd : 87 Ko).

### Verdict H-HorsModèle (graine 86 ; 10 appels, aucun lot tronqué ni illisible ; coût : préparation ≈ 27 % de session, appels ≈ 10 %)
| t | GrandNexus | Opus-recherche | actuel | historique | deux sauts | sans réponse |
|---|---|---|---|---|---|---|
| 3 | 82 % (Brier 0,183) | 66 % (0,190) | 70 / 50 % | 80 / 40 % | 80 / 80 % | 100 / 100 % |
| 7 | 82 % (0,124) | 71 % (0,245) | 70 / 80 % | 100 / 80 % | 60 / 30 % | 100 / 100 % |
| 11 | **85 %** (0,128) | 72 % (0,204) | 80 / 70 % | 87 / 70 % | 77 / 53 % | 100 / 100 % |
t = 11 : GrandNexus − Opus-recherche +13,2 % [+5,3 ; +21,1] → VERDICT : **ROBUSTE HORS MODÈLE**.
| | observé | type | proba | |
|---|---|---|---|---|
| H151 GrandNexus > Opus-recherche (point) | +13,2 | sens | 45 % | ✓ |
| H152 significatif | [+5,3 ; +21,1] | sens | 25 % | ✓ |
| H153 GrandNexus < 80 % | 85 % | ampleur | 60 % | ✗ |
Calibration : 2/3, Brier 0,408 — ma pire série : j'ai nettement sous-estimé GrandNexus. Cumul 136 : 0,186.
Lecture : six hypothèses des organes fausses à la fois, sans une ligne d'adaptation, et GrandNexus ne recule pas (85 %). Ses organes
se comportent comme des mécanismes statistiques généraux — pondérer les sources par leur accord, lisser dans le temps, apprendre
la forme des erreurs (les valeurs fétiches ressemblent à une confusion partagée) — plutôt que comme des astuces taillées pour un monde.
La réserve « clé taillée pour sa serrure » s'en trouve fortement affaiblie, pour ce type de désordre.
Réserves qui demeurent : une graine ; mondes synthétiques ; faits fournis sans lecture (lecture parfaite d'Opus montrée sur une autre
graine) ; recherche conçue par moi ; Opus répond à 19 questions par appel en lisant — un pipeline qui le ferait raisonner question par
question, plus coûteux, serait un adversaire plus fort.
Synthèse des quatre mondes qui débordent (graines 83, 84, 85, 86) : GrandNexus − Opus-recherche = +5,3 ; +5,3 ; +13,2 ; +13,2.

# PROGRAMME en deux étapes (Khaled : « ce ne sont pas des directions, ce sont des étapes » — contre l'optimisation locale)
Observation EXPLORATOIRE (graines 83-86 réunies, t = 11, 456 questions, aucune nouvelle mesure) : GrandNexus − Opus-recherche =
actuel +6 [−1 ; +12] ; historique +10 [+2 ; +18] ; deux sauts +19 [+11 ; +28] ; sans réponse 0. L'avantage tient à la COMPOSITION et
au TEMPS, pas au présent. Biais constant identifié, hérité par tous les tests : Opus répond à 19 questions par lecture, d'un bloc.
Étape 1 — même questions, même contexte, seul le FORMAT d'Opus change (une question par appel, raisonnement permis).
Étape 2 — premier pas vers des données réelles ; conçue après l'étape 1, avec les MÊMES mesures (types, exactitude, Brier, doutes),
pour que les deux se lisent ensemble.
Lecture conjointe, écrite avant : si l'étape 1 referme l'écart sur les deux sauts, l'avantage de GrandNexus sur la composition tenait
au format ; il ne resterait alors que le temps — et c'est sur le temps que l'étape 2 devra porter son regard en premier.

## H-QuestionParQuestion (étape 1, écrite le 2026-10-13 à 18:09 UTC, avant tout appel)
120 questions tirées des quatre mondes (t = 11), 40 actuelles, 40 historiques, 40 en deux sauts (générateur dédié) ; les questions
« sans réponse » sont exclues (100 % pour tous). Opus reçoit UNE question par appel, avec exactement le contexte de recherche déjà
donné, la même consigne, et le droit de raisonner avant de conclure par une ligne JSON. Comparaisons APPARIÉES sur les mêmes questions :
Opus question par question / Opus par lots de 19 (déjà mesuré) / GrandNexus (déjà scellé). 120 appels courts.
- H154 [sens] deux sauts : Opus question par question > Opus par lots (point estimé)                    — 75 %
- H155 [sens] ensemble : Opus question par question > Opus par lots, significatif                     — 55 %
- H156 [sens] ensemble : GrandNexus > Opus question par question (point estimé)                        — 55 %
- H157 [sens] deux sauts : GrandNexus > Opus question par question, significatif                       — 40 %

### Verdict H-QuestionParQuestion (étape 1 ; 120 questions appariées ; 0 réponse illisible)
| type | GrandNexus | Opus par lots | Opus une par une | une par une − lots | GrandNexus − une par une |
|---|---|---|---|---|---|
| actuel | 88 % | 82 % | 80 % | −2 [−8 ; 0] | +8 [0 ; +18] |
| historique | 82 % | 70 % | 72 % | +2 [0 ; +8] | +10 [−2 ; +22] |
| deux sauts | 78 % | 62 % | 65 % | +2 [−10 ; +15] | +12 [−2 ; +28] |
| ensemble | **82 %** | 72 % | 72 % | +1 [−4 ; +6] | **+10 [+3 ; +18]** |
| | observé | type | proba | |
|---|---|---|---|---|
| H154 deux sauts : une par une > lots (point) | 65 % > 62 % | sens | 75 % | ✓ |
| H155 ensemble : une par une > lots, significatif | +1 [−4 ; +6] | sens | 55 % | ✗ |
| H156 GrandNexus > une par une (point) | +10 | sens | 55 % | ✓ |
| H157 deux sauts : GrandNexus > une par une, significatif | +12 [−2 ; +28] | sens | 40 % | ✗ |
Calibration : 2/4, Brier 0,182. Cumul 140 : 0,186.
Lecture conjointe (écrite avant : « si l'étape 1 referme l'écart sur les deux sauts… ») : elle NE le referme PAS. Laisser Opus
raisonner question par question ne change rien (72 % = 72 %). Le format par lots n'était PAS le biais constant soupçonné ;
l'avantage de GrandNexus (+10 points sur ces questions) n'en dépendait pas. Les écarts par type vont dans le même sens que la vue
réunie (passé, deux sauts) mais 40 questions par type ne suffisent pas à les rendre significatifs isolément.

# Étape 2 — données réelles : ÉTUDE DE FAISABILITÉ (exploration, aucun test, aucun appel à Opus)
Accès : Wikidata (SPARQL) et Wikipédia (API des révisions, section 0) joignables depuis l'environnement de calcul.
Vérité candidate : Wikidata, maires avec dates de début et de fin (P6, P580, P582).
Sondage : Marseille et Bordeaux, éditions fr / en / de / es / it, infobox au 1er de chaque mois de 2019-01 à 2021-06 (300 lectures,
16 échecs de récupération à examiner). Données : faisabilite_wiki.json.
Observé (réel, non provoqué) :
- RETARD : l'édition allemande de Marseille affiche Gaudin cinq mois après l'élection de Rubirola, puis Rubirola quatre mois après
  l'arrivée de Payan ; fr / en / es suivent en moins d'un mois. Une vraie source en retard, avec une valeur fausse intermédiaire.
- DÉPENDANCE À LA VÉRITÉ : l'infobox allemande de Bordeaux ne contient aucun nom dans son texte — vraisemblablement alimentée par
  Wikidata au rendu. Une source qui recopie la « vérité » ne peut pas servir à juger contre elle.
- VÉRITÉ EN RETARD POSSIBLE : Wikidata ne montre aucune fin de mandat en 2026 pour Lyon, Marseille, Toulouse, Nantes, Strasbourg
  malgré les municipales de mars 2026 — réélections ou retard de la référence : à vérifier.
- FUITE À ÉVITER : ce sondage repère les maires en cherchant les noms fournis par Wikidata ; dans un vrai test, l'extraction ne devra
  JAMAIS dépendre de la liste de vérité (lecture des champs, ou lecteur LLM sans liste).
Conséquences pour la conception : (1) extraction indépendante de la vérité ; (2) exclure ou traiter comme copies les infobox alimentées
par Wikidata ; (3) vérité figée à une date, et vérifiée ; (4) les changements de maire sont rares : il faut beaucoup de villes — les
municipales de 2020 offrent des centaines de transitions le même mois.

## Étape 2 — SPÉCIFICATION (écrite le 2026-10-13 à 19:41 UTC, avant toute collecte au-delà du sondage)
Entités : les 60 communes françaises les plus peuplées selon Wikidata (P1082), quel que soit leur historique de maires.
Sources : éditions fr, en, de, es, it de Wikipédia ; énoncé = valeur du champ « maire » de l'infobox, au 1er de chaque mois de 2019-07
à 2021-06 (24 époques, autour des municipales de 2020).
Piège 1 — extraction indépendante de la vérité : la valeur est lue dans le CHAMP de l'infobox (clé propre à chaque langue), jamais en
cherchant des noms connus. Règles d'extraction réglées sur Marseille et Bordeaux seulement (déjà sondées), puis figées.
Piège 2 — sources alimentées par Wikidata : un champ vide ou absent ne produit aucun énoncé ; ces sources s'excluent d'elles-mêmes.
Une copie MANUELLE de Wikidata reste indétectable : limite déclarée.
Piège 3 — vérité en retard : vérité = Wikidata (P6, P580, P582), figée au moment de la collecte ; questions limitées à 2019-2021,
période close depuis cinq ans. Correspondance des noms : égalité après normalisation (casse, accents, espaces), sinon même nom de
famille et même initiale.
Piège 4 — mémoire d'Opus : TOUT est anonymisé (villes et personnes remplacées par des pseudonymes fixes) avant d'être montré à
GrandNexus comme à Opus. Les retards, copies, erreurs et fautes du réel sont conservés ; une graphie différente reçoit un pseudonyme
différent (le bruit réel reste du bruit).
Comparaison : GrandNexus (Méprise, sources = éditions, relation unique « dirige ») contre Opus-recherche (pour chaque question, tous les
énoncés anonymisés de la commune). Questions : « Qui était maire de X au 1er <mois> ? », 4 mois par commune tirés uniformément ;
rapportées aussi sur la strate « transition » (±6 mois d'un changement dans la vérité).
Hypothèses et verdict : écrits APRÈS la collecte (qui ne révèle aucun score) mais AVANT tout calcul de GrandNexus et tout appel à Opus.

## H-Réel (écrite le 2026-10-13 à 19:57 UTC — après la collecte, avant tout calcul de GrandNexus et tout appel à Opus)
Collecte : 297 articles (60 communes × 5 éditions), instantanés au 1er de chaque mois 2019-07 → 2021-06 (24 époques) ; deux méthodes
concordantes (937/937). Édition allemande lisible 9 % des mois (infobox alimentée par Wikidata : exclue d'elle-même). Vérité Wikidata
figée le 13/10/2026, définie pour 1 226 couples (commune, mois) ; ambigus (42) et absents (172) exclus.
Anonymisation : chaque commune et chaque graphie distincte de nom reçoit un pseudonyme fixe ; les éditions deviennent « Source A…E ».
Énoncé = « à l'époque k, la source S affiche X comme maire de V ». Questions : 4 époques par commune, tirées uniformément parmi celles
à vérité définie (générateur dédié) ; strate « transition » = époques à ±6 mois d'un changement de maire dans la vérité.
Juste = la graphie répondue correspond au maire vrai (égalité normalisée, sinon même nom et même initiale).
GrandNexus : Méprise, relation unique, sources = éditions ; aucune adaptation. Opus-recherche : pour chaque question, tous les énoncés
de la commune ; lots de 19 (le format est sans effet, H-QuestionParQuestion).
VERDICT écrit avant, sur l'ensemble : AVANTAGE RÉEL si GrandNexus − Opus significativement > 0 ; ÉGALITÉ si l'intervalle contient 0 ;
BATTU SUR LE RÉEL si significativement < 0. Strate « transition » rapportée à part.
- H158 [sens]    ensemble : GrandNexus > Opus-recherche (point estimé)                     — 50 %
- H159 [sens]    strate transition : GrandNexus > Opus-recherche (point estimé)          — 55 %
- H160 [ampleur] ensemble : les deux ≥ 90 % (le réel est surtout stable)                — 60 %
- H161 [sens]    ensemble : GrandNexus > Opus-recherche, significatif                     — 20 %

### Verdict H-Réel (220 questions ; 12 appels sans troncature ni illisibilité)
| | n | GrandNexus | Opus-recherche | écart |
|---|---|---|---|---|
| ensemble | 220 | 94,1 % (Brier 0,038) | 95,5 % (0,037) | −1,4 [−3,2 ; 0,0] |
| transition (±6 mois) | 22 | 95,5 % | 100 % | −4,5 [−13,6 ; 0,0] |
| hors transition | 198 | 93,9 % | 94,9 % | −1,0 [−2,5 ; 0,0] |
Désaccords : 3, tous en faveur d'Opus (test exact des paires discordantes : p ≈ 0,25). VERDICT selon la règle : **ÉGALITÉ**
(l'intervalle touche 0) — point estimé légèrement en faveur d'Opus.
| | observé | type | proba | |
|---|---|---|---|---|
| H158 GrandNexus > Opus (point) | −1,4 | sens | 50 % | ✗ |
| H159 transition : GrandNexus > Opus (point) | −4,5 | sens | 55 % | ✗ |
| H160 les deux ≥ 90 % | 94 % et 96 % | ampleur | 60 % | ✓ |
| H161 GrandNexus > Opus, significatif | non | sens | 20 % | ✗ |
Calibration : 1/4, Brier 0,188. Cumul 144 : 0,186.

Examen des 13 erreurs (DESCRIPTIF, après coup ; ne modifie pas le verdict) :
- La VÉRITÉ semble en retard dans 6 cas (selon mes connaissances, non vérifiées par recherche) : Metz (Grosdidier maire depuis 2020,
  Wikidata dit Gros), Saint-Paul (Bello depuis 2020, Wikidata dit Sinimalé), Aubervilliers (Franclet depuis 2020, Wikidata dit
  Derkaoui). Sur ces cas, les sources majoritaires et les deux juges ont raison contre la référence. Strasbourg 2020-07 : la référence
  date le mandat de l'élection (28 juin), les sources de l'installation (début juillet) — question de définition.
- Saint-Denis (4 cas) : une seule édition, sans valeur lisible — personne ne pouvait répondre.
- Erreurs PROPRES à GrandNexus (2) : Orléans et Nancy au 1er juillet 2020 — toutes les sources affichent encore l'ancien maire,
  GrandNexus répond déjà le nouveau. Il ANTICIPE : ayant appris que des sources sont en retard, il place le changement avant leurs mises
  à jour. Juste dans nos mondes ; ici, le changement est survenu quelques jours APRÈS le 1er juillet. Premier mode d'échec propre au réel.
- Le seul « succès » d'Opus seul (Saint-Paul 2020-10) correspond à la référence en retard, donc probablement faux dans le réel.
Lecture (interprétation, non établie) : ce réel est calme (22 questions de transition), chaque ville tient en ~120 énoncés lus en entier,
et il n'y a aucune composition : aucune des conditions où GrandNexus gagnait n'était présente. Les deux leçons propres au réel :
la référence elle-même est une source qui se trompe ; et le modèle temporel de GrandNexus peut anticiper à tort.
