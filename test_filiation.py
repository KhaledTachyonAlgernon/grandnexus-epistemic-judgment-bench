"""Test pré-enregistré H-Filiation (H12-H15)."""
import sys
from evaluer import tableau, PLAFOND
from monde import generer
from pesee import Pesee
from temoins import Majorite
from filiation import Filiation

mondes = tuple(sys.argv[1:]) or ("echo", "hostile", "realiste", "facile")
tableau(presets=mondes, systemes=[lambda m: Majorite(), lambda m: Pesee(True, True, un_contre_tous=True),
                                  lambda m: Filiation()] + PLAFOND)
if "echo" in mondes:
    print("\n── H12 : filiations détectées (monde écho)")
    for g in (0, 1, 2):
        m = generer("echo", g)
        o = Filiation()
        o.ingerer(m.enonces)
        print(f"   graine {g} : {o.rapport()['parent']}")
        if g == 0:
            print(f"   {'source':<14}{'fiabilité apprise':>18}{'vraie':>7}")
            for s in m.sources:
                print(f"   {s.nom:<14}{o.f[s.nom]:>18.2f}{s.fiabilite:>7.2f}")
for monde in [x for x in mondes if x != "echo"]:
    o = Filiation()
    o.ingerer(generer(monde, 0).enonces)
    print(f"── fausses accusations ? « {monde} » graine 0 : {o.rapport()['parent']}")
