import re
import zlib
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class NoteRecord:
    slug: str
    label: str
    word_count: int
    links: list[str]
    content_hash: int
    raw: str


_LINK_RE = re.compile(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]')


def parse_note(path: str | Path) -> NoteRecord:
    path = Path(path)
    raw = path.read_text(encoding='utf-8')
    slug = path.stem
    label = slug
    word_count = len(raw.split())
    links = [m.group(1).strip() for m in _LINK_RE.finditer(raw)]
    content_hash = zlib.adler32(path.read_bytes()) & 0xFFFFFFFF
    return NoteRecord(slug=slug, label=label, word_count=word_count,
                      links=links, content_hash=content_hash, raw=raw)
