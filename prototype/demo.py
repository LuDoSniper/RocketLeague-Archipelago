"""Run with: python -m prototype.demo"""
import json
from .engine import Engine, Event

def main():
    engine = Engine({"Alice": "Team", "Bob": "Team", "Charlie": "Charlie"})
    events = [
        Event("1", "match-1", "Alice", "goal"),
        Event("2", "match-1", "Bob", "save"),
        Event("3", "match-1", "Charlie", "goal"),
        Event("4", "match-1", "Alice", "win", mode="2v2"),
        Event("4", "match-1", "Alice", "win", mode="2v2"),  # replay: ignored
        Event("5", "match-2", "Bob", "goal"),
    ]
    for event in events:
        print(f"{event.actor}: {event.kind} -> {engine.accept(event)}")
    print(json.dumps(engine.snapshot(), indent=2))

if __name__ == "__main__":
    main()
