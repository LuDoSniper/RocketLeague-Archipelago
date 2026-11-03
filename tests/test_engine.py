import json
import unittest
from prototype.engine import Engine, Event

class EngineTests(unittest.TestCase):
    def test_shared_slot_and_isolated_slot(self):
        engine = Engine({"Alice": "Team", "Bob": "Team", "Charlie": "Charlie"})
        self.assertEqual(engine.accept(Event("1", "m1", "Alice", "goal")), [("Team", "first_goal")])
        self.assertEqual(engine.accept(Event("2", "m1", "Bob", "goal")), [])
        self.assertEqual(engine.accept(Event("3", "m1", "Charlie", "goal")), [("Charlie", "first_goal")])
        self.assertEqual(engine.accept(Event("4", "m1", "Alice", "goal")), [("Team", "three_goals")])

    def test_event_idempotence(self):
        engine = Engine({"A": "one"})
        event = Event("id", "match", "A", "save")
        self.assertEqual(engine.accept(event), [("one", "first_save")])
        self.assertEqual(engine.accept(event), [])
        self.assertEqual(engine.counts["one"]["save"], 1)

    def test_match_namespace(self):
        engine = Engine({"A": "one"})
        engine.accept(Event("id", "match1", "A", "goal"))
        engine.accept(Event("id", "match2", "A", "goal"))
        self.assertEqual(engine.counts["one"]["goal"], 2)

    def test_win_variants(self):
        engine = Engine({"A": "one"})
        result = engine.accept(Event("end", "m1", "A", "win", mode="2v2", overtime=True))
        self.assertEqual(set(result), {("one", "first_win"), ("one", "two_v_two_win"), ("one", "overtime_win")})

    def test_round_trip_snapshot(self):
        engine = Engine({"A": "one"})
        engine.accept(Event("1", "m", "A", "goal"))
        restored = Engine.restore(json.loads(json.dumps(engine.snapshot())))
        self.assertEqual(restored.accept(Event("1", "m", "A", "goal")), [])
        self.assertEqual(restored.accept(Event("2", "m", "A", "save")), [("one", "first_save")])

    def test_unknown_participant_does_not_change_state(self):
        engine = Engine({"A": "one"})
        with self.assertRaises(ValueError):
            engine.accept(Event("bad", "m", "B", "goal"))
        self.assertFalse(engine.seen_events)

if __name__ == "__main__":
    unittest.main()
