"""Tournament statistics — fun awards computed from the match data."""
from __future__ import annotations

from typing import Iterable

from .models import Match, Player
from .tournament import compute_standings


def _match_total_points(m: Match) -> tuple[int, int]:
    """Return (total_points, n_sets) played in a match — counting both players."""
    total = 0
    n_sets = 0
    for s in m.set_scores or []:
        if isinstance(s, (list, tuple)) and len(s) >= 2:
            total += int(s[0]) + int(s[1])
            n_sets += 1
    return total, n_sets


def compute_marathon(players: Iterable[Player], matches: Iterable[Match]) -> list[dict]:
    """Player(s) who played the most points across all their matches."""
    by_id = {p.id: p for p in players}
    points = {pid: 0 for pid in by_id}
    sets_count = {pid: 0 for pid in by_id}
    for m in matches:
        if not m.played:
            continue
        total, n = _match_total_points(m)
        if total == 0:
            continue
        for pid in (m.player1_id, m.player2_id):
            if pid in points:
                points[pid] += total
                sets_count[pid] += n
    if not any(points.values()):
        return []
    best = max(points.values())
    return [
        {"player": by_id[pid], "points": points[pid], "sets": sets_count[pid]}
        for pid in by_id
        if points[pid] == best
    ]


def compute_defender(players: Iterable[Player], matches: Iterable[Match]) -> list[dict]:
    """Player(s) who lost the fewest sets in the tournament."""
    by_id = {p.id: p for p in players}
    lost = {pid: 0 for pid in by_id}
    played_count = {pid: 0 for pid in by_id}
    for m in matches:
        if not m.played:
            continue
        if m.player1_id in lost:
            lost[m.player1_id] += m.score2
            played_count[m.player1_id] += 1
        if m.player2_id in lost:
            lost[m.player2_id] += m.score1
            played_count[m.player2_id] += 1
    active = {pid: lost[pid] for pid in by_id if played_count[pid] > 0}
    if not active:
        return []
    best = min(active.values())
    return [
        {"player": by_id[pid], "sets_lost": active[pid], "played": played_count[pid]}
        for pid in active
        if active[pid] == best
    ]


def compute_troublemaker(players: list[Player], matches: list[Match]) -> list[dict]:
    """Player(s) with the best progression: initial rank (by entry points) → current rank.

    Returns the players whose (initial rank - current rank) is maximal and strictly
    positive — i.e., who climbed the most. Players who didn't move up are excluded.
    """
    initial = sorted(players, key=lambda p: (-p.points, p.name.lower()))
    init_rank = {p.id: i + 1 for i, p in enumerate(initial)}
    standings = compute_standings(players, matches)
    if not standings:
        return []
    final_rank = {s.player.id: i + 1 for i, s in enumerate(standings)}

    by_id = {p.id: p for p in players}
    deltas = []
    for p in players:
        if p.id not in final_rank:
            continue
        delta = init_rank[p.id] - final_rank[p.id]
        deltas.append((p, delta))

    positive = [(p, d) for p, d in deltas if d > 0]
    if not positive:
        return []
    best = max(d for _, d in positive)
    return [
        {
            "player": p,
            "init_rank": init_rank[p.id],
            "final_rank": final_rank[p.id],
            "progression": d,
        }
        for p, d in positive
        if d == best
    ]


def compute_showmen(players: Iterable[Player], matches: Iterable[Match]) -> list[dict]:
    """Match(es) with the highest total of points played (rallies)."""
    by_id = {p.id: p for p in players}
    best_total = 0
    best: list[tuple[Match, int, int]] = []
    for m in matches:
        if not m.played:
            continue
        total, n_sets = _match_total_points(m)
        if total == 0:
            continue
        if total > best_total:
            best_total = total
            best = [(m, total, n_sets)]
        elif total == best_total:
            best.append((m, total, n_sets))
    return [
        {
            "p1": by_id.get(m.player1_id),
            "p2": by_id.get(m.player2_id),
            "points": total,
            "sets": n_sets,
            "score1": m.score1,
            "score2": m.score2,
        }
        for m, total, n_sets in best
    ]


def compute_best_perf(players: Iterable[Player], matches: Iterable[Match]) -> list[dict]:
    """Best upset — the biggest "X beat Y where Y had more entry points" gap."""
    by_id = {p.id: p for p in players}
    best_diff = 0
    best: list[tuple[Player, Player, int]] = []
    for m in matches:
        if not m.played:
            continue
        if m.score1 > m.score2:
            wid, lid = m.player1_id, m.player2_id
        elif m.score2 > m.score1:
            wid, lid = m.player2_id, m.player1_id
        else:
            continue
        w = by_id.get(wid)
        l = by_id.get(lid)
        if w is None or l is None:
            continue
        diff = l.points - w.points
        if diff <= 0:
            continue
        if diff > best_diff:
            best_diff = diff
            best = [(w, l, diff)]
        elif diff == best_diff:
            best.append((w, l, diff))
    return [
        {"winner": w, "loser": l, "diff": diff}
        for w, l, diff in best
    ]
