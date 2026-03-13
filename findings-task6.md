# Task 6: Card Counting Deviations

## Summary

Card counting exploits the fact that blackjack is a game with memory — cards already dealt change the composition of remaining cards, shifting EVs. Basic strategy is optimal for an average deck composition. When the composition deviates significantly (as tracked by the running/true count), some basic strategy decisions become suboptimal.

The most important deviations are codified as the **"Illustrious 18"** by Don Schlesinger, plus the **"Fab 4" surrenders**.

## Card Counting Basics

### Hi-Lo System

The most common counting system assigns:
- **+1**: Cards 2, 3, 4, 5, 6 (low cards favor dealer)
- **0**: Cards 7, 8, 9 (neutral)
- **-1**: Cards 10, J, Q, K, A (high cards favor player)

**Running Count (RC)**: Sum of assigned values as cards are dealt.
**True Count (TC)**: RC divided by number of remaining decks. TC = RC / decks_remaining.

A positive TC means more high cards remain (favorable to player):
- More blackjacks (player gets 3:2, dealer doesn't)
- Dealer busts more on stiff hands (must hit, more 10s available)
- Doubling is more profitable (more 10s for 10/11 doubles)
- Insurance becomes profitable (more 10s behind dealer Ace)

## The Illustrious 18

These are the 18 most valuable strategy deviations, ordered by their contribution to profit from counting. The "index" is the TC at which the decision changes from basic strategy.

| # | Hand | vs. | Basic | Deviation | Index (TC) | Notes |
|---|------|-----|-------|-----------|------------|-------|
| 1 | Insurance | A | No | Yes | +3 | Most valuable single play |
| 2 | 16 | 10 | H | S | 0 | Stand when TC >= 0 |
| 3 | 15 | 10 | H | S | +4 | Stand when TC >= +4 |
| 4 | 10,10 | 5 | S | P | +5 | Split 10s at very high count |
| 5 | 10,10 | 6 | S | P | +4 | Split 10s at very high count |
| 6 | 10 | 10 | H | D | +4 | Double 10 vs. 10 at high count |
| 7 | 12 | 3 | H | S | +2 | Stand at TC >= +2 |
| 8 | 12 | 2 | H | S | +3 | Stand at TC >= +3 |
| 9 | 11 | A | D | D | +1 | Always double (even more at +1; under S17 some say hit at TC < +1) |
| 10 | 9 | 2 | H | D | +1 | Double at TC >= +1 |
| 11 | 10 | A | H | D | +4 | Double 10 vs. A at high count |
| 12 | 9 | 7 | H | D | +3 | Double at TC >= +3 |
| 13 | 16 | 9 | H | S | +5 | Stand at very high count |
| 14 | 13 | 2 | S | H | -1 | Hit at TC <= -1 |
| 15 | 12 | 4 | S | H | 0 | Hit when TC <= -1 (some say 0) |
| 16 | 12 | 5 | S | H | -2 | Hit at TC <= -2 |
| 17 | 12 | 6 | S | H | -1 | Hit at TC <= -1 |
| 18 | 13 | 3 | S | H | -2 | Hit at TC <= -2 |

### Analysis of Key Deviations

#### #1: Insurance at TC >= +3

**The single most valuable counting play.**

Insurance is a side bet that pays 2:1 if the dealer has a 10-value hole card when showing an Ace.

At neutral count: P(10 in hole) = 16/51 ≈ 31.37% (single deck) or ≈ 30.77% (infinite deck). For insurance to break even, you need P(10) = 1/3 ≈ 33.33%.

With each unit of TC:
- Approximately 1 more high card per deck remaining
- In a 6-deck shoe: each TC unit shifts the 10-density by roughly 1/52 per deck

At TC = +3:
- Roughly 3 extra high cards per remaining deck
- 10-value density approaches 33.3%
- Insurance EV crosses from negative to positive

**EV of insurance at various TCs (6-deck, approximate):**
- TC 0: EV ≈ -0.077 (7.7% house edge on the insurance bet)
- TC +1: EV ≈ -0.044
- TC +2: EV ≈ -0.012
- TC +3: EV ≈ +0.021 (**profitable**)
- TC +4: EV ≈ +0.053
- TC +5: EV ≈ +0.086

Insurance occurs relatively frequently (whenever dealer shows Ace, ~7.7% of hands), and the swing from negative to positive EV is large, making this the most valuable deviation.

#### #2: 16 vs. 10 — Stand at TC >= 0

At the typical shoe composition (TC near 0), this hand is nearly break-even between hit and stand. The basic strategy says hit because at a perfectly neutral composition, hitting is marginally better.

At TC >= 0 (more precisely, TC >= 0), the extra high cards in the deck:
1. Make your bust probability slightly higher (more 10s to draw)
2. Make the dealer more likely to bust when standing (dealer must draw to their 10-showing hand and more high cards penalize the stiff dealer hands too)

The net effect favors standing. This is the second-most valuable deviation because 16 vs. 10 occurs very frequently (roughly 2.4% of all hands).

**TC Sensitivity:**
- TC = -2: EV(Hit) - EV(Stand) ≈ +0.06 → clearly hit
- TC = -1: EV(Hit) - EV(Stand) ≈ +0.04 → hit
- TC = 0: EV(Hit) - EV(Stand) ≈ +0.01 → barely hit (some say stand)
- TC = +1: EV(Hit) - EV(Stand) ≈ -0.02 → stand
- TC = +3: EV(Hit) - EV(Stand) ≈ -0.05 → clearly stand

#### #3: 15 vs. 10 — Stand at TC >= +4

Similar to 16 vs. 10 but requires a higher count because 15 has more room to improve (draws of 2-6 improve without busting), so you need a stronger high-card signal before standing becomes correct.

#### #4-5: Split 10,10 vs. 5/6 at TC +5/+4

At extremely high counts, the deck is so rich in 10s and Aces that:
1. Each split 10 has an excellent chance of drawing 10 or A for 20-21
2. The dealer 5 or 6 busts at an even higher rate than normal

However, splitting 10s is a **major tell to casino surveillance**. This play should be used sparingly and only at very high counts.

#### #7-8: 12 vs. 3 at TC +2, 12 vs. 2 at TC +3

Basic strategy says hit 12 vs. 2 and 3 because the bust probability is only 30.8% and the dealer's bust rate is under 38%. But at positive counts:
- Your bust probability increases (more 10s to draw)
- Dealer bust probability increases (more 10s for dealer to draw on stiff hands)

The second effect outweighs the first for the player on 12, so standing becomes correct.

#### #14-18: Standing hands become hits at negative counts

When the count goes negative, the deck is rich in low cards:
- Dealer is less likely to bust (more low cards to draw safely)
- Your stiff hand is slightly less likely to bust (but you're drawing into bad totals)
- Net effect: standing on 12-13 vs. weak upcards becomes worse

So at negative counts, you start hitting hands you'd normally stand on (13 vs. 2, 12 vs. 4-6).

## The Fab 4 Surrenders

These are the four most valuable surrender deviations:

| # | Hand | vs. | Basic (no surr.) | Deviation | Index (TC) |
|---|------|-----|-----------------|-----------|------------|
| 1 | 14 | 10 | H | R (Surrender) | +3 |
| 2 | 15 | 10 | R | R (earlier) | 0 (basic strategy already surrenders) |
| 3 | 15 | 9 | H | R (Surrender) | +2 |
| 4 | 15 | A | H | R (Surrender) | +1 (H17) / not applicable (S17) |

At high counts, stiff hands against strong dealer upcards become even more dangerous (more 10s to bust both you and the dealer, but your bust comes first). Surrendering these hands protects against the increased bust risk.

## How Much Does Counting Reduce the House Edge?

### Theoretical Analysis

With perfect basic strategy, the house edge is approximately 0.5% (varies by rules). Card counting provides an edge through two mechanisms:

1. **Bet variation** (most important): Betting more when the count is positive (player advantage) and less when negative (house advantage). This is worth approximately 0.5-1.5% edge, depending on spread.

2. **Play variation** (Illustrious 18): Playing deviations from basic strategy. This is worth approximately 0.1-0.2% additional edge.

### Combined Effect (6-deck, S17, DAS, 75% penetration)

| Bet Spread | Player Edge (approximate) |
|------------|--------------------------|
| 1:4 | +0.25% |
| 1:8 | +0.7% |
| 1:12 | +1.0% |
| 1:16 | +1.2% |

Without play deviations (Illustrious 18), these edges would be approximately 0.1-0.2% lower.

### Penetration Impact

Deck penetration (how deep into the shoe before reshuffling) is crucial:

| Penetration | Relative Counting Effectiveness |
|-------------|-------------------------------|
| 50% (3 of 6 decks) | ~40% of maximum |
| 67% (4 of 6 decks) | ~70% of maximum |
| 75% (4.5 of 6 decks) | ~85% of maximum |
| 83% (5 of 6 decks) | ~100% (reference) |

Poor penetration drastically reduces counting effectiveness because the extreme counts (where big bets should be placed) occur less frequently.

## Advanced Counting Concepts

### Ace Side Counts

The Hi-Lo system counts Aces as -1, grouping them with 10s. But Aces are special:
- For hitting/standing: Aces are good (make 21, provide soft hands)
- For doubling: Aces are good (A + 10 = 21)
- For insurance: Aces are neutral (we care about 10s in the hole)

An Ace side count tracks Aces separately. The expected number of Aces remaining can be compared to the actual count to adjust decisions, particularly for insurance and doubling.

### True Count Conversion for Different Deck Sizes

| Decks | TC = +3 means roughly... |
|-------|--------------------------|
| 1 | 3 excess high cards in 1 deck |
| 2 | 6 excess high cards in 2 decks |
| 6 | 18 excess high cards in 6 decks |
| 8 | 24 excess high cards in 8 decks |

The true count normalizes the running count by decks remaining, making it comparable across shoe sizes.

### Wonging (Back-counting)

Stanford Wong popularized entering the game only when the count is favorable. By "Wonging in" at TC >= +1 and leaving at TC <= -1:
- The player faces only advantageous shoes
- Effective player edge can exceed 1% with moderate spreads
- Most casinos now prohibit mid-shoe entry to counter this

## Practical Considerations

1. **Speed vs. accuracy**: In a real casino, you must count cards while playing, talking, and maintaining a natural appearance. Practicing to automate the count is essential.

2. **Risk of ruin**: Even with a positive edge, short-term variance is high. A 1% edge with $100 bets has a standard deviation of about $1,140 per hour, meaning losing sessions are common.

3. **Camouflage**: Using all 18 deviations accurately marks you as a counter. Many players deliberately make "wrong" plays (like not splitting 10s) to avoid detection.

4. **Team play**: MIT Blackjack Team model — spotters count at minimum bets, signal a "big player" to enter at high counts. This maximizes bet spread while distributing risk.
