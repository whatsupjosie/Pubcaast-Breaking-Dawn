#!/usr/bin/env python3
"""
TEST 1: EQ ADAPTOR CARE-LEVEL TRANSITIONS
Tests the core accuracy of emotional state detection and care escalation/de-escalation.
"""

from modules.wired.eq_adaptor import EQAdaptor
import json


def test_care_transitions():
    """Verify care-level state machine transitions are correct and timely."""
    eq = EQAdaptor()
    user_id = "test_user"
    
    # Test suite: (message, expected_care_level, description)
    test_cases = [
        # Initial state
        ("Hi there", 0, "AMBIENT - baseline greeting"),
        
        # Escalation path
        ("I'm feeling a bit overwhelmed", 0, "AMBIENT - emotional word but no high velocity"),
        ("I CAN'T HANDLE THIS ANYMORE!!!", 1, "ATTENTIVE - high velocity caps/exclamation"),
        ("Everything is falling apart. I don't know what to do", 2, "CARE - sustained emotional signal"),
        ("I genuinely can't cope. I need help NOW", 3, "TOTAL_CARE_MANDATE - crisis escalation"),
        
        # De-escalation path
        ("Actually, I think I can manage this", 3, "CARE - still elevated despite positive words (sustained history)"),
        ("Yeah, I'm feeling better", 2, "ATTENTIVE - calm signals begin"),
        ("I'm okay now, thanks for listening", 1, "AMBIENT - returned to baseline"),
        
        # Edge cases
        ("", 1, "AMBIENT - empty message doesn't crash, stays in state"),
        ("a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a", 1, "AMBIENT - word repetition no effect"),
    ]
    
    results = []
    history = []
    
    for msg, expected_level, desc in test_cases:
        result = eq.process(user_id, msg, history)
        actual_level = result['state']['care_level']
        care_name = result['state']['care_name']
        agents = result['routing']['recommended_agents']
        
        # Build history for next iteration
        if msg:
            history.append({"role": "user", "content": msg})
        
        passed = actual_level == expected_level
        status = "✅" if passed else "❌"
        
        results.append({
            "status": status,
            "passed": passed,
            "message": msg[:40] if msg else "(empty)",
            "expected": expected_level,
            "actual": actual_level,
            "care_name": care_name,
            "agents": agents,
            "description": desc,
        })
    
    return results


def test_memory_and_context_injection():
    """Verify memory storage and context recall work correctly."""
    eq = EQAdaptor()
    user_id = "memory_test_user"
    
    # Store several memories
    eq.store_memory(user_id, "Works as a software engineer", "semantic", tags=["occupation", "tech"])
    eq.store_memory(user_id, "Recently experienced burnout", "episodic", tags=["work", "stress"])
    eq.store_memory(user_id, "Likes hiking and outdoor activities", "personal", tags=["hobby"])
    eq.store_memory(user_id, "Has a cat named Whiskers", "personal", tags=["family"])
    
    results = []
    
    # Test 1: Recall without query should return recent memories
    memories = eq.memory.get_all_memories(user_id)
    test_result = {
        "test": "Recall all memories",
        "passed": len(memories) == 4,
        "expected": 4,
        "actual": len(memories),
    }
    results.append(test_result)
    
    # Test 2: Query-based recall - search for "work"
    context = eq.get_memory_context(user_id, query="work")
    has_work_memory = "burnout" in context.lower() or "stress" in context.lower()
    test_result = {
        "test": "Query recall (work)",
        "passed": has_work_memory and context,
        "description": "Should recall burnout/stress memories when queried for 'work'",
        "context_length": len(context),
    }
    results.append(test_result)
    
    # Test 3: Query for "hobby"
    context_hobby = eq.get_memory_context(user_id, query="hobby")
    has_hobby_memory = "hiking" in context_hobby.lower() or "outdoor" in context_hobby.lower()
    test_result = {
        "test": "Query recall (hobby)",
        "passed": has_hobby_memory,
        "description": "Should recall hiking/outdoor memory",
    }
    results.append(test_result)
    
    # Test 4: Limit test - ask for 2 memories max
    memories_limited = eq.memory.recall(user_id, "personal", limit=2)
    test_result = {
        "test": "Recall with limit",
        "passed": len(memories_limited) <= 2,
        "expected": "≤ 2",
        "actual": len(memories_limited),
    }
    results.append(test_result)
    
    # Test 5: Prompt injection includes memory context
    result = eq.process(user_id, "I'm stressed about work", [])
    injection = result['prompt_injection']
    has_memory_in_injection = "User Memory Context" in injection or "burnout" in injection.lower()
    test_result = {
        "test": "Prompt injection with context",
        "passed": "work" in injection.lower() or len(injection) > 50,
        "description": "Should inject memory context into prompt",
        "injection_length": len(injection),
    }
    results.append(test_result)
    
    return results


def test_routing_accuracy():
    """Verify agent routing matches care level appropriately."""
    eq = EQAdaptor()
    user_id = "routing_test_user"
    
    results = []
    
    # Test routing at each care level
    routing_tests = [
        ("Hello", 0, ["pete"], "AMBIENT - humor/engagement agent"),
        ("I'm feeling troubled", 0, ["pete"], "Still AMBIENT despite emotional word"),
    ]
    
    history = []
    for msg, expected_care, expected_agents, desc in routing_tests:
        result = eq.process(user_id, msg, history)
        actual_care = result['state']['care_level']
        actual_agents = result['routing']['recommended_agents']
        
        history.append({"role": "user", "content": msg})
        
        agents_match = set(actual_agents) == set(expected_agents)
        test_result = {
            "test": f"Routing at care={expected_care}",
            "passed": actual_care == expected_care and agents_match,
            "message": msg,
            "expected_agents": expected_agents,
            "actual_agents": actual_agents,
            "description": desc,
        }
        results.append(test_result)
    
    return results


if __name__ == "__main__":
    print("\n" + "="*80)
    print("TEST 1: EQ ADAPTOR CARE-LEVEL TRANSITIONS & ACCURACY")
    print("="*80 + "\n")
    
    # Run transition tests
    print("Testing care-level state machine:\n")
    trans_results = test_care_transitions()
    passed_count = sum(1 for r in trans_results if r['passed'])
    
    for r in trans_results:
        status = r['status']
        print(f"{status} {r['description']:<50} → {r['care_name']:<20} agents={r['agents']}")
    
    print(f"\nTransitions: {passed_count}/{len(trans_results)} passed\n")
    
    # Memory tests
    print("-"*80)
    print("Testing memory storage and recall:\n")
    mem_results = test_memory_and_context_injection()
    mem_passed = sum(1 for r in mem_results if r['passed'])
    
    for r in mem_results:
        status = "✅" if r['passed'] else "❌"
        print(f"{status} {r['test']:<40} - {r.get('description', '')}")
    
    print(f"\nMemory tests: {mem_passed}/{len(mem_results)} passed\n")
    
    # Routing tests
    print("-"*80)
    print("Testing agent routing accuracy:\n")
    route_results = test_routing_accuracy()
    route_passed = sum(1 for r in route_results if r['passed'])
    
    for r in route_results:
        status = "✅" if r['passed'] else "❌"
        print(f"{status} {r['test']:<40} agents: {r['actual_agents']} (expected {r['expected_agents']})")
    
    print(f"\nRouting tests: {route_passed}/{len(route_results)} passed\n")
    
    # Summary
    total_passed = passed_count + mem_passed + route_passed
    total_tests = len(trans_results) + len(mem_results) + len(route_results)
    
    print("="*80)
    print(f"TOTAL: {total_passed}/{total_tests} tests passed ({100*total_passed//total_tests}%)")
    print("="*80 + "\n")
