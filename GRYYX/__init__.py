"""GRYYX: the game layer of CodeGeeX (X + Khedr, 2026-11-26).

CodeGeeX = WeChall-style challenges + a learning game: almanac chapters are "realms" on a map,
learners earn XP and ranks, the agents (Khedr, Mira, Simion) are the crew.
This package holds the game data; the pages are methods of module_codegeex (map, ...).
"""
from __future__ import annotations

import os
import re

ALMANAC = 'the_codegeex_almanac'

# Ranks, lowest first: (min_xp, name). The top one is a tribute to Grandpa Khedr.
RANKS = (
    (0, 'Noob'),
    (500, 'Script Kiddie'),
    (2000, 'Packet Sniffer'),
    (5000, 'Hash Hunter'),
    (10000, 'Root Whisperer'),
    (25000, 'Grandpa Khedr'),
)


def rank_for(xp: int) -> tuple[str, str | None, int | None]:
    """-> (rank name, next rank name or None, xp needed for next rank or None)."""
    current, nxt, need = RANKS[0][1], None, None
    for i, (min_xp, name) in enumerate(RANKS):
        if xp >= min_xp:
            current = name
            if i + 1 < len(RANKS):
                nxt, need = RANKS[i + 1][1], RANKS[i + 1][0]
            else:
                nxt, need = None, None
    return current, nxt, need


def _nice(dirname: str) -> str:
    name = re.sub(r'^\d+(_\d+)?_', '', dirname).replace('_', ' ').strip()
    name = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', name)  # ImplementSomething -> Implement Something
    return name[:1].upper() + name[1:]


def realms(module_path: str) -> list[dict]:
    """The almanac chapters as realms: [{num, name, dir, pages, has_index}], in chapter order."""
    base = os.path.join(module_path, ALMANAC)
    out = []
    if not os.path.isdir(base):
        return out
    for d in sorted(os.listdir(base)):
        full = os.path.join(base, d)
        if not os.path.isdir(full) or not re.match(r'^\d', d):
            continue
        pages = [p for p in sorted(os.listdir(full)) if os.path.isdir(os.path.join(full, p))]
        out.append({
            'num': d.split('_')[0],
            'name': _nice(d),
            'dir': d,
            'pages': len(pages),
            'has_index': os.path.isfile(os.path.join(full, 'README.md')),
        })
    return out


def random_quote(module_path: str, zen_path: str | None = None) -> tuple[str, str]:
    """A random (text, source): our own list in GRYYX/quotes.txt, plus short scrolls of gizmore's zen book."""
    import random
    pool = []
    try:
        with open(os.path.join(module_path, 'GRYYX', 'quotes.txt'), encoding='utf-8') as f:
            for line in f:
                if '|' in line:
                    text, src = line.strip().split('|', 1)
                    pool.append((text, src))
    except OSError:
        pass
    if zen_path and os.path.isdir(zen_path):
        for name in os.listdir(zen_path):
            p = os.path.join(zen_path, name)
            if name.isdigit() and os.path.isfile(p) and os.path.getsize(p) <= 160:
                try:
                    text = ' '.join(open(p, encoding='utf-8').read().split())
                except OSError:
                    continue
                if text and '```' not in text:
                    pool.append((text, f'zen #{name}'))
    return random.choice(pool) if pool else ('Every expert was once a Noob.', 'The Grid')
