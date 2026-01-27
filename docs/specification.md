# Hivra Network - Core Logic Specification (FINAL)

## §0. Design Principles (Mandatory)

### Strict Modularity
- Any logic implemented through isolated modules
- Adding, changing, or removing mechanics requires no global system edits

### Event-driven Architecture
- System reacts only to events
- No direct connections between modules

### Data Carries No Logic
- Starters, Pulse, invitations and their names have no built-in semantics
- All interpretation performed by handlers

### Toggle-first Logic
- Any event with starter works as a toggle (ON/OFF)

### UI and Core Completely Separated
- UI sends events and displays states
- Core processes events and manages states
- Neither layer knows implementation details of the other

## §1. Basic Entities

### Capsule
Autonomous network participant.

Characteristics:
- Has 5 slots for starters
- Stores local connection states
- Processes incoming events

Types (logical, not privileged):
- Genesis
- Proto  
- Linked

Type grants no rights, used only for describing initial state.

### Starter
Abstract token-switch.

Properties:
- Unique
- Non-fungible
- Contains no logic
- Name has no semantic load

Behavior:
- First event with starter turns state ON
- Repeated event with same starter turns state OFF

### Slot
Local storage place for starter.

States:
- Empty
- Occupied

Slots used exclusively as condition for generation and burn.

## §2. Events

### InviteEvent
Connection offer event.
- Can be sent by any capsule having at least one own starter
- Does not guarantee acceptance

### StarterEvent / PulseEvent
Universal toggle events.
- Have no built-in semantics
- Processed by modules

### UserActionEvent
User-initiated events:
- AcceptInvite
- RejectInvite  
- ToggleState

## §3. Connection States Between Capsules

States exist between capsule pairs and are independent of each other.

Basic states:
- **Invited** - Active invitation exists
- **Trusted** - Trust connection established
- **Linked** - Enhanced logical connection
- **Ignored** - Invitations from capsule ignored locally

All states managed by toggle logic.

## §4. Invitation Processing

### Receiving Invitation
When receiving InviteEvent:
- Invited state toggles ON
- Capsule sees all invitations, including from duplicates

### Accepting Invitation
Condition: Slot empty
- Invited toggles OFF
- New own starter generated
- Trusted or Linked states may activate (by module policies)

Condition: Slot occupied
- Invited toggles OFF
- No starter generation
- Only logical states (trust/link) may activate

Genesis capsules always work by this scenario.

### Rejecting Invitation
Condition: Slot empty
- Invited toggles OFF
- Sender's starter burned
- Ignored state may activate

Condition: Slot occupied
- Invited toggles OFF
- No burn occurs

⚠️ Starter burn only possible with combination:
- Empty slot + explicit RejectInvite action

## §5. Capsule Duplicates

- Duplicates not considered errors
- Proto can receive invitations from other duplicates
- Acceptance creates trust connection, not hierarchy
- Rejection has no side effects except described above

## §6. Starter Generation

Generation only possible when:
- Accepting invitation
- Having empty slot
- No restrictions from policy modules

No other events can lead to generation.

## §7. Burn Policy Module

Starter burn implemented as separate module.

It reacts only to:
- RejectInvite event
- Slot == Empty state

Any other situations ignored.

## §8. Modular Architecture

Each module:
- Subscribes to events
- Stores own state
- Knows nothing about other modules

Adding new logic = adding new module.

Example modules:
- TrustModule
- LinkModule
- BurnPolicyModule
- ReplicationModule

## §9. UI ↔ Core Contract

UI:
- Displays states
- Sends events

Core:
- Processes events
- Manages states

Neither layer knows implementation details of the other.

## §10. Final Model

- Starters - universal switches
- States - ON/OFF combinations
- Invitations - events, not entities
- Trust and growth separated
- System extensible without global edits

Document fixed as FINAL CORE SPEC.
