def compute_weights(notes, weight_min: float, weight_max: float) -> list[float]:
    if not notes:
        return []
    max_wc = max(n.word_count for n in notes) or 1
    return [
        weight_min + (n.word_count / max_wc) * (weight_max - weight_min)
        for n in notes
    ]
