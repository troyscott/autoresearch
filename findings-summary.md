# Blackjack Basic Strategy Research: Summary of Findings

## Overview

This research project validated and analyzed the complete blackjack basic strategy through combinatorial analysis, probability calculations, and expected value comparisons. All 8 research tasks were completed, covering 350+ individual strategic decisions.

## Key Result: Strategy Tables Validated

The basic strategy tables provided in `program-blackjack.md` are **100% correct** for the standard game:
- **Conditions**: 6+ deck, S17 (dealer stands on soft 17), DAS (double after split allowed), dealer peeks for blackjack, no surrender
- **Hard totals**: All 170 cells validated (17 rows × 10 upcards)
- **Soft totals**: All 80 cells validated (8 rows × 10 upcards)
- **Pairs**: All 100 cells validated (10 rows × 10 upcards)

No changes to the existing tables are needed.

## Task-by-Task Summary

### Task 1: Hard Totals (findings-task1.md)
- Validated all hard total decisions with EV calculations
- Key insight: 12 vs. 4 is the tightest decision in blackjack (margin ~0.002)
- The dealer bust rate governs the hit/stand boundary: stand vs. 4-6 (bust rate 40%+), hit vs. 2-3 (bust rate 35-37%)
- 11 always doubles because you can't bust and have 38.5% chance of 20-21
- 10 doesn't double vs. 10/A because dealer's strong position doesn't justify the doubled stake

### Task 2: Soft Totals (findings-task2.md)
- Validated all soft total decisions
- The Ace "safety net" (can't bust on one hit) makes hitting and doubling more attractive
- A,7 (soft 18) is the most complex hand: Stand vs. 2/7/8, Double vs. 3-6, Hit vs. 9/10/A
- A,8 vs. 6 is rule-dependent: Stand under S17, Double under H17

### Task 3: Pairs (findings-task3.md)
- Validated all pair decisions with and without DAS
- Always split Aces (30.8% chance of 21 per hand) and 8s (escaping hard 16)
- Never split 5s (hard 10 is a great doubling hand) or 10s (hard 20 is near-certain win)
- 9,9 vs. 7 stands because 18 dominates the dealer's likely 17
- Without DAS, 7 pair cells change (mostly low pairs vs. marginal upcards)

### Task 4: Rule Variations (findings-task4.md)
- H17 costs +0.20% house edge; main strategy change is A,8 vs. 6 → Double
- Deck count: 1→2 decks is the biggest jump (+0.32%); 6→8 is negligible (+0.02%)
- DAS saves 0.14% and affects 7 pair decisions
- Late surrender saves 0.07-0.09%; apply to 16 vs. 10/A and 15 vs. 10
- No-peek: never double/split aggressively against dealer 10/A

### Task 5: Borderline Hands (findings-task5.md)
- Identified all hands with EV margin < 1%
- Top 5 tightest: 12 vs. 4, 13 vs. 2, 11 vs. A, 9 vs. 2, A,8 vs. 6
- These hands form the basis of card counting deviations
- Cost of misplaying borderline hands is small per occurrence but meaningful over time

### Task 6: Card Counting Deviations (findings-task6.md)
- Documented the Illustrious 18 and Fab 4 surrender deviations
- Insurance at TC >= +3 is the single most valuable deviation
- 16 vs. 10 → Stand at TC >= 0 is the second most valuable
- Card counting with 1:8 spread provides ~0.7% player edge in 6-deck games
- Play deviations add ~0.1-0.2% on top of bet-variation gains

### Task 7: House Edge Analysis (findings-task7.md)
- Documented house edges for 20+ rule configurations
- Range: 0.03% (single deck, S17, DAS) to 2.0%+ (8-deck, H17, 6:5 BJ)
- 6:5 BJ payout adds 1.36% — the single worst common rule change
- Never-bust strategy: 3.9% house edge (vs. 0.4% with basic strategy)
- Variance is enormous: 100K+ hands needed to observe the theoretical edge

### Task 8: Common Misconceptions (findings-task8.md)
- Ranked top 10 player mistakes by cost
- Biggest: not learning basic strategy at all (3-5% cost)
- Most psychologically difficult: hitting stiff hands vs. strong dealer, splitting 8,8 vs. 10
- Insurance/even money: always decline without card counting
- No betting system overcomes a negative-expectation game

## Strategy Table (Confirmed Correct)

### Hard Totals
```
       2    3    4    5    6    7    8    9   10    A
 5:    H    H    H    H    H    H    H    H    H    H
 6:    H    H    H    H    H    H    H    H    H    H
 7:    H    H    H    H    H    H    H    H    H    H
 8:    H    H    H    H    H    H    H    H    H    H
 9:    H    D    D    D    D    H    H    H    H    H
10:    D    D    D    D    D    D    D    D    H    H
11:    D    D    D    D    D    D    D    D    D    D
12:    H    H    S    S    S    H    H    H    H    H
13:    S    S    S    S    S    H    H    H    H    H
14:    S    S    S    S    S    H    H    H    H    H
15:    S    S    S    S    S    H    H    H    H    H
16:    S    S    S    S    S    H    H    H    H    H
17+:   S    S    S    S    S    S    S    S    S    S
```

### Soft Totals
```
         2    3    4    5    6    7    8    9   10    A
A,2:     H    H    H    D    D    H    H    H    H    H
A,3:     H    H    H    D    D    H    H    H    H    H
A,4:     H    H    D    D    D    H    H    H    H    H
A,5:     H    H    D    D    D    H    H    H    H    H
A,6:     H    D    D    D    D    H    H    H    H    H
A,7:     S    D    D    D    D    S    S    H    H    H
A,8:     S    S    S    S    S    S    S    S    S    S
A,9:     S    S    S    S    S    S    S    S    S    S
```

### Pairs
```
          2    3    4    5    6    7    8    9   10    A
A,A:      P    P    P    P    P    P    P    P    P    P
2,2:      P    P    P    P    P    P    H    H    H    H
3,3:      P    P    P    P    P    P    H    H    H    H
4,4:      H    H    H    P    P    H    H    H    H    H
5,5:      D    D    D    D    D    D    D    D    H    H
6,6:      P    P    P    P    P    H    H    H    H    H
7,7:      P    P    P    P    P    P    H    H    H    H
8,8:      P    P    P    P    P    P    P    P    P    P
9,9:      P    P    P    P    P    S    P    P    S    S
10,10:    S    S    S    S    S    S    S    S    S    S
```

## Engine

`blackjack_engine.py` contains:
- Combinatorial dealer outcome probability calculator
- Recursive EV calculations for Hit, Stand, Double, and Split
- Full strategy table generation
- Monte Carlo simulation framework
- Support for S17/H17, peek/no-peek, DAS/no-DAS variations
- Basic strategy and "never bust" strategy comparison

The engine uses Python standard library only (no external packages).

## Files

| File | Description |
|------|-------------|
| `blackjack_engine.py` | Simulation and analysis engine |
| `test_blackjack_engine.py` | Test suite for engine validation |
| `findings-task1.md` | Hard totals validation |
| `findings-task2.md` | Soft totals validation |
| `findings-task3.md` | Pairs validation |
| `findings-task4.md` | Rule variations analysis |
| `findings-task5.md` | Borderline hands identification |
| `findings-task6.md` | Card counting deviations |
| `findings-task7.md` | House edge analysis |
| `findings-task8.md` | Common misconceptions |
| `findings-summary.md` | This summary |
