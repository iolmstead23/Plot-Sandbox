"""Static sample knowledge graph: labels, edges, and degree-derived weights.

No imports from sibling packages.
"""

from collections import Counter

SAMPLE_EDGES: list[tuple[str, str]] = [
    ("Algorithm", "Recursion"),
    ("Algorithm", "Sorting Algorithms"),
    ("Algorithm", "Depth First Search"),
    ("Algorithm", "Breadth First Search"),
    ("Algorithm", "Graph Theory"),
    ("Algorithm", "Optimization"),
    ("Machine Learning", "Algorithm"),
    ("Machine Learning", "Decision Tree"),
    ("Machine Learning", "Neural Network"),
    ("Machine Learning", "Gradient Descent"),
    ("Machine Learning", "Bayes Theorem"),
    ("Machine Learning", "Random Forest"),
    ("Machine Learning", "Statistics"),
    ("Graph Theory", "Depth First Search"),
    ("Graph Theory", "Breadth First Search"),
    ("Graph Theory", "Matrix"),
    ("Mathematics", "Calculus"),
    ("Mathematics", "Discrete Mathematics"),
    ("Mathematics", "Set Theory"),
    ("Mathematics", "Statistics"),
    ("Calculus", "Derivative"),
    ("Calculus", "Integral"),
    ("Calculus", "Gradient Descent"),
    ("Discrete Mathematics", "Combinatorics"),
    ("Discrete Mathematics", "Set Theory"),
    ("Discrete Mathematics", "Cardinality"),
    ("Set Theory", "Cardinality"),
    ("Data Structure", "Binary Tree"),
    ("Data Structure", "Hash Table"),
    ("Computer Science", "Algorithm"),
    ("Computer Science", "Data Structure"),
    ("Computer Science", "Machine Learning"),
    ("Computer Science", "Graph Theory"),
    ("Data", "Data Structure"),
    ("Data", "Statistics"),
    ("Data", "Machine Learning"),
    ("Statistics", "Probability"),
    ("Statistics", "Markov Chain"),
    ("Statistics", "Bayes Theorem"),
    ("Probability", "Markov Chain"),
    ("Probability", "Bayes Theorem"),
    ("Optimization", "Gradient Descent"),
    ("Optimization", "Algorithm"),
    ("Function", "Derivative"),
    ("Function", "Mathematics"),
    ("Vector Space", "Matrix"),
    ("Vector Space", "Eigenvalue"),
    ("Matrix", "Eigenvalue"),
]


# Leaf nodes from the prompt that should exist even if isolated.
_PROMPT_LEAVES: list[str] = [
    "Recursion",
    "Sorting Algorithms",
    "Decision Tree",
    "Neural Network",
    "Gradient Descent",
    "Set Theory",
    "Combinatorics",
    "Cardinality",
    "Derivative",
    "Integral",
    "Matrix",
    "Vector Space",
    "Binary Tree",
    "Hash Table",
    "Depth First Search",
    "Breadth First Search",
    "Eigenvalue",
    "Markov Chain",
    "Bayes Theorem",
    "Random Forest",
]


def _build_labels() -> list[str]:
    seen: dict[str, None] = {}
    for a, b in SAMPLE_EDGES:
        seen.setdefault(a, None)
        seen.setdefault(b, None)
    for leaf in _PROMPT_LEAVES:
        seen.setdefault(leaf, None)
    return list(seen.keys())


def _build_weights(labels: list[str]) -> list[float]:
    # Use unique undirected edges so weight matches DOM-side graph degree
    # even when SAMPLE_EDGES contains both (a,b) and (b,a) for the same pair.
    seen: set[tuple[str, str]] = set()
    deg: Counter[str] = Counter()
    for a, b in SAMPLE_EDGES:
        if a == b:
            continue
        key = (a, b) if a < b else (b, a)
        if key in seen:
            continue
        seen.add(key)
        deg[a] += 1
        deg[b] += 1
    return [1.0 + float(deg[label]) for label in labels]


SAMPLE_LABELS: list[str] = _build_labels()
SAMPLE_WEIGHTS: list[float] = _build_weights(SAMPLE_LABELS)
