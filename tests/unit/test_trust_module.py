import pytest
from src.core.capsule import Capsule, CapsuleType
from src.events.base import *
from src.modules.trust import TrustModule

def test_toggle_trust():
    capsule = Capsule(id="a", capsule_type=CapsuleType.PROTO)
    module = TrustModule(capsule)
    
    event = UserActionEvent(
        source="a",
        action_type=UserActionType.TOGGLE_STATE,
        target_capsule_id="b",
        state_name="trusted"
    )
    
    module.handle_event(event)
    assert capsule.get_relationship("b").trusted == True
    
    module.handle_event(event)
    assert capsule.get_relationship("b").trusted == False
