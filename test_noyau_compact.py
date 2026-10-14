"""Smoke and contract tests for the compact epistemic judgment core."""
from base import Enonce
from coherence import Coherence2, Coherence3
from meprise import Meprise


def run():
    assertions = [
        Enonce(0, 0, "A", "Maison O", "dirige", "Personne P", ""),
        Enonce(1, 0, "A", "Personne P", "travaille", "Maison X", ""),
        Enonce(2, 0, "B", "Maison O", "dirige", "Personne P", ""),
        Enonce(3, 0, "B", "Personne P", "travaille", "Maison O", ""),
        Enonce(4, 0, "C", "Maison O", "dirige", "Personne P", ""),
        Enonce(5, 0, "C", "Personne P", "travaille", "Maison O", ""),
    ]

    reference = Meprise()
    reference.ingerer(assertions)
    neutral = Coherence3(contraintes=())
    neutral.ingerer(assertions)
    assert neutral.croyance == reference.croyance
    assert neutral.dom == reference.dom

    c1 = Coherence2()
    c1.ingerer(assertions)
    assert c1.ecartes, "C1 should identify the self-contradictory source"
    assert ("A", ("Personne P", "travaille"), "Maison X") in c1.ecartes

    # C2 and C3 are exercised with explicit declared facts and a self-contradiction.
    extended = [
        Enonce(10, 0, "A", "Maison O", "siege", "Quartier 1", ""),
        Enonce(11, 0, "A", "Maison O", "dirige", "Personne P", ""),
        Enonce(12, 0, "A", "Personne P", "habite", "Quartier 2", ""),
        Enonce(13, 0, "B", "Maison O", "siege", "Quartier 1", ""),
        Enonce(14, 0, "B", "Maison O", "dirige", "Personne P", ""),
        Enonce(15, 0, "B", "Personne P", "habite", "Quartier 1", ""),
        Enonce(16, 0, "C", "Personne P", "conjoint", "Personne Q", ""),
        Enonce(17, 0, "C", "Personne P", "habite", "Quartier 1", ""),
        Enonce(18, 0, "C", "Personne Q", "habite", "Quartier 2", ""),
        Enonce(19, 0, "D", "Personne P", "conjoint", "Personne Q", ""),
        Enonce(20, 0, "D", "Personne P", "habite", "Quartier 1", ""),
        Enonce(21, 0, "D", "Personne Q", "habite", "Quartier 1", ""),
    ]
    c3 = Coherence3()
    c3.ingerer(extended)
    assert c3.ecartes, "Coherence3 should expose at least one declared-constraint contradiction"
    assert any(item[0] == "A" for item in c3.ecartes)

    print("compact_core_smoke=PASS")


if __name__ == "__main__":
    run()
