"""Shared compute helpers for handler modules.

Bridges plain-tuple element records (owned by state) to spatial.Element instances
(needed by spatial formulas), then back to plain (label, x, y, z) tuples (consumed
by plot). Lives in the orchestration layer, not in any package.
"""

from packages.spatial import Element


def records_to_elements(records: list[tuple[str, float, int, int]]) -> list[Element]:
    return [Element(*rec) for rec in records]


def points_from_formula(records, formula):
    """records -> Elements -> apply formula -> [(label, x, y, z), ...]"""
    elements = records_to_elements(records)
    return [(e.label, c.x, c.y, c.z) for e in elements for c in (formula(e),)]
