#!/usr/bin/env python3
"""
Hivra CapsuleNet CLI - Stateful version.
"""
import argparse
import json
import sys
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime

from src.core.capsule import Capsule, CapsuleType
from src.core.ledger import Ledger
from src.core.state import State
from src.events import Event, create_invitation_event


class CapsuleManager:
    """Manages capsules with state persistence."""
    
    def __init__(self, data_dir: Path = Path.home() / ".capsulenet"):
        self.data_dir = data_dir
        self.data_dir.mkdir(exist_ok=True)
        self._invitations_file = data_dir / "invitations.json"
        self._state_file = data_dir / "cli_state.json"
        self._current_capsule: Optional[str] = None
    
    def get_current_capsule_id(self) -> Optional[str]:
        """Get currently loaded capsule ID."""
        if self._state_file.exists():
            try:
                with open(self._state_file, 'r') as f:
                    state = json.load(f)
                return state.get('current_capsule')
            except:
                pass
        return None
    
    def set_current_capsule(self, capsule_id: str) -> None:
        """Set current capsule."""
        state = {'current_capsule': capsule_id}
        with open(self._state_file, 'w') as f:
            json.dump(state, f, indent=2)
    
    def clear_current_capsule(self) -> None:
        """Clear current capsule."""
        if self._state_file.exists():
            self._state_file.unlink()
    
    def load_capsule(self, capsule_id: str) -> Optional[Dict]:
        """Load capsule data."""
        capsule_file = self.data_dir / f"{capsule_id}_capsule.json"
        if not capsule_file.exists():
            return None
        
        try:
            with open(capsule_file, 'r') as f:
                data = json.load(f)
            return data
        except:
            return None
    
    def save_capsule(self, capsule_id: str, data: Dict) -> None:
        """Save capsule data."""
        capsule_file = self.data_dir / f"{capsule_id}_capsule.json"
        with open(capsule_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_ledger(self, capsule_id: str) -> Ledger:
        """Load or create ledger."""
        ledger_file = self.data_dir / f"{capsule_id}_ledger.json"
        if ledger_file.exists():
            return Ledger.load_from_file(str(ledger_file))
        return Ledger(capsule_id)
    
    def save_ledger(self, capsule_id: str, ledger: Ledger) -> None:
        """Save ledger."""
        ledger_file = self.data_dir / f"{capsule_id}_ledger.json"
        ledger.save_to_file(str(ledger_file))
    
    def load_invitations(self) -> List[Dict]:
        """Load invitations."""
        if not self._invitations_file.exists():
            return []
        try:
            with open(self._invitations_file, 'r') as f:
                return json.load(f)
        except:
            return []
    
    def save_invitations(self, invitations: List[Dict]) -> None:
        """Save invitations."""
        with open(self._invitations_file, 'w') as f:
            json.dump(invitations, f, indent=2)
    
    def list_capsules(self) -> List[Dict]:
        """List all capsules."""
        capsules = []
        for file in self.data_dir.glob("*_capsule.json"):
            caps_id = file.name.replace("_capsule.json", "")
            try:
                with open(file, 'r') as f:
                    data = json.load(f)
                caps_type = data.get("capsule_type", "unknown").upper()
                
                slots = data.get("slots", {})
                starter_count = sum(1 for s in slots.values() if s.get("starter_id"))
                total_slots = len(slots)
                
                capsules.append({
                    'id': caps_id,
                    'type': caps_type,
                    'starters': f"{starter_count}/{total_slots}",
                    'is_genesis': caps_type == "GENESIS"
                })
            except:
                capsules.append({
                    'id': caps_id,
                    'type': "ERROR",
                    'starters': "?/?",
                    'is_genesis': False
                })
        return capsules


def create_capsule(capsule_type: str, capsule_id: str, manager: CapsuleManager) -> None:
    """Create new capsule."""
    try:
        caps_type = CapsuleType(capsule_type.lower())
    except ValueError:
        print(f"Error: Use 'genesis' or 'proto'")
        return
    
    capsule = Capsule(capsule_id=capsule_id, capsule_type=caps_type)
    manager.save_capsule(capsule_id, capsule.to_dict())
    manager.set_current_capsule(capsule_id)
    
    # Create empty ledger
    ledger = Ledger(capsule_id)
    manager.save_ledger(capsule_id, ledger)
    
    print(f"✓ Created {capsule_type.upper()} capsule: {capsule_id}")
    if caps_type == CapsuleType.GENESIS:
        print(f"  🎉 All 5 starters created automatically")
    else:
        print(f"  ⏳ Empty slots - needs invitation to get starters")


def load_capsule(capsule_id: str, manager: CapsuleManager) -> bool:
    """Load capsule as current."""
    if not manager.load_capsule(capsule_id):
        print(f"Error: Capsule '{capsule_id}' not found")
        return False
    
    manager.set_current_capsule(capsule_id)
    print(f"✓ Loaded capsule: {capsule_id}")
    show_status(capsule_id, manager)
    return True


def show_status(capsule_id: str, manager: CapsuleManager) -> None:
    """Show capsule status."""
    data = manager.load_capsule(capsule_id)
    if not data:
        print(f"Error: Capsule '{capsule_id}' not found")
        return
    
    capsule = Capsule.from_dict(data)
    ledger = manager.load_ledger(capsule_id)
    invitations = manager.load_invitations()
    my_invitations = [inv for inv in invitations if inv['recipient'] == capsule_id]
    
    print(f"\n{'='*50}")
    print(f"CAPSULE: {capsule_id}")
    print(f"TYPE: {capsule.capsule_type.value.upper()}")
    print(f"{'='*50}")
    
    print("\n🧪 STARTER SLOTS:")
    for slot_name, slot in capsule.slots.items():
        if slot.starter_id:
            print(f"  {slot_name:15} ✅ OCCUPIED")
        else:
            print(f"  {slot_name:15} ⭕ EMPTY")
    
    if my_invitations:
        print(f"\n📥 PENDING INVITATIONS: {len(my_invitations)}")
        for inv in my_invitations[:3]:
            print(f"  From: {inv['sender']}, Slot: {inv['slot']}")
        if len(my_invitations) > 3:
            print(f"  ... and {len(my_invitations) - 3} more")
    
    print(f"\n📊 Ledger events: {len(ledger.entries)}")
    
    if capsule.capsule_type == CapsuleType.GENESIS:
        print(f"\n💡 This GENESIS capsule can send invitations")
        print(f"   Command: cli.py invite <recipient> <slot>")
    else:
        print(f"\n💡 This PROTO capsule can accept invitations")
        print(f"   Command: cli.py accept <invitation-id>")


def list_capsules(manager: CapsuleManager) -> None:
    """List all capsules."""
    capsules = manager.list_capsules()
    
    if not capsules:
        print("No capsules found")
        return
    
    print(f"\n📦 CAPSULES:")
    print("-" * 40)
    
    # Sort: genesis first
    capsules.sort(key=lambda x: (not x['is_genesis'], x['id']))
    
    for caps in capsules:
        type_icon = "👑" if caps['is_genesis'] else "🆕"
        print(f"  {type_icon} {caps['id']:20} - {caps['type']:8} [{caps['starters']} starters]")
    
    current = manager.get_current_capsule_id()
    if current:
        print(f"\n💡 Current capsule: {current}")
    print(f"💡 Load capsule: cli.py load <id>")


def send_invitation(sender_id: str, recipient_id: str, slot_name: str, manager: CapsuleManager) -> None:
    """Send invitation from Genesis to Proto."""
    sender_data = manager.load_capsule(sender_id)
    if not sender_data:
        print(f"Error: Sender capsule '{sender_id}' not found")
        return
    
    sender = Capsule.from_dict(sender_data)
    if sender.capsule_type != CapsuleType.GENESIS:
        print(f"Error: Only GENESIS capsules can send invitations")
        return
    
    recipient_data = manager.load_capsule(recipient_id)
    if not recipient_data:
        print(f"Error: Recipient capsule '{recipient_id}' not found")
        print(f"  Create it first: cli.py create proto {recipient_id}")
        return
    
    recipient = Capsule.from_dict(recipient_data)
    if recipient.capsule_type != CapsuleType.PROTO:
        print(f"Error: Recipient must be a PROTO capsule")
        return
    
    slot = sender.get_slot(slot_name)
    if not slot:
        print(f"Error: Slot '{slot_name}' not found")
        print(f"  Available: {', '.join(sender.slots.keys())}")
        return
    
    if not slot.starter_id:
        print(f"Error: Slot '{slot_name}' is empty")
        return
    
    # Create invitation
    invitation_id = f"inv_{sender_id}_{recipient_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    invitation = {
        'id': invitation_id,
        'sender': sender_id,
        'recipient': recipient_id,
        'slot': slot_name,
        'starter_id': slot.starter_id,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Save invitation
    invitations = manager.load_invitations()
    invitations.append(invitation)
    manager.save_invitations(invitations)
    
    # Record in sender's ledger
    ledger = manager.load_ledger(sender_id)
    event = create_invitation_event(
        invitation_id=invitation_id,
        sender_id=sender_id,
        recipient_id=recipient_id,
        starter_id=slot.starter_id,
        capsule_id=sender_id,
        slot_type=slot_name
    )
    ledger.append(event, tags=["invitation", "outgoing"])
    manager.save_ledger(sender_id, ledger)
    
    print(f"\n📤 INVITATION SENT:")
    print(f"  From: {sender_id} (GENESIS)")
    print(f"  To: {recipient_id} (PROTO)")
    print(f"  Starter: {slot_name}")
    print(f"  Invitation ID: {invitation_id}")
    print(f"\n💡 {recipient_id} can accept with:")
    print(f"    cli.py accept {invitation_id}")


def accept_invitation(capsule_id: str, invitation_id: str, manager: CapsuleManager) -> None:
    """Accept invitation (Proto only)."""
    capsule_data = manager.load_capsule(capsule_id)
    if not capsule_data:
        print(f"Error: Capsule '{capsule_id}' not found")
        return
    
    capsule = Capsule.from_dict(capsule_data)
    if capsule.capsule_type != CapsuleType.PROTO:
        print(f"Error: Only PROTO capsules can accept invitations")
        return
    
    invitations = manager.load_invitations()
    invitation = next((inv for inv in invitations if inv['id'] == invitation_id), None)
    
    if not invitation:
        print(f"Error: Invitation '{invitation_id}' not found")
        return
    
    if invitation['recipient'] != capsule_id:
        print(f"Error: Invitation is for {invitation['recipient']}, not {capsule_id}")
        return
    
    slot_name = invitation['slot']
    slot = capsule.get_slot(slot_name)
    if not slot:
        print(f"Error: Slot '{slot_name}' not found")
        return
    
    if slot.starter_id:
        print(f"Error: Slot '{slot_name}' is already occupied")
        return
    
    # Accept invitation
    slot.starter_id = invitation['starter_id']
    
    # Save updated capsule
    manager.save_capsule(capsule_id, capsule.to_dict())
    
    # Record in ledger
    ledger = manager.load_ledger(capsule_id)
    event = Event(event_type="invitation_accepted")
    event.metadata.update({
        "invitation_id": invitation_id,
        "sender": invitation['sender'],
        "slot": slot_name,
        "new_starter_id": slot.starter_id
    })
    ledger.append(event, tags=["invitation", "accepted"])
    manager.save_ledger(capsule_id, ledger)
    
    # Remove invitation
    invitations = [inv for inv in invitations if inv['id'] != invitation_id]
    manager.save_invitations(invitations)
    
    print(f"\n✅ INVITATION ACCEPTED:")
    print(f"  By: {capsule_id} (PROTO)")
    print(f"  From: {invitation['sender']} (GENESIS)")
    print(f"  Starter: {slot_name}")
    print(f"  Starter ID: {slot.starter_id[:12]}...")
    print(f"\n🎉 {capsule_id} now has {slot_name} starter!")


def show_invitations(capsule_id: str, manager: CapsuleManager) -> None:
    """Show pending invitations for capsule."""
    invitations = manager.load_invitations()
    my_invitations = [inv for inv in invitations if inv['recipient'] == capsule_id]
    
    if not my_invitations:
        print(f"\n📭 No pending invitations for {capsule_id}")
        return
    
    print(f"\n📥 PENDING INVITATIONS for {capsule_id}:")
    print("-" * 50)
    
    for i, inv in enumerate(my_invitations, 1):
        print(f"\n{i}. ID: {inv['id']}")
        print(f"   From: {inv['sender']}")
        print(f"   Starter: {inv['slot']}")
        print(f"   Sent: {inv['timestamp']}")
        print(f"   Accept: cli.py accept {inv['id']}")


def main():
    parser = argparse.ArgumentParser(
        description="Hivra CapsuleNet V1 - Genesis sends, Proto receives",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create capsules
  %(prog)s create genesis alice
  %(prog)s create proto bob
  
  # List capsules
  %(prog)s list
  
  # Load capsule (sets as current)
  %(prog)s load alice
  
  # Send invitation (Genesis only)
  %(prog)s invite bob "⚡ Juice"
  
  # Show/accept invitations (Proto only)
  %(prog)s load bob
  %(prog)s invitations
  %(prog)s accept <invitation-id>
  
  # Show current capsule status
  %(prog)s status
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command")
    
    # Create
    create_p = subparsers.add_parser("create", help="Create capsule")
    create_p.add_argument("type", choices=["genesis", "proto"])
    create_p.add_argument("id", help="Capsule ID")
    
    # Load
    load_p = subparsers.add_parser("load", help="Load capsule as current")
    load_p.add_argument("id", help="Capsule ID")
    
    # Status
    status_p = subparsers.add_parser("status", help="Show current capsule status")
    status_p.add_argument("id", nargs="?", help="Capsule ID (optional)")
    
    # List
    subparsers.add_parser("list", help="List all capsules")
    
    # Invite
    invite_p = subparsers.add_parser("invite", help="Send invitation")
    invite_p.add_argument("recipient", help="Recipient capsule ID")
    invite_p.add_argument("slot", help='Slot type, e.g., "⚡ Juice"')
    
    # Accept
    accept_p = subparsers.add_parser("accept", help="Accept invitation")
    accept_p.add_argument("invitation_id", help="Invitation ID")
    
    # Invitations
    invitations_p = subparsers.add_parser("invitations", help="Show invitations")
    invitations_p.add_argument("id", nargs="?", help="Capsule ID (optional)")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    manager = CapsuleManager()
    
    try:
        if args.command == "create":
            create_capsule(args.type, args.id, manager)
        
        elif args.command == "load":
            load_capsule(args.id, manager)
        
        elif args.command == "status":
            capsule_id = args.id or manager.get_current_capsule_id()
            if not capsule_id:
                print("Error: No capsule specified and no current capsule")
                print("  Use: cli.py load <id>  or  cli.py status <id>")
                return
            show_status(capsule_id, manager)
        
        elif args.command == "list":
            list_capsules(manager)
        
        elif args.command == "invite":
            sender_id = manager.get_current_capsule_id()
            if not sender_id:
                print("Error: No current capsule")
                print("  Use: cli.py load <sender-id>  first")
                return
            send_invitation(sender_id, args.recipient, args.slot, manager)
        
        elif args.command == "accept":
            capsule_id = manager.get_current_capsule_id()
            if not capsule_id:
                print("Error: No current capsule")
                print("  Use: cli.py load <your-id>  first")
                return
            accept_invitation(capsule_id, args.invitation_id, manager)
        
        elif args.command == "invitations":
            capsule_id = args.id or manager.get_current_capsule_id()
            if not capsule_id:
                print("Error: No capsule specified")
                print("  Use: cli.py invitations <id>  or  cli.py load <id> first")
                return
            show_invitations(capsule_id, manager)
    
    except KeyboardInterrupt:
        print("\n⏹️  Cancelled")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
