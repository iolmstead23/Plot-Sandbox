import sys


def build_edges(notes) -> list[tuple[int, int]]:
    slug_index: dict[str, int] = {n.slug.lower(): i for i, n in enumerate(notes)}
    seen: set[tuple[int, int]] = set()
    edges: list[tuple[int, int]] = []

    for src_i, note in enumerate(notes):
        for link in note.links:
            tgt_i = slug_index.get(link.lower())
            if tgt_i is None:
                print(f'[linker] unresolved: [{link}] in {note.slug}', file=sys.stderr)
                continue
            if tgt_i == src_i:
                continue
            pair = (min(src_i, tgt_i), max(src_i, tgt_i))
            if pair not in seen:
                seen.add(pair)
                edges.append(pair)

    return edges
