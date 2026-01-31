# Changelog

## [1.0.0] - 2026-01-31

### Added
- V1 Core Architecture complete
- Ledger-centric design with append-only event log
- Immutable State for deterministic state derivation
- Binary Starter abstraction (ON/OFF switches)
- Genesis and PROTO capsule types
- Complete event system with serialization
- Working CLI with full invitation cycle
- Starter types: ⚡ Juice, 💥 Spark, 🌱 Seed, 📡 Pulse, 🔥 Kick

### Features
- Create Genesis capsules (auto-filled starters)
- Create PROTO capsules (empty slots)
- Send invitations from Genesis to PROTO
- Accept invitations (PROTO receives starters)
- Ledger records all events
- State manages capsule state immutably
- JSON persistence for capsules and ledgers

### Technical Implementation
- Modular architecture without shared mutable state
- Event-driven design
- Dataclass-based event system
- Type-safe Python implementation
- No external dependencies

### Specification Compliance
- 18/26 requirements fully implemented
- Core V1 architecture complete
- Working end-to-end demonstration

### Notes
First stable release of Hivra CapsuleNet V1 architecture.
Ready for further development of invitation mechanics and transport layer.
