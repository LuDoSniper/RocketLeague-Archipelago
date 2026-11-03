# Rocket League Archipelago

Experimental Archipelago integration for **Rocket League LAN**. This is a **prototype**, not a working Rocket League mod yet.

## Current scope (v0.1.0 prototype)

- Offline event-to-check simulation for **shared**, **individual**, and **hybrid** slot ownership.
- Persistent, deduplicated checks by Archipelago slot.
- A minimal experimental `.apworld` with 12 check locations, progression items, and a goal.
- Automated unit tests and GitHub Actions validation.

**Not implemented:** Rocket League event capture, real LAN gameplay hooking, in-game capability restrictions, a production Archipelago network client, or a verified installation against the current game version. No anti-cheat bypass is attempted.

## Quick start (Windows, Python 3.11+)

```powershell
git clone https://github.com/LuDoSniper/RocketLeague-Archipelago.git
cd RocketLeague-Archipelago
python -m unittest discover -s tests -v
python -m prototype.demo
```

See [docs/TESTING.md](docs/TESTING.md) for the exact first test, sample events, and limitations.

## Design

A Rocket League *participant* is linked to an Archipelago *slot*. Several participants may share a slot; distinct slots can be present in the same LAN match. Only validated events attributed to a participant can unlock their slot's checks. The simulation deliberately keeps this distinction separate from the matchmaking/LAN transport.

The world package is in `rocket_league/`; see the packaging guidance in the testing instructions. Archipelago versions differ: generation must be tested against the version of Archipelago used by ArchiLAN before we consider the `.apworld` stable.

## Safety and limitations

Use only allowed offline/LAN modding paths with EAC disabled, following game/platform rules. This project does not attempt to modify anti-cheat, online matchmaking, or official competitive games.

## License

No license selected yet. The repository owner should choose one before accepting external contributions.
