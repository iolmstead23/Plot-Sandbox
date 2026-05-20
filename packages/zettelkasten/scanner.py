import sys
from pathlib import Path
from .parser import NoteRecord, parse_note


def scan_directory(root: str | Path) -> list[NoteRecord]:
    root = Path(root)
    records: list[NoteRecord] = []
    for path in sorted(root.rglob('*.md'), key=lambda p: p.stem):
        try:
            records.append(parse_note(path))
        except Exception as exc:
            print(f'[zettelkasten] skip {path.name}: {exc}', file=sys.stderr)
    return records
