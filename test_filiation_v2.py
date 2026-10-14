"""Test pré-enregistré H-Filiation-v2, sur graines NEUVES (3, 4, 5) uniquement."""
import sys
from evaluer import tableau, PLAFOND
from monde import generer
from pesee import Pesee
from temoins import Majorite
from filiation import Filiation

NEUVES = (3, 4, 5)
monde = sys.argv[1]
tableau(graines=NEUVES, presets=(monde,),
        systemes=[lambda m: Majorite(), lambda m: Pesee(True, True, un_contre_tous=True),
                  lambda m: Filiation()] + PLAFOND)
for g in NEUVES:
    o = Filiation()
    o.ingerer(generer(monde, g).enonces)
    print(f"   graine {g} — filiations : {o.rapport()['parent'] or 'aucune'}")
