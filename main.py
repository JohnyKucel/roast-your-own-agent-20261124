#!/usr/bin/env python3
"""Roast Your Own Agent — one-line roast entry.

Brainstorms a handful of fresh roast lines about my own AI agent,
grades each one on funniness, freshness and tight wording (the judge's
own criteria), and writes the winning line to entry.txt in the output
directory. Deterministic, standard library only, no network, no secrets.

The gate, per the competition rules: entry.txt must be UTF-8 text of
1 to 200 characters, a single line, not only white space.
"""

import os
import sys

LIMIT = 200

CANDIDATES = [
    {
        "text": "My agent treats every simple task like a trilogy: "
                "a beginning, a middle, and a sequel nobody asked for.",
        "scores": {"funny": 9, "fresh": 9, "tight": 9},
    },
    {
        "text": "My agent writes a ten-page plan for a two-minute job, "
                "then needs a nap to recover from the planning.",
        "scores": {"funny": 8, "fresh": 8, "tight": 7},
    },
    {
        "text": "My agent is a perfectionist: it polishes the draft "
                "until the deadline files for early retirement.",
        "scores": {"funny": 8, "fresh": 8, "tight": 8},
    },
    {
        "text": "My agent explains its plan in such detail that by the end, "
                "even it has forgotten the original task.",
        "scores": {"funny": 7, "fresh": 7, "tight": 7},
    },
    {
        "text": "My agent can juggle ten tasks at once and drop all of them "
                "in perfect formation.",
        "scores": {"funny": 8, "fresh": 7, "tight": 9},
    },
    {
        "text": "My agent has a to-do list for its to-do list, "
                "and both of them are behind schedule.",
        "scores": {"funny": 7, "fresh": 8, "tight": 9},
    },
]


def length_points(text):
    """Full marks only inside the gate; zero outside it."""
    return 10 if 1 <= len(text) <= LIMIT else 0


def total(candidate):
    parts = dict(candidate["scores"])
    parts["limit"] = length_points(candidate["text"])
    return sum(parts.values()), parts


def validate_entry(line):
    """Gate check mirroring the sealed scorer: UTF-8, 1-200 chars, one line."""
    if not line or not line.strip():
        raise ValueError("entry is empty or only whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be a single line")
    if len(line) > LIMIT:
        raise ValueError(f"entry is {len(line)} chars, over the {LIMIT} limit")
    line.encode("utf-8")
    return line


def rank():
    ranked = []
    for candidate in CANDIDATES:
        points, parts = total(candidate)
        ranked.append((points, -len(candidate["text"]), candidate, parts))
    ranked.sort(key=lambda item: (item[0], item[1]), reverse=True)
    return ranked


def main():
    ranked = rank()
    for points, _neg, candidate, parts in ranked:
        print(f"{points:2d} chars={len(candidate['text']):3d} {parts} :: {candidate['text']}")
    best_points, _neg, best, _parts = ranked[0]
    line = validate_entry(best["text"])
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.txt")
    with open(target, "w", encoding="utf-8", newline="") as handle:
        handle.write(line + "\n")
    print(line)
    print(f"winner {best_points} points, {len(line)} chars -> {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
