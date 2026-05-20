from __future__ import annotations

import collections
from typing import Iterable

import numpy as np


def bfs_landmark_layout(
    n: int,
    edges: Iterable[tuple[int, int]],
    *,
    dims: int = 3,
    view_range: float = 10.0,
    n_landmarks: int = 3,
    rng: np.random.Generator,
    focus: np.ndarray | None = None,
) -> np.ndarray:
    """Place n nodes using BFS hop-distances from k landmark vertices.

    Landmark selection spreads landmarks across the graph by greedily picking
    the node farthest from all existing landmarks. Falls back to random uniform
    positions if the graph has no edges or n < 2.
    """
    if n == 0:
        return np.zeros((0, dims), dtype=np.float64)

    focus_d = np.zeros(dims, dtype=np.float64)
    if focus is not None:
        f = np.asarray(focus, dtype=np.float64).reshape(-1)
        copy_n = min(f.shape[0], dims)
        focus_d[:copy_n] = f[:copy_n]

    # Build adjacency list.
    adj: list[list[int]] = [[] for _ in range(n)]
    edge_count = 0
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
        edge_count += 1

    if n < 2 or edge_count == 0:
        # No topology to exploit — scatter randomly.
        raw = rng.standard_normal((n, dims))
        norms = np.linalg.norm(raw, axis=1, keepdims=True)
        norms = np.where(norms > 0.0, norms, 1.0)
        return focus_d[None, :] + (raw / norms) * (view_range * 0.5)

    k = min(n_landmarks, dims, n)
    INF = n + 1  # sentinel for unreachable nodes

    def _bfs(source: int) -> list[int]:
        dist = [INF] * n
        dist[source] = 0
        q: collections.deque[int] = collections.deque([source])
        while q:
            u = q.popleft()
            for v in adj[u]:
                if dist[v] == INF:
                    dist[v] = dist[u] + 1
                    q.append(v)
        return dist

    # Select first landmark randomly; subsequent landmarks maximize min-distance
    # to any existing landmark (farthest-first / gonzalez spread).
    landmarks: list[int] = [int(rng.integers(0, n))]
    min_dists = np.array(_bfs(landmarks[0]), dtype=np.float64)

    for _ in range(k - 1):
        next_lm = int(np.argmax(min_dists))
        landmarks.append(next_lm)
        new_d = np.array(_bfs(next_lm), dtype=np.float64)
        min_dists = np.minimum(min_dists, new_d)

    # Build (n, k) distance matrix, one column per landmark BFS.
    dist_matrix = np.empty((n, k), dtype=np.float64)
    for col, lm in enumerate(landmarks):
        d = _bfs(lm)
        dist_matrix[:, col] = d

    # Center and scale each dimension so max abs value = view_range * 0.8.
    for col in range(k):
        col_data = dist_matrix[:, col]
        col_data -= col_data.mean()
        peak = np.abs(col_data).max()
        if peak > 0.0:
            col_data *= (view_range * 0.8) / peak
        dist_matrix[:, col] = col_data

    # Pad remaining dimensions with small noise when dims > k.
    if dims > k:
        pad = rng.standard_normal((n, dims - k)) * (view_range * 0.05)
        positions = np.concatenate([dist_matrix, pad], axis=1)
    else:
        positions = dist_matrix[:, :dims]

    return focus_d[None, :] + positions
