# First prototype test

## Prerequisites

- Windows 10/11, Linux or macOS
- Python 3.11+ (no third-party dependencies for the simulation)

## Test 1 — automated

From a cloned repository:

```powershell
python -m unittest discover -s tests -v
```

Expected: **6 tests pass**. The tests verify shared slots, isolated slots, duplicate-event rejection, stable match IDs, victory check attribution and persistence of a snapshot.

## Test 2 — simulated LAN events

```powershell
python -m prototype.demo
```

Expected: Alice and Bob share the `Team` slot; Charlie has his own slot. A replayed win event causes no new check. The output ends in JSON listing counters and validated checks.

## Test 3 — world package (experimental)

The `rocket_league` Python package is intended as a first Archipelago world implementation. After installing a compatible Archipelago development environment, package it as a ZIP containing the `rocket_league/` directory, then rename the ZIP to `rocket_league.apworld`. Archipelago world APIs vary across versions, and this package has **not** been generation-tested in this environment. Do not deploy it to ArchiLAN without a generation test. The check engine test does not prove the `.apworld` is loadable.

## Not testable yet

There is **no** game injector, BakkesMod plugin, LAN adapter, playable overlay, or real Archipelago network client in this milestone. Running Rocket League will not show or apply the mod. Modding the game requires a separate compatibility investigation with EAC disabled and permitted LAN environments.

## Feedback requested

Send the terminal output of both commands (tests and demo), your Rocket League client version and whether you have a LAN hosting solution that successfully starts a match on two computers. Never disable or bypass protections for online matchmaking.
