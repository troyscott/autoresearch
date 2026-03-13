# Advanced Topic: Mathematical Foundations of Blackjack Analysis

## Introduction

This document provides the rigorous mathematical framework underlying all blackjack strategy calculations. It serves as a reference for the probability theory, combinatorial analysis, and optimization techniques used throughout this research.

## 1. The Blackjack Probability Space

### State Space

A blackjack game state is defined by:
- **Player hand**: Multiset of card values (e.g., {10, 6} for hard 16)
- **Dealer upcard**: Single card value
- **Remaining shoe composition**: Count of each card value remaining
- **Available actions**: Subset of {Hit, Stand, Double, Split, Surrender}

The total state space is enormous. For a 6-deck shoe with 312 cards, the number of possible shoe compositions is C(321, 9) ≈ 10^14. However, the analysis can be greatly simplified.

### Simplifying Assumptions

1. **Infinite deck model**: Each card drawn has a fixed probability independent of previous draws. This eliminates card removal effects and makes the analysis tractable.

2. **Face-down hole card**: Under peek rules, the hole card's existence is known (no BJ) but its value is not.

3. **No other players**: Other players' cards don't affect the mathematical analysis (they are invisible in infinite-deck, and in finite-deck they constitute a random sample with no information).

## 2. Dealer Outcome Probability Calculation

### Recursive Formulation

Let D(total, soft_aces, probs) be the probability distribution over final dealer totals.

**Base case**:
- If effective_total > 21: bust (probability mass goes to "bust")
- If effective_total >= 18: stand (probability mass goes to that total)
- If effective_total == 17 and (S17 or not soft): stand

**Recursive case**:
- For each card value v with probability p(v):
  - D(total + v, soft_aces + I(v=11), probs) with probability p(v)

Where effective_total = total - 10 × min(soft_aces, max(0, ceil((total-21)/10)))

This recursion terminates because the total strictly increases with each card drawn (minimum card value is 2), so eventually every path leads to a total of 17+ or bust.

### Computational Complexity

The number of distinct dealer states is bounded by:
- Total values: 2-26 (soft) or 2-31 (before ace reduction) → ~30 values
- Soft ace count: 0-4 (in practice 0-2) → ~3 values
- Total states: ~90

Each state branches into ~10 next states (one per distinct card value).

The recursive computation with memoization takes O(90 × 10) = O(900) operations. This is why combinatorial analysis is fast and preferred over simulation.

### Exact Dealer Probabilities (Infinite Deck, S17)

These are computed to 10 decimal places:

```
Upcard 2: {17: 0.1395283078, 18: 0.1348846550, 19: 0.1304590082,
           20: 0.1235653025, 21: 0.1196817997, bust: 0.3518809268}
Upcard 6: {17: 0.1654004007, 18: 0.1063618524, 19: 0.1063618524,
           20: 0.1005758399, 21: 0.0978205739, bust: 0.4234794807}
Upcard A: {17: 0.1309843156, 18: 0.1309843156, 19: 0.1309843156,
           20: 0.1309843156, 21: 0.0504128789, bust: 0.1156498587}
```

(Note: Ace probabilities are conditional on no dealer blackjack under peek rules)

## 3. Expected Value Computation

### EV of Standing

Given player total P and dealer upcard U:

EV(Stand | P, U) = Σ_{d ∈ {17,18,19,20,21}} Pr(dealer=d | U) × outcome(P, d) + Pr(bust | U) × 1

Where outcome(P, d) = +1 if P > d, -1 if P < d, 0 if P = d.

This is a simple weighted sum over 6 terms.

### EV of Hitting (Recursive)

EV(Hit | hand, U) = Σ_v Pr(draw v) × [
  if bust(hand + v): -1
  else: max(EV(Stand | total(hand+v), U), EV(Hit | hand+v, U))
]

This recursion captures the fact that after hitting, the player again chooses optimally between Hit and Stand.

**Termination**: The recursion terminates because:
1. Eventually the player busts (total > 21)
2. Eventually the player reaches 21 and must stand
3. In practice, the hand total increases with each card, and at 21 the player stands

**Convergence**: With infinite deck, the EV computation is exact (no sampling error). Each level of recursion multiplies by card probabilities, and the total probability mass decays exponentially with depth.

### EV of Doubling

EV(Double | hand, U) = 2 × Σ_v Pr(draw v) × [
  if bust(hand + v): -1
  else: EV(Stand | total(hand+v), U)
]

The factor of 2 accounts for the doubled bet. Note: after doubling, the player MUST stand (no further hitting).

### EV of Splitting

For a pair (c, c):

EV(Split | c, U) = 2 × Σ_v Pr(draw v) × optimal_play_EV({c, v}, U)

Where optimal_play_EV considers Hit, Stand, Double, and (if allowed) re-split for the split hand.

For split Aces: typically only one card per hand, so:
EV(Split Aces | A, U) = 2 × Σ_v Pr(draw v) × EV(Stand | total(A+v), U)

## 4. Optimal Strategy Derivation

For each hand state (hand composition, dealer upcard, available actions):

**a*(hand, U) = argmax_{a ∈ Actions} EV(a | hand, U)**

The basic strategy table is the collection of a*(hand, U) for all relevant hand states.

### Fixed-Point Nature

The optimal strategy is defined implicitly through the recursive EV computation: the EV of hitting depends on future optimal decisions. This is a dynamic programming problem where the "value function" (optimal EV from each state) satisfies:

V(hand, U) = max(EV(Stand | hand, U), EV(Hit | hand, U), EV(Double | hand, U), ...)

And EV(Hit) depends on V for successor states. Since successor states have higher totals, we can compute V bottom-up starting from total = 21 and working down.

## 5. Variance Calculation

The variance of a blackjack hand is:

Var(X) = E[X²] - E[X]²

For a basic strategy player:
- E[X] ≈ -0.005 (house edge)
- E[X²] ≈ 1.30 (depends on doubling/splitting frequency)
- SD(X) ≈ √1.30 ≈ 1.14

The higher moments arise from:
- Regular hands: X ∈ {-1, 0, +1}, contributing E[X²] = 1
- Doubles: X ∈ {-2, +2}, contributing E[X²] = 4 (but weighted by probability of doubling)
- Splits: X can be multi-valued, contributing to higher E[X²]
- Blackjacks: X = +1.5, contributing 2.25
- Surrenders: X = -0.5, contributing 0.25

## 6. Conditional Probability Under Peek Rule

When dealer shows Ace and peeks (no BJ), we condition on the event "hole card ≠ 10-value":

Pr(hole = v | no BJ, upcard = A) = Pr(hole = v) / Pr(hole ≠ 10) for v ≠ 10
                                  = 0 for v = 10

Pr(hole ≠ 10) = 9/13

So each non-10 card has conditional probability:
- Pr(v | no BJ) = (1/13) / (9/13) = 1/9 for v ∈ {2,...,9,A}

Similarly, when upcard = 10:
Pr(hole = v | no BJ, upcard = 10) = Pr(hole = v) / Pr(hole ≠ A) for v ≠ A
Pr(hole ≠ A) = 12/13

## 7. Card Removal Effects (Finite Deck)

In a finite shoe with N total cards, removing card c changes the probability of drawing card v:

Before removal: Pr(v) = count(v) / N
After removing c: Pr(v | c removed) = [count(v) - I(v=c)] / (N-1)

The change in probability: ΔPr(v) = Pr(v | c removed) - Pr(v)

For v = c: ΔPr = -[N - count(v)] / [N(N-1)]  (probability decreases)
For v ≠ c: ΔPr = +count(c) / [N(N-1)]          (probability increases slightly)

In a 6-deck shoe (N=312), removing one card changes probabilities by approximately 1/312 ≈ 0.32%. This is why card removal effects are small in multi-deck games.

## 8. True Count as a Sufficient Statistic

The true count (TC) is an approximate sufficient statistic for the player's edge. The player's edge is approximately linear in TC:

Edge ≈ -0.5% + 0.5% × TC (approximate, varies by rules)

This linearity holds because:
1. Each unit of TC represents approximately 1 extra high card per remaining deck
2. The effect on dealer bust probability, blackjack probability, and doubling success is approximately proportional to the excess high-card density
3. Higher-order effects (TC² terms) are small

The quality of this linear approximation depends on the counting system. Hi-Lo captures ~97% of the betting-relevant information in a single linear summary.

## 9. Blackjack as a Markov Decision Process

Blackjack can be formulated as an MDP:
- **States**: (player hand, dealer upcard, shoe composition)
- **Actions**: {Hit, Stand, Double, Split, Surrender}
- **Transition**: Determined by card draw probabilities
- **Reward**: +1 (win), -1 (lose), 0 (push), ±2 (doubled), +1.5 (BJ), -0.5 (surrender)
- **Discount factor**: γ = 1 (finite horizon, no discounting)

The optimal policy for this MDP IS the basic strategy (with composition-dependent modifications in finite-deck).

The key property that makes blackjack tractable: **the MDP has a DAG structure** (hand totals only increase), ensuring finite horizon and eliminating cycles. This means value iteration converges in a single backward pass.

## 10. Game-Theoretic Perspective

Blackjack is NOT a strategic game between player and house in the game-theory sense, because:
1. The dealer follows fixed rules (no strategic choices)
2. The player's optimal strategy is independent of the dealer's "strategy" (which is deterministic)

This means there is no Nash equilibrium concept needed — pure optimization suffices.

However, the interaction between counter and casino IS game-theoretic:
- Counter chooses: bet spread, play deviations, camouflage
- Casino chooses: rules, penetration, surveillance threshold, shuffle frequency
- This is an adversarial game with incomplete information

The equilibrium of this meta-game determines the practical viability of card counting.
