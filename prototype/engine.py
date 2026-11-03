"""Deterministic, transport-independent Rocket League check engine."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Iterable

CHECKS = {
    "first_goal": "First Goal",
    "three_goals": "Three Career Goals",
    "first_save": "First Save",
    "three_saves": "Three Career Saves",
    "first_assist": "First Assist",
    "first_win": "First Win",
    "two_wins": "Two Career Wins",
    "overtime_win": "Overtime Winner",
    "two_v_two_win": "2v2 Victory",
    "three_v_three_win": "3v3 Victory",
    "five_goals": "Five Career Goals",
    "championship": "Champion",
}
THRESHOLDS = {
    "goal": [(1, "first_goal"), (3, "three_goals"), (5, "five_goals")],
    "save": [(1, "first_save"), (3, "three_saves")],
    "assist": [(1, "first_assist")],
    "win": [(1, "first_win"), (2, "two_wins")],
}

@dataclass(frozen=True)
class Event:
    event_id: str
    match_id: str
    actor: str
    kind: str
    mode: str = "1v1"
    overtime: bool = False

@dataclass
class Engine:
    """Events must be supplied by a trusted match authority in production.

    Slot ownership is immutable for a run. Deduplication uses stable IDs.
    """
    membership: dict[str, str]
    seen_events: set[str] = field(default_factory=set)
    counts: dict[str, dict[str, int]] = field(default_factory=dict)
    completed: dict[str, set[str]] = field(default_factory=dict)

    def accept(self, event: Event) -> list[tuple[str, str]]:
        if not event.event_id or not event.match_id:
            raise ValueError("event_id and match_id are required")
        if event.actor not in self.membership:
            raise ValueError("unknown participant")
        if event.kind not in THRESHOLDS:
            raise ValueError("unknown event kind")
        # Namespaced by match: reusing an ID in another match is safe.
        key = f"{event.match_id}:{event.event_id}"
        if key in self.seen_events:
            return []
        self.seen_events.add(key)
        slot = self.membership[event.actor]
        counter = self.counts.setdefault(slot, {})
        counter[event.kind] = counter.get(event.kind, 0) + 1
        possible = [name for threshold, name in THRESHOLDS[event.kind]
                    if counter[event.kind] >= threshold]
        if event.kind == "win":
            if event.overtime:
                possible.append("overtime_win")
            if event.mode == "2v2":
                possible.append("two_v_two_win")
            if event.mode == "3v3":
                possible.append("three_v_three_win")
        done = self.completed.setdefault(slot, set())
        newly_completed = sorted(set(possible) - done)
        done.update(newly_completed)
        return [(slot, check) for check in newly_completed]

    def snapshot(self) -> dict:
        return {
            "membership": dict(self.membership),
            "seen_events": sorted(self.seen_events),
            "counts": {k: dict(v) for k, v in self.counts.items()},
            "completed": {k: sorted(v) for k, v in self.completed.items()},
        }

    @classmethod
    def restore(cls, snapshot: dict) -> Engine:
        return cls(
            membership=dict(snapshot["membership"]),
            seen_events=set(snapshot["seen_events"]),
            counts={k: dict(v) for k, v in snapshot["counts"].items()},
            completed={k: set(v) for k, v in snapshot["completed"].items()},
        )
