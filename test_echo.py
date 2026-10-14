"""Test pré-enregistré H-Écho (H8-H11) : tableau, boîte de verre, signature des erreurs."""
from evaluer import tableau, TEMOINS, ORGANES, PLAFOND
from monde import generer
from pesee import Pesee

tableau(presets=("echo",), systemes=TEMOINS + [ORGANES[0], ORGANES[3]] + PLAFOND)

print("\n── boîte de verre, variante D (monde écho)")
for g in (0, 1, 2):
    m = generer("echo", g)
    o = Pesee(True, True, un_contre_tous=True)
    o.ingerer(m.enonces)
    if g == 0:
        print(f"{'source':<14}{'apprise':>9}{'vraie':>7}{'  copie'}")
        for s in m.sources:
            print(f"{s.nom:<14}{o.f[s.nom]:>9.2f}{s.fiabilite:>7.2f}  {s.copie or ''}")
    # H10 : les erreurs de D reprennent-elles la valeur de La Dépêche ?
    dep = {}
    for e in m.enonces:
        if e.source == "La Dépêche":
            dep.setdefault((e.sujet, e.relation), []).append((e.epoque, e.objet))
    err = echo = 0
    for q in m.questions:
        if q.type not in ("actuel", "historique"):
            continue
        rep, _ = o.repondre(q)
        if rep is None or rep == q.attendu:
            continue
        err += 1
        avant = [x for x in dep.get((q.sujet, q.chaine[0]), []) if x[0] <= q.epoque]
        if avant and max(avant)[1] == rep:
            echo += 1
    print(f"   graine {g} : Dépêche apprise {o.f['La Dépêche']:.2f} | Registre appris "
          f"{o.f['Le Registre']:.2f} | erreurs reprenant La Dépêche : {echo}/{err}")
