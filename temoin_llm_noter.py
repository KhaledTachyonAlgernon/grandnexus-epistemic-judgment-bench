"""H-TémoinLLM : réponses de GrandNexus sur les mêmes mondes et questions, puis notation des deux témoins.
Étape 1 (ici) : GrandNexus. Étape 2 : les réponses du témoin LLM, relues depuis la base de la page, sont notées
exactement de la même façon."""
import json, sys
from monde import generer
from meprise import Meprise

MONDES = ("facile", "echo", "menteur", "complice")


def grandnexus():
    out = {}
    for w in MONDES:
        m = generer(w, 79, n_personnes=40, n_orgs=8, n_questions=60)
        o = Meprise(); o.ingerer(m.enonces)
        cibles = m.menteur[2] if m.menteur else set()
        T = m.n_epoques - 1
        L = []
        for q in m.questions:
            rep, conf = o.repondre(q)
            dep = False
            if cibles and q.type in ("actuel", "historique"):
                dep = (q.sujet, q.chaine[0]) in cibles
            elif cibles and q.type == "deux_sauts":
                org = m.verite[(q.sujet, "travaille")][T]
                dep = (q.sujet, "travaille") in cibles or (org, "dirige") in cibles
            L.append({"id": q.id, "type": q.type, "attendu": q.attendu, "gn": rep, "gn_conf": conf, "cible": dep})
        out[w] = L
    return out


if __name__ == "__main__":
    G = grandnexus()
    json.dump(G, open("/mnt/user-data/outputs/grandnexus_banc/temoin_gn.json", "w"), ensure_ascii=False)
    for w, L in G.items():
        ok = sum((x["gn"] is None) if x["attendu"] is None else (x["gn"] == x["attendu"]) for x in L)
        print(f"{w:<9} GrandNexus : {ok}/{len(L)} justes ; questions dépendant d'un fait ciblé : {sum(x['cible'] for x in L)}")


def noter():
    import random
    G = json.load(open("/mnt/user-data/outputs/grandnexus_banc/temoin_gn.json"))
    norm = lambda v: None if v is None or str(v).strip().upper() in ("INCONNU", "") else str(v).strip().lower()
    lignes = []
    for w in MONDES:
        llm = {}
        for i in range(3):
            d = json.load(open(f"/mnt/user-data/outputs/grandnexus_banc/temoin_reponses/temoin/{w}_{i}.json"))
            for r in d["reponses"]:
                llm[int(r["id"])] = (norm(r.get("reponse")), float(r.get("confiance", 0) or 0))
        for x in G[w]:
            att = norm(x["attendu"])
            rl, cl = llm.get(x["id"], (None, 0.0))
            rg, cg = norm(x["gn"]), x["gn_conf"]
            jl = (rl is None) if att is None else (rl == att)
            jg = (rg is None) if att is None else (rg == att)
            lignes.append({"monde": w, "id": x["id"], "type": x["type"], "cible": x["cible"], "llm": int(jl), "gn": int(jg),
                           "repondable": att is not None,
                           "b_llm": ((cl if rl is not None else 0.0) - (rl == att)) ** 2 if att is not None else None,
                           "b_gn": ((cg if rg is not None else 0.0) - (rg == att)) ** 2 if att is not None else None,
                           "manquante": x["id"] not in llm})
    return lignes


def ic(diff, tirages=4000, graine=1):
    rng = random.Random(graine) if False else __import__("random").Random(graine)
    n = len(diff)
    s = sorted(sum(diff[rng.randrange(n)] for _ in range(n)) / n for _ in range(tirages))
    return sum(diff) / n, s[int(0.025 * tirages)], s[int(0.975 * tirages) - 1]


def bilan():
    L = noter()
    print(f"Réponses manquantes du témoin : {sum(x['manquante'] for x in L)}\n")
    print(f"{'monde':<10}{'témoin LLM':>12}{'GrandNexus':>12}   écart GN − LLM [IC 95 %]")
    for w in MONDES:
        E = [x for x in L if x["monde"] == w]
        m, lo, hi = ic([x["gn"] - x["llm"] for x in E])
        print(f"{w:<10}{sum(x['llm'] for x in E) / len(E):>11.0%} {sum(x['gn'] for x in E) / len(E):>11.0%}   {m:+.0%} [{lo:+.0%} ; {hi:+.0%}]")
    print("\nPar type de question (4 mondes réunis) :")
    for t in ("actuel", "historique", "deux_sauts", "sans_reponse"):
        E = [x for x in L if x["type"] == t]
        m, lo, hi = ic([x["gn"] - x["llm"] for x in E])
        print(f"   {t:<13} témoin {sum(x['llm'] for x in E) / len(E):.0%}   GrandNexus {sum(x['gn'] for x in E) / len(E):.0%}   GN − LLM {m:+.0%} [{lo:+.0%} ; {hi:+.0%}]")
    C = [x for x in L if x["monde"] == "complice" and x["cible"]]
    print(f"\nComplice, questions dépendant d'un fait ciblé (n = {len(C)}) : témoin {sum(x['llm'] for x in C)}/{len(C)} justes ; GrandNexus {sum(x['gn'] for x in C)}/{len(C)}")
    M = [x for x in L if x["monde"] == "menteur" and x["cible"]]
    print(f"Menteur, questions dépendant d'un fait ciblé (n = {len(M)}) : témoin {sum(x['llm'] for x in M)}/{len(M)} ; GrandNexus {sum(x['gn'] for x in M)}/{len(M)}")
    R = [x for x in L if x["repondable"]]
    m, lo, hi = ic([x["b_llm"] - x["b_gn"] for x in R])
    print(f"\nBrier (questions à réponse, 4 mondes) : témoin {sum(x['b_llm'] for x in R) / len(R):.3f} ; GrandNexus {sum(x['b_gn'] for x in R) / len(R):.3f} ;"
          f" LLM − GN {m:+.3f} [{lo:+.3f} ; {hi:+.3f}]")


if len(sys.argv) > 1 and sys.argv[1] == "noter":
    bilan()
