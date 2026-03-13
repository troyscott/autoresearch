"""Tests for the blackjack engine analysis."""
import sys
sys.path.insert(0, '/opt/autoresearch-blkjk')
from blackjack_engine import (
    hand_value, dealer_probs, dealer_probs_with_peek, infinite_deck_probs,
    ev_stand, ev_hit, ev_double, ev_split, ev_surrender,
    best_action_hard, best_action_soft, best_action_pair,
    generate_hard_table, generate_soft_table, generate_pair_table,
    UPCARDS
)

def test_hand_value():
    assert hand_value([10, 7]) == (17, False)
    assert hand_value([11, 6]) == (17, True)
    assert hand_value([11, 11]) == (12, False)
    assert hand_value([11, 10]) == (21, True)
    assert hand_value([10, 6, 10]) == (26, False)
    assert hand_value([11, 5, 10]) == (16, False)
    print("hand_value tests passed")

def test_dealer_probabilities():
    """Calculate and print dealer outcome probabilities for all upcards."""
    probs = infinite_deck_probs()

    print("\n=== DEALER OUTCOME PROBABILITIES (S17, infinite deck, peek) ===")
    for uc in UPCARDS:
        dp = dealer_probs_with_peek(uc, probs, stands_soft_17=True)
        uc_name = 'A' if uc == 11 else str(uc)
        print(f"\nDealer upcard {uc_name}:")
        total_p = 0
        for outcome in [17, 18, 19, 20, 21, 'bust']:
            print(f"  {str(outcome):>4}: {dp[outcome]:.6f} ({dp[outcome]*100:.2f}%)")
            total_p += dp[outcome]
        print(f"  Sum: {total_p:.6f}")

    # Verify probabilities sum to 1
    for uc in UPCARDS:
        dp = dealer_probs_with_peek(uc, probs, stands_soft_17=True)
        total = sum(dp.values())
        assert abs(total - 1.0) < 0.001, f"Dealer probs for upcard {uc} sum to {total}"
    print("\nDealer probability tests passed")

def test_hard_totals_table():
    """Generate and display the hard totals strategy table."""
    print("\n=== HARD TOTALS TABLE (S17, infinite deck, peek) ===")
    hard_table, hard_evs = generate_hard_table()

    header = f"{'':>5}"
    for uc in UPCARDS:
        uc_name = 'A' if uc == 11 else str(uc)
        header += f"{uc_name:>5}"
    print(header)

    for total in range(5, 22):
        row = f"{total:>5}"
        for uc in UPCARDS:
            row += f"{hard_table[total][uc]:>5}"
        print(row)

    # Print detailed EVs for key hands
    print("\n=== KEY HARD HAND EVs ===")
    key_hands = [(16, 10), (16, 7), (12, 2), (12, 3), (12, 4), (11, 10), (11, 11), (10, 10), (10, 11), (9, 2)]
    for total, uc in key_hands:
        evs = hard_evs[total][uc]
        uc_name = 'A' if uc == 11 else str(uc)
        parts = []
        for a in ['S', 'H', 'D']:
            if a in evs:
                parts.append(f"{a}={evs[a]:+.6f}")
        print(f"  Hard {total} vs {uc_name}: {', '.join(parts)}")
        best = max(evs, key=evs.get)
        print(f"    Best: {best} (margin: {evs[best] - sorted(evs.values())[-2]:+.6f})")

def test_soft_totals_table():
    """Generate and display the soft totals strategy table."""
    print("\n=== SOFT TOTALS TABLE (S17, infinite deck, peek) ===")
    soft_table, soft_evs = generate_soft_table()

    header = f"{'':>7}"
    for uc in UPCARDS:
        uc_name = 'A' if uc == 11 else str(uc)
        header += f"{uc_name:>5}"
    print(header)

    for kicker in range(2, 10):
        row = f"  A,{kicker}:"
        for uc in UPCARDS:
            row += f"{soft_table[kicker][uc]:>5}"
        print(row)

    # Print detailed EVs for key soft hands
    print("\n=== KEY SOFT HAND EVs ===")
    key_soft = [(7, 2), (7, 3), (7, 6), (7, 7), (7, 9), (8, 6), (8, 5)]
    for kicker, uc in key_soft:
        evs = soft_evs[kicker][uc]
        uc_name = 'A' if uc == 11 else str(uc)
        parts = []
        for a in ['S', 'H', 'D']:
            if a in evs:
                parts.append(f"{a}={evs[a]:+.6f}")
        print(f"  A,{kicker} vs {uc_name}: {', '.join(parts)}")
        best = max(evs, key=evs.get)
        second = sorted(evs.values())[-2]
        print(f"    Best: {best} (margin: {evs[best] - second:+.6f})")

def test_pairs_table():
    """Generate and display the pairs strategy table."""
    print("\n=== PAIRS TABLE (S17, infinite deck, peek, DAS) ===")
    pair_table, pair_evs = generate_pair_table(das=True)

    pair_order = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    header = f"{'':>8}"
    for uc in UPCARDS:
        uc_name = 'A' if uc == 11 else str(uc)
        header += f"{uc_name:>5}"
    print(header)

    for pv in pair_order:
        label = 'A,A' if pv == 11 else f"{pv},{pv}"
        row = f"  {label:>4}:"
        for uc in UPCARDS:
            row += f"{pair_table[pv][uc]:>5}"
        print(row)

    # Print detailed EVs for key pairs
    print("\n=== KEY PAIR EVs ===")
    key_pairs = [(8, 10), (8, 11), (11, 10), (9, 7), (9, 10), (10, 5), (10, 6)]
    for pv, uc in key_pairs:
        evs = pair_evs[pv][uc]
        uc_name = 'A' if uc == 11 else str(uc)
        label = 'A,A' if pv == 11 else f"{pv},{pv}"
        parts = []
        for a in ['S', 'H', 'D', 'P']:
            if a in evs:
                parts.append(f"{a}={evs[a]:+.6f}")
        print(f"  {label} vs {uc_name}: {', '.join(parts)}")
        best = max(evs, key=evs.get)
        vals = sorted(evs.values(), reverse=True)
        if len(vals) > 1:
            print(f"    Best: {best} (margin: {vals[0] - vals[1]:+.6f})")

def test_compare_with_reference():
    """Compare computed strategy with the reference tables."""
    hard_table, hard_evs = generate_hard_table()
    soft_table, soft_evs = generate_soft_table()
    pair_table, pair_evs = generate_pair_table(das=True)

    # Reference from program-blackjack.md
    REF_HARD = {
        5:  {2:'H',3:'H',4:'H',5:'H',6:'H',7:'H',8:'H',9:'H',10:'H',11:'H'},
        6:  {2:'H',3:'H',4:'H',5:'H',6:'H',7:'H',8:'H',9:'H',10:'H',11:'H'},
        7:  {2:'H',3:'H',4:'H',5:'H',6:'H',7:'H',8:'H',9:'H',10:'H',11:'H'},
        8:  {2:'H',3:'H',4:'H',5:'H',6:'H',7:'H',8:'H',9:'H',10:'H',11:'H'},
        9:  {2:'H',3:'D',4:'D',5:'D',6:'D',7:'H',8:'H',9:'H',10:'H',11:'H'},
        10: {2:'D',3:'D',4:'D',5:'D',6:'D',7:'D',8:'D',9:'D',10:'H',11:'H'},
        11: {2:'D',3:'D',4:'D',5:'D',6:'D',7:'D',8:'D',9:'D',10:'D',11:'D'},
        12: {2:'H',3:'H',4:'S',5:'S',6:'S',7:'H',8:'H',9:'H',10:'H',11:'H'},
        13: {2:'S',3:'S',4:'S',5:'S',6:'S',7:'H',8:'H',9:'H',10:'H',11:'H'},
        14: {2:'S',3:'S',4:'S',5:'S',6:'S',7:'H',8:'H',9:'H',10:'H',11:'H'},
        15: {2:'S',3:'S',4:'S',5:'S',6:'S',7:'H',8:'H',9:'H',10:'H',11:'H'},
        16: {2:'S',3:'S',4:'S',5:'S',6:'S',7:'H',8:'H',9:'H',10:'H',11:'H'},
        17: {2:'S',3:'S',4:'S',5:'S',6:'S',7:'S',8:'S',9:'S',10:'S',11:'S'},
    }
    REF_SOFT = {
        2: {2:'H',3:'H',4:'H',5:'D',6:'D',7:'H',8:'H',9:'H',10:'H',11:'H'},
        3: {2:'H',3:'H',4:'H',5:'D',6:'D',7:'H',8:'H',9:'H',10:'H',11:'H'},
        4: {2:'H',3:'H',4:'D',5:'D',6:'D',7:'H',8:'H',9:'H',10:'H',11:'H'},
        5: {2:'H',3:'H',4:'D',5:'D',6:'D',7:'H',8:'H',9:'H',10:'H',11:'H'},
        6: {2:'H',3:'D',4:'D',5:'D',6:'D',7:'H',8:'H',9:'H',10:'H',11:'H'},
        7: {2:'S',3:'D',4:'D',5:'D',6:'D',7:'S',8:'S',9:'H',10:'H',11:'H'},
        8: {2:'S',3:'S',4:'S',5:'S',6:'S',7:'S',8:'S',9:'S',10:'S',11:'S'},
        9: {2:'S',3:'S',4:'S',5:'S',6:'S',7:'S',8:'S',9:'S',10:'S',11:'S'},
    }
    REF_PAIRS = {
        11: {2:'P',3:'P',4:'P',5:'P',6:'P',7:'P',8:'P',9:'P',10:'P',11:'P'},
        2:  {2:'P',3:'P',4:'P',5:'P',6:'P',7:'P',8:'H',9:'H',10:'H',11:'H'},
        3:  {2:'P',3:'P',4:'P',5:'P',6:'P',7:'P',8:'H',9:'H',10:'H',11:'H'},
        4:  {2:'H',3:'H',4:'H',5:'P',6:'P',7:'H',8:'H',9:'H',10:'H',11:'H'},
        5:  {2:'D',3:'D',4:'D',5:'D',6:'D',7:'D',8:'D',9:'D',10:'H',11:'H'},
        6:  {2:'P',3:'P',4:'P',5:'P',6:'P',7:'H',8:'H',9:'H',10:'H',11:'H'},
        7:  {2:'P',3:'P',4:'P',5:'P',6:'P',7:'P',8:'H',9:'H',10:'H',11:'H'},
        8:  {2:'P',3:'P',4:'P',5:'P',6:'P',7:'P',8:'P',9:'P',10:'P',11:'P'},
        9:  {2:'P',3:'P',4:'P',5:'P',6:'P',7:'S',8:'P',9:'P',10:'S',11:'S'},
        10: {2:'S',3:'S',4:'S',5:'S',6:'S',7:'S',8:'S',9:'S',10:'S',11:'S'},
    }

    print("\n=== COMPARISON WITH REFERENCE TABLES ===")

    diffs_hard = []
    for total in range(5, 18):
        for uc in UPCARDS:
            computed = hard_table[total][uc]
            ref = REF_HARD[total][uc]
            if computed != ref:
                evs = hard_evs[total][uc]
                uc_name = 'A' if uc == 11 else str(uc)
                ev_parts = ", ".join(f"{a}={evs[a]:+.6f}" for a in ['S','H','D'] if a in evs)
                diffs_hard.append((total, uc_name, ref, computed, ev_parts))

    if diffs_hard:
        print(f"\nHard totals differences ({len(diffs_hard)} cells):")
        for total, uc_name, ref, computed, ev_parts in diffs_hard:
            print(f"  Hard {total} vs {uc_name}: ref={ref}, computed={computed} | {ev_parts}")
    else:
        print("\nHard totals: ALL MATCH reference table")

    diffs_soft = []
    for kicker in range(2, 10):
        for uc in UPCARDS:
            computed = soft_table[kicker][uc]
            ref = REF_SOFT[kicker][uc]
            if computed != ref:
                evs = soft_evs[kicker][uc]
                uc_name = 'A' if uc == 11 else str(uc)
                ev_parts = ", ".join(f"{a}={evs[a]:+.6f}" for a in ['S','H','D'] if a in evs)
                diffs_soft.append((kicker, uc_name, ref, computed, ev_parts))

    if diffs_soft:
        print(f"\nSoft totals differences ({len(diffs_soft)} cells):")
        for kicker, uc_name, ref, computed, ev_parts in diffs_soft:
            print(f"  A,{kicker} vs {uc_name}: ref={ref}, computed={computed} | {ev_parts}")
    else:
        print("\nSoft totals: ALL MATCH reference table")

    diffs_pairs = []
    for pv in [11, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
        for uc in UPCARDS:
            computed = pair_table[pv][uc]
            ref = REF_PAIRS[pv][uc]
            if computed != ref:
                evs = pair_evs[pv][uc]
                uc_name = 'A' if uc == 11 else str(uc)
                label = 'A,A' if pv == 11 else f"{pv},{pv}"
                ev_parts = ", ".join(f"{a}={evs[a]:+.6f}" for a in ['S','H','D','P'] if a in evs)
                diffs_pairs.append((label, uc_name, ref, computed, ev_parts))

    if diffs_pairs:
        print(f"\nPairs differences ({len(diffs_pairs)} cells):")
        for label, uc_name, ref, computed, ev_parts in diffs_pairs:
            print(f"  {label} vs {uc_name}: ref={ref}, computed={computed} | {ev_parts}")
    else:
        print("\nPairs: ALL MATCH reference table")

def test_borderline_hands():
    """Identify all hands where EV difference between best and second-best action < 1%."""
    print("\n=== BORDERLINE HANDS (EV margin < 0.01) ===")

    hard_table, hard_evs = generate_hard_table()
    soft_table, soft_evs = generate_soft_table()
    pair_table, pair_evs = generate_pair_table(das=True)

    borderlines = []

    # Hard totals
    for total in range(5, 22):
        for uc in UPCARDS:
            evs = hard_evs[total][uc]
            vals = sorted(evs.values(), reverse=True)
            if len(vals) >= 2:
                margin = vals[0] - vals[1]
                if margin < 0.01:
                    best = max(evs, key=evs.get)
                    second = [k for k, v in evs.items() if v == vals[1]][0]
                    uc_name = 'A' if uc == 11 else str(uc)
                    borderlines.append((f"Hard {total}", uc_name, best, second, margin, evs))

    # Soft totals
    for kicker in range(2, 10):
        for uc in UPCARDS:
            evs = soft_evs[kicker][uc]
            vals = sorted(evs.values(), reverse=True)
            if len(vals) >= 2:
                margin = vals[0] - vals[1]
                if margin < 0.01:
                    best = max(evs, key=evs.get)
                    second = [k for k, v in evs.items() if v == vals[1]][0]
                    uc_name = 'A' if uc == 11 else str(uc)
                    borderlines.append((f"A,{kicker}", uc_name, best, second, margin, evs))

    # Pairs
    for pv in [11, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
        for uc in UPCARDS:
            evs = pair_evs[pv][uc]
            vals = sorted(evs.values(), reverse=True)
            if len(vals) >= 2:
                margin = vals[0] - vals[1]
                if margin < 0.01:
                    best = max(evs, key=evs.get)
                    second = [k for k, v in evs.items() if v == vals[1]][0]
                    uc_name = 'A' if uc == 11 else str(uc)
                    label = 'A,A' if pv == 11 else f"{pv},{pv}"
                    borderlines.append((label, uc_name, best, second, margin, evs))

    borderlines.sort(key=lambda x: x[4])

    for hand, uc_name, best, second, margin, evs in borderlines:
        ev_str = ", ".join(f"{a}={evs[a]:+.6f}" for a in sorted(evs.keys()))
        print(f"  {hand:>10} vs {uc_name:>2}: {best} vs {second}, margin={margin:.6f} | {ev_str}")

    print(f"\nTotal borderline hands: {len(borderlines)}")

def test_h17_vs_s17():
    """Compare strategy under H17 vs S17 rules."""
    print("\n=== H17 vs S17 COMPARISON ===")

    # S17
    hard_s17, evs_s17 = generate_hard_table(s17=True)
    soft_s17, sevs_s17 = generate_soft_table(s17=True)

    # H17
    hard_h17, evs_h17 = generate_hard_table(s17=False)
    soft_h17, sevs_h17 = generate_soft_table(s17=False)

    print("\nHard totals that change between S17 and H17:")
    for total in range(5, 22):
        for uc in UPCARDS:
            s17_action = hard_s17[total][uc]
            h17_action = hard_h17[total][uc]
            if s17_action != h17_action:
                uc_name = 'A' if uc == 11 else str(uc)
                print(f"  Hard {total} vs {uc_name}: S17={s17_action}, H17={h17_action}")

    print("\nSoft totals that change between S17 and H17:")
    for kicker in range(2, 10):
        for uc in UPCARDS:
            s17_action = soft_s17[kicker][uc]
            h17_action = soft_h17[kicker][uc]
            if s17_action != h17_action:
                uc_name = 'A' if uc == 11 else str(uc)
                print(f"  A,{kicker} vs {uc_name}: S17={s17_action}, H17={h17_action}")

def test_all_ev_details():
    """Print ALL EVs for complete documentation."""
    print("\n=== COMPLETE HARD TOTALS EV TABLE ===")
    hard_table, hard_evs = generate_hard_table()

    for total in range(5, 22):
        for uc in UPCARDS:
            evs = hard_evs[total][uc]
            uc_name = 'A' if uc == 11 else str(uc)
            best = max(evs, key=evs.get)
            parts = ", ".join(f"{a}={evs[a]:+.6f}" for a in ['S','H','D'] if a in evs)
            print(f"  Hard {total:>2} vs {uc_name:>2}: best={best} | {parts}")

if __name__ == "__main__":
    test_hand_value()
    test_dealer_probabilities()
    test_hard_totals_table()
    test_soft_totals_table()
    test_pairs_table()
    test_compare_with_reference()
    test_borderline_hands()
    test_h17_vs_s17()
