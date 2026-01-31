#!/usr/bin/env python3
"""
Hivra CapsuleNet CLI - Command line interface for capsule management.
"""
import argparse
import json
import sys
from pathlib import Path
from typing import Optional

from src.core.capsule import Capsule, CapsuleType
from src.core.ledger import Ledger
from src.core.state import State
from src.events.base import Event
from src.events.invitation import InvitationEvent
from src.modules.invitation import InvitationModule
from src.modules.trust import TrustModule
from src.coordinator.event_bus import EventBus


class CapsuleCLI:
    """Command line interface for capsule operations."""
    
    def __init__(self, data_dir: Path = Path.home() / ".capsulenet"):
        self.data_dir = data_dir
        self.data_dir.mkdir(exist_ok=True)
        self.event_bus = EventBus()
        
        # Register modules
        self.invitation_module = InvitationModule(self.event_bus)
        self.trust_module = TrustModule(self.event_bus)
        
        self.capsule: Optional[Capsule] = None
        self.ledger: Optional[Ledger] = None
        self.state: Optional[State] = None
    
    def create_capsule(self, capsule_type: str, capsule_id: str) -> None:
        """Create a new capsule."""
        try:
            caps_type = CapsuleType(capsule_type.lower())
        except ValueError:
            print(f"Error: Invalid capsule type. Use 'genesis' or 'proto'")
            return
        
        # Create capsule
        self.capsule = Capsule(
            capsule_id=capsule_id,
            capsule_type=caps_type
        )
        
        # Create ledger
        self.ledger = Ledger(capsule_id)
        
        # Create initial state
        self.state = State(capsule_id, caps_type)
        
        # Save to file
        self._save_capsule()
        
        print(f"✓ Created {caps_type.value.upper()} capsule: {capsule_id}")
        print(f"  Data directory: {self.data_dir}")
    
    def load_capsule(self, capsule_id: str) -> bool:
        """Load existing capsule."""
        capsule_file = self.data_dir / f"{capsule_id}_capsule.json"
        ledger_file = self.data_dir / f"{capsule_id}_ledger.json"
        state_file = self.data_dir / f"{capsule_id}_state.json"
        
        try:
            # Load capsule
            if capsule_file.exists():
                with open(capsule_file, 'r') as f:
                    data = json.load(f)
                self.capsule = Capsule.from_dict(data)
            else:
                print(f"Error: Capsule file not found: {capsule_file}")
                return False
            
            # Load ledger
            if ledger_file.exists():
                self.ledger = Ledger.load_from_file(str(ledger_file))
            else:
                self.ledger = Ledger(capsule_id)
            
            # Load or create state
            if state_file.exists():
                with open(state_file, 'r') as f:
                    data = json.load(f)
                self.state = State.from_dict(data)
            else:
                # Recreate state from ledger
                self.state = State(capsule_id, self.capsule.capsule_type)
                # TODO: Replay ledger events to rebuild state
                print("Note: State file not found, created empty state")
            
            return True
            
        except Exception as e:
            print(f"Error loading capsule: {e}")
            return False
    
    def _save_capsule(self) -> None:
        """Save capsule data to files."""
        if not self.capsule or not self.ledger:
            return
        
        capsule_id = self.capsule.capsule_id
        
        # Save capsule
        capsule_file = self.data_dir / f"{capsule_id}_capsule.json"
        with open(capsule_file, 'w') as f:
            json.dump(self.capsule.to_dict(), f, indent=2)
        
        # Save ledger
        ledger_file = self.data_dir / f"{capsule_id}_ledger.json"
        self.ledger.save_to_file(str(ledger_file))
        
        # Save state
        if self.state:
            state_file = self.data_dir / f"{capsule_id}_state.json"
            with open(state_file, 'w') as f:
                json.dump(self.state.to_dict(), f, indent=2)
    
    def show_status(self) -> None:
        """Show capsule status."""
        if not self.capsule or not self.state:
            print("No capsule loaded")
            return
        
        print(f"\nCapsule: {self.capsule.capsule_id}")
        print(f"Type: {self.capsule.capsule_type.value.upper()}")
        print(f"State sequence: {self.state._sequence}")
        
        # Show slots
        print("\nSlots:")
        for slot_type, slot in self.capsule.slots.items():
            starter_id = slot.starter_id
            status = "EMPTY" if not starter_id else "OCCUPIED"
            print(f"  {slot_type:15} - {status:10}", end="")
            if starter_id:
                print(f" (starter: {starter_id[:8]}...)")
            else:
                print()
        
        # Show connections
        if self.capsule.connections:
            print(f"\nConnections: {len(self.capsule.connections)}")
            for conn_id in list(self.capsule.connections)[:5]:  # Show first 5
                print(f"  {conn_id[:8]}...")
            if len(self.capsule.connections) > 5:
                print(f"  ... and {len(self.capsule.connections) - 5} more")
        else:
            print("\nConnections: None")
        
        # Show ledger stats
        if self.ledger:
            print(f"\nLedger entries: {len(self.ledger.entries)}")
            if self.ledger.entries:
                last_entry = self.ledger.get_last_entry()
                print(f"Last event: {last_entry.event.event_type}")
    
    def list_capsules(self) -> None:
        """List all capsules in data directory."""
        print(f"\nCapsules in {self.data_dir}:")
        found = False
        
        for file in self.data_dir.glob("*_capsule.json"):
            capsule_id = file.name.replace("_capsule.json", "")
            try:
                with open(file, 'r') as f:
                    data = json.load(f)
                caps_type = data.get("capsule_type", "unknown")
                print(f"  {capsule_id:30} - {caps_type.upper():10}")
                found = True
            except:
                print(f"  {capsule_id:30} - ERROR reading")
        
        if not found:
            print("  No capsules found")
    
    def send_invitation(self, recipient_id: str, slot_type: str) -> None:
        """Send invitation to another capsule."""
        if not self.capsule or not self.ledger:
            print("Error: No capsule loaded")
            return
        
        # Check if slot exists
        slot = self.capsule.get_slot(slot_type)
        if not slot:
            print(f"Error: Slot type '{slot_type}' not found")
            return
        
        # Check if slot has starter
        if not slot.starter_id:
            print(f"Error: Slot '{slot_type}' is empty (no starter)")
            return
        
        # Create invitation event
        event = InvitationEvent(
            invitation_id=f"inv_{self.capsule.capsule_id[:8]}_{recipient_id[:8]}",
            sender_id=self.capsule.capsule_id,
            recipient_id=recipient_id,
            starter_id=slot.starter_id,
            capsule_id=self.capsule.capsule_id,
            slot_type=slot_type
        )
        
        # Append to ledger
        entry = self.ledger.append(event, tags=["invitation", "outgoing"])
        
        print(f"✓ Invitation sent to {recipient_id}")
        print(f"  Starter: {slot.starter_id[:8]}...")
        print(f"  Event ID: {entry.id[:8]}...")
        
        self._save_capsule()
    
    def show_ledger(self, limit: int = 10, tags: Optional[list] = None) -> None:
        """Show ledger entries."""
        if not self.ledger:
            print("Error: No ledger loaded")
            return
        
        entries = self.ledger.get_entries(tags)
        
        print(f"\nLedger entries (showing {min(limit, len(entries))} of {len(entries)}):")
        print("-" * 80)
        
        for i, entry in enumerate(entries[:limit]):
            print(f"{entry.sequence_number:4} | {entry.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"     | Event: {entry.event.event_type:15} | ID: {entry.id[:8]}...")
            print(f"     | Tags: {', '.join(entry.tags) if entry.tags else 'None'}")
            
            # Show event-specific data
            if hasattr(entry.event, 'sender_id'):
                print(f"     | From: {entry.event.sender_id[:8]}...")
            if hasattr(entry.event, 'recipient_id'):
                print(f"     | To: {entry.event.recipient_id[:8]}...")
            if hasattr(entry.event, 'starter_id'):
                print(f"     | Starter: {entry.event.starter_id[:8]}...")
            
            print()
    
    def replay_ledger(self) -> None:
        """Replay ledger to rebuild state (for debugging)."""
        if not self.ledger or not self.state:
            print("Error: No ledger or state loaded")
            return
        
        print(f"Replaying {len(self.ledger.entries)} events...")
        
        # Reset state
        self.state = State(self.capsule.capsule_id, self.capsule.capsule_type)
        
        # Replay each event
        for entry in self.ledger.entries:
            new_state = self.state.apply_event(entry.event)
            self.state = new_state
        
        print(f"✓ State rebuilt. Sequence: {self.state._sequence}")
        self._save_capsule()


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Hivra CapsuleNet - Distributed capsule management system",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s create genesis my-capsule-001
  %(prog)s load my-capsule-001
  %(prog)s status
  %(prog)s send friend@capsule friendship
  %(prog)s ledger --limit 5
  %(prog)s list
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Create capsule command
    create_parser = subparsers.add_parser("create", help="Create a new capsule")
    create_parser.add_argument("type", choices=["genesis", "proto"], help="Capsule type")
    create_parser.add_argument("id", help="Capsule ID")
    
    # Load capsule command
    load_parser = subparsers.add_parser("load", help="Load existing capsule")
    load_parser.add_argument("id", help="Capsule ID")
    
    # Status command
    status_parser = subparsers.add_parser("status", help="Show capsule status")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List all capsules")
    
    # Send invitation command
    send_parser = subparsers.add_parser("send", help="Send invitation")
    send_parser.add_argument("recipient", help="Recipient capsule ID")
    send_parser.add_argument("slot_type", help="Slot type (friendship, collaboration, etc.)")
    
    # Ledger command
    ledger_parser = subparsers.add_parser("ledger", help="Show ledger entries")
    ledger_parser.add_argument("--limit", type=int, default=10, help="Number of entries to show")
    ledger_parser.add_argument("--tags", help="Filter by tags (comma-separated)")
    
    # Replay command
    replay_parser = subparsers.add_parser("replay", help="Replay ledger to rebuild state")
    
    # Parse arguments
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Initialize CLI
    cli = CapsuleCLI()
    
    # Execute command
    try:
        if args.command == "create":
            cli.create_capsule(args.type, args.id)
        elif args.command == "load":
            if cli.load_capsule(args.id):
                print(f"✓ Capsule loaded: {args.id}")
                cli.show_status()
            else:
                sys.exit(1)
        elif args.command == "status":
            if not cli.capsule:
                print("Error: No capsule loaded. Use 'load <id>' first")
                sys.exit(1)
            cli.show_status()
        elif args.command == "list":
            cli.list_capsules()
        elif args.command == "send":
            if not cli.capsule:
                print("Error: No capsule loaded. Use 'load <id>' first")
                sys.exit(1)
            cli.send_invitation(args.recipient, args.slot_type)
        elif args.command == "ledger":
            if not cli.capsule:
                print("Error: No capsule loaded. Use 'load <id>' first")
                sys.exit(1)
            tags = args.tags.split(",") if args.tags else None
            cli.show_ledger(args.limit, tags)
        elif args.command == "replay":
            if not cli.capsule:
                print("Error: No capsule loaded. Use 'load <id>' first")
                sys.exit(1)
            cli.replay_ledger()
    
    except KeyboardInterrupt:
        print("\nOperation cancelled")
        sys.exit(130)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
