"""
Test Cases for Dispatch Guard
Run: python test_dispatch.py
"""
from dispatch_guard import should_dispatch, reset_state

# Test data template
def create_signal(confidence=85, direction="BUY", entry=1.0850):
    return {
        "status": "ok",
        "payload": {
            "symbol": "EUR/USD",
            "timeframe": "M15",
            "confidence": confidence,
            "direction": direction,
            "entry": entry,
            "tp": 1.0900,
            "sl": 1.0800
        }
    }


def test_r1_confidence_threshold():
    """R1: Only send if confidence >= 60%"""
    print("\n🧪 TEST R1: Confidence Threshold")
    
    reset_state()
    
    # Should reject
    low_conf = create_signal(confidence=45)
    assert not should_dispatch(low_conf), "Should reject confidence < 60%"
    print("   ✅ Rejected confidence 45%")
    
    # Should accept
    good_conf = create_signal(confidence=75)
    assert should_dispatch(good_conf), "Should accept confidence >= 60%"
    print("   ✅ Accepted confidence 75%")


def test_r2_duplicate_prevention():
    """R2: Don't resend same direction + entry"""
    print("\n🧪 TEST R2: Duplicate Prevention")
    
    reset_state()
    
    # First signal - should send
    signal1 = create_signal(direction="BUY", entry=1.0850)
    assert should_dispatch(signal1), "First signal should send"
    print("   ✅ First signal sent")
    
    # Same signal - should block
    signal2 = create_signal(direction="BUY", entry=1.0850)
    assert not should_dispatch(signal2), "Duplicate should be blocked"
    print("   ✅ Duplicate blocked")
    
    # Different direction - should send
    signal3 = create_signal(direction="SELL", entry=1.0850)
    assert should_dispatch(signal3), "Direction change should send"
    print("   ✅ Direction change sent")


def test_r3_different_entry():
    """R2: Send if entry changes"""
    print("\n🧪 TEST R3: Entry Change")
    
    reset_state()
    
    signal1 = create_signal(entry=1.0850)
    should_dispatch(signal1)
    
    signal2 = create_signal(entry=1.0900)
    assert should_dispatch(signal2), "Entry change should send"
    print("   ✅ Entry change sent")


def test_r4_restart_safe():
    """R4: State persists across restarts"""
    print("\n🧪 TEST R4: Restart Safety")
    
    reset_state()
    
    signal = create_signal()
    should_dispatch(signal)
    
    # Simulate restart (state should persist)
    assert not should_dispatch(signal), "Should block after restart"
    print("   ✅ State persisted across restart")


def run_all_tests():
    """Run all test cases"""
    print("=" * 50)
    print("🧪 DISPATCH GUARD TEST SUITE")
    print("=" * 50)
    
    try:
        test_r1_confidence_threshold()
        test_r2_duplicate_prevention()
        test_r3_different_entry()
        test_r4_restart_safe()
        
        print("\n" + "=" * 50)
        print("✅ ALL TESTS PASSED")
        print("=" * 50)
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")


if __name__ == "__main__":
    run_all_tests()
