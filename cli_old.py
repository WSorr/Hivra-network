#!/usr/bin/env python3
"""
Hivra Network CLI
Event-driven, modular architecture
"""
import sys
import json
import uuid
import readline  # For command history
from typing import Dict, Optional, List
from src.core.capsule import Capsule, CapsuleType
from src.core.starter import Starter
from src.coordinator.event_bus import EventBus
from src.modules.invitation import InvitationModule
from src.modules.trust import TrustModule
from src.events.base import *

class HistoryCompleter:
    """Simple autocompleter for CLI"""
    def __init__(self, commands: List[str]):
        self.commands = commands
        self.matches = []
    
    def complete(self, text: str, state: int) -> Optional[str]:
        if state == 0:
            if text:
                self.matches = [c for c in self.commands if c.startswith(text)]
            else:
                self.matches = self.commands[:]
        
        try:
            return self.matches[state]
        except IndexError:
            return None

class CapsuleSystem:
    """Core system managing capsules and events"""
    
    def __init__(self):
        self.capsules: Dict[str, Capsule] = {}
        self.bus = EventBus()
    
    def create_capsule(self, capsule_id: str, capsule_type: CapsuleType = CapsuleType.PROTO) -> Capsule:
        """Create new capsule"""
        capsule = Capsule(id=capsule_id, capsule_type=capsule_type)
        self.capsules[capsule_id] = capsule
        
        # Create modules for this capsule
        inv_module = InvitationModule(capsule)
        trust_module = TrustModule(capsule)
        
        # Subscribe modules to events
        self.bus.subscribe(InviteEvent, inv_module.handle_event)
        self.bus.subscribe(UserActionEvent, inv_module.handle_event)
        self.bus.subscribe(UserActionEvent, trust_module.handle_event)
        self.bus.subscribe(StarterEvent, trust_module.handle_event)
        
        return capsule
    
    def add_starter_to_capsule(self, capsule_id: str, starter_id: Optional[str] = None) -> str:
        """Add starter to capsule (occupy slot)"""
        if capsule_id not in self.capsules:
            raise ValueError(f"Capsule {capsule_id} not found")
        
        capsule = self.capsules[capsule_id]
        empty_slot = capsule.find_empty_slot()
        
        if empty_slot is None:
            raise ValueError(f"Capsule {capsule_id} has no empty slots")
        
        if starter_id is None:
            starter = Starter.generate(capsule_id)
            starter_id = starter.id
        else:
            starter = Starter(id=starter_id, owner_capsule_id=capsule_id)
        
        capsule.occupy_slot(empty_slot, starter_id)
        return starter_id
    
    def send_invite(self, from_id: str, to_id: str, starter_id: str):
        """Send invitation from one capsule to another"""
        if from_id not in self.capsules:
            raise ValueError(f"Source capsule {from_id} not found")
        if to_id not in self.capsules:
            raise ValueError(f"Target capsule {to_id} not found")
        
        invite = InviteEvent(
            source=from_id,
            sender_capsule_id=from_id,
            target_capsule_id=to_id,
            sender_starter_id=starter_id
        )
        
        self.bus.publish(invite)
        return invite
    
    def accept_invite(self, capsule_id: str, from_id: str, starter_id: str):
        """Accept invitation"""
        if capsule_id not in self.capsules:
            raise ValueError(f"Capsule {capsule_id} not found")
        
        accept = UserActionEvent(
            source=capsule_id,
            action_type=UserActionType.ACCEPT_INVITE,
            target_capsule_id=from_id,
            invite_sender_id=from_id,
            invite_starter_id=starter_id
        )
        
        new_events = self.bus.publish(accept)
        
        # Process any generated events (like starter generation)
        for event in new_events:
            self.bus.publish(event)
        
        return new_events
    
    def toggle_trust(self, capsule_id: str, target_id: str):
        """Toggle trust relationship"""
        if capsule_id not in self.capsules:
            raise ValueError(f"Capsule {capsule_id} not found")
        
        toggle = UserActionEvent(
            source=capsule_id,
            action_type=UserActionType.TOGGLE_STATE,
            target_capsule_id=target_id,
            state_name="trusted"
        )
        
        self.bus.publish(toggle)
        return toggle
    
    def get_status(self, capsule_id: str) -> dict:
        """Get capsule status"""
        if capsule_id not in self.capsules:
            raise ValueError(f"Capsule {capsule_id} not found")
        
        capsule = self.capsules[capsule_id]
        
        slots_status = []
        for idx, slot in capsule.slots.items():
            slots_status.append({
                "slot": idx,
                "state": slot.state,
                "starter_id": slot.starter_id
            })
        
        relationships = {}
        for other_id, rel in capsule.relationships.items():
            relationships[other_id] = {
                "invited": rel.invited,
                "trusted": rel.trusted,
                "linked": rel.linked,
                "ignored": rel.ignored
            }
        
        return {
            "id": capsule.id,
            "type": capsule.capsule_type.value,
            "slots": slots_status,
            "relationships": relationships
        }
    
    def list_capsules(self) -> List[str]:
        """List all capsule IDs"""
        return list(self.capsules.keys())

def print_help():
    """Print CLI help"""
    print("""
Hivra Network CLI
=================

Commands:
  help                          Show this help
  create <id> [type]            Create capsule (types: genesis, proto, linked)
  status <id>                   Show capsule status
  add-starter <capsule_id>      Add starter to capsule
  invite <from> <to> <starter>  Send invitation
  accept <capsule> <from> <starter> Accept invitation
  trust <capsule> <target>      Toggle trust relationship
  list                          List all capsules
  exit                          Exit CLI

Examples:
  create capsule_a genesis
  create capsule_b proto
  add-starter capsule_a
  invite capsule_a capsule_b starter_123
  accept capsule_b capsule_a starter_123
  trust capsule_b capsule_a
  status capsule_b
""")

def main():
    """Main CLI loop"""
    system = CapsuleSystem()
    
    # Setup autocompletion
    commands = [
        "help", "create", "status", "add-starter", 
        "invite", "accept", "trust", "list", "exit"
    ]
    
    completer = HistoryCompleter(commands)
    readline.set_completer(completer.complete)
    readline.parse_and_bind("tab: complete")
    
    print("Hivra Network CLI (Press Tab for auto-completion)")
    print("Type 'help' for commands, 'exit' to quit\n")
    
    while True:
        try:
            cmd = input("hivra> ").strip()
            if not cmd:
                continue
            
            parts = cmd.split()
            command = parts[0]
            
            if command == "help":
                print_help()
            
            elif command == "create":
                if len(parts) < 2:
                    print("Usage: create <id> [type]")
                    continue
                
                capsule_id = parts[1]
                capsule_type = CapsuleType.PROTO
                if len(parts) > 2:
                    try:
                        capsule_type = CapsuleType(parts[2].lower())
                    except ValueError:
                        print(f"Invalid type. Use: {[t.value for t in CapsuleType]}")
                        continue
                
                system.create_capsule(capsule_id, capsule_type)
                print(f"Created capsule {capsule_id} ({capsule_type.value})")
            
            elif command == "list":
                capsules = system.list_capsules()
                if not capsules:
                    print("No capsules created")
                else:
                    print("Capsules:")
                    for cid in capsules:
                        capsule = system.capsules[cid]
                        print(f"  {cid} ({capsule.capsule_type.value})")
            
            elif command == "status":
                if len(parts) < 2:
                    print("Usage: status <capsule_id>")
                    continue
                
                try:
                    status = system.get_status(parts[1])
                    print(json.dumps(status, indent=2))
                except ValueError as e:
                    print(f"Error: {e}")
            
            elif command == "add-starter":
                if len(parts) < 2:
                    print("Usage: add-starter <capsule_id>")
                    continue
                
                try:
                    starter_id = system.add_starter_to_capsule(parts[1])
                    print(f"Added starter {starter_id} to {parts[1]}")
                except ValueError as e:
                    print(f"Error: {e}")
            
            elif command == "invite":
                if len(parts) < 4:
                    print("Usage: invite <from_id> <to_id> <starter_id>")
                    continue
                
                try:
                    system.send_invite(parts[1], parts[2], parts[3])
                    print(f"Invitation sent from {parts[1]} to {parts[2]}")
                except ValueError as e:
                    print(f"Error: {e}")
            
            elif command == "accept":
                if len(parts) < 4:
                    print("Usage: accept <capsule_id> <from_id> <starter_id>")
                    continue
                
                try:
                    events = system.accept_invite(parts[1], parts[2], parts[3])
                    print(f"Invitation accepted. Generated {len(events)} events")
                except ValueError as e:
                    print(f"Error: {e}")
            
            elif command == "trust":
                if len(parts) < 3:
                    print("Usage: trust <capsule_id> <target_id>")
                    continue
                
                try:
                    system.toggle_trust(parts[1], parts[2])
                    print(f"Trust toggled for {parts[1]} -> {parts[2]}")
                except ValueError as e:
                    print(f"Error: {e}")
            
            elif command == "exit":
                print("Goodbye!")
                break
            
            else:
                print(f"Unknown command: {command}. Type 'help' for commands.")
        
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except EOFError:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
