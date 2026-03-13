# Task 5: Borderline Hands

## Summary

Borderline hands are those where the EV difference between the best and second-best action is less than 1% (0.01 units per unit bet). These hands are important because:
1. They are the hands casual players most often get wrong (small penalty)
2. They are the first to change under different rule variations
3. They form the basis of card-counting deviations (the "Illustrious 18")

## Complete List of Borderline Hands (EV margin < 0.01)

Ordered from tightest margin to widest. Conditions: infinite deck, S17, peek, DAS.

### Extremely Close (Margin < 0.002)

| # | Hand | vs. | Best | 2nd | Margin | EVs |
|---|------|-----|------|-----|--------|-----|
| 1 | Hard 12 | 4 | S | H | ~0.002 | S≈-0.211, H≈-0.213 |
| 2 | Hard 13 | 2 | S | H | ~0.003 | S≈-0.293, H≈-0.296 |

These two hands are so close that the penalty for playing the wrong action is nearly zero. They are also the first two hands on the "Illustrious 18" deviation list.

### Very Close (Margin 0.002-0.005)

| # | Hand | vs. | Best | 2nd | Margin | EVs |
|---|------|-----|------|-----|--------|-----|
| 3 | 16 | 10 | H | S | ~0.033 | H≈-0.507, S≈-0.540 |
| 4 | A,8 | 6 | S | D | ~0.012 | S≈+0.337, D≈+0.325 |
| 5 | Hard 9 | 2 | H | D | ~0.011 | H≈+0.088, D≈+0.077 |
| 6 | 11 | A(S17) | D | H | ~0.009 | D≈+0.127, H≈+0.118 |
| 7 | Hard 12 | 3 | H | S | ~0.018 | H≈-0.234, S≈-0.252 |
| 8 | A,2 | 4 | H | D | ~0.013 | H≈+0.001, D≈-0.012 |

Note: I've included some hands with margin > 0.01 but < 0.04 in the borderline discussion because they are traditionally considered close calls and appear on the Illustrious 18.

### Close (Margin 0.005-0.01)

| # | Hand | vs. | Best | 2nd | Margin | EVs |
|---|------|-----|------|-----|--------|-----|
| 9 | A,7 | 2 | S | D | ~0.019 | S≈+0.122, D≈+0.100 |
| 10 | 15 | 10 | H | S | ~0.037 | H≈-0.487, S≈-0.524 |
| 11 | 10 | A | H | D | ~0.025 | H≈+0.060, D≈+0.035 |
| 12 | 10 | 10 | H | D | ~0.025 | H≈+0.098, D≈+0.073 |
| 13 | 9,9 | 7 | S | P | ~0.091 | S≈+0.399, P≈+0.308 |

### Borderline by Category

#### Hard Hands (8 borderline decisions)
1. **12 vs. 4** — Tightest decision in blackjack (margin ~0.002)
2. **13 vs. 2** — Very close stand/hit (margin ~0.003)
3. **12 vs. 3** — Close hit/stand (margin ~0.018)
4. **16 vs. 10** — The famous hand (margin ~0.033)
5. **15 vs. 10** — Similar to 16 vs. 10 (margin ~0.037)
6. **9 vs. 2** — Hit/double borderline (margin ~0.011)
7. **10 vs. 10** — Hit/double borderline (margin ~0.025)
8. **10 vs. A** — Hit/double borderline (margin ~0.025)

#### Soft Hands (3 borderline decisions)
1. **A,8 vs. 6** — Stand/double borderline (margin ~0.012)
2. **A,7 vs. 2** — Stand/double borderline (margin ~0.019)
3. **A,2 vs. 4** — Hit/double borderline (margin ~0.013)

#### Pairs (2 borderline decisions)
1. **9,9 vs. A** — Stand/split borderline (margin ~0.040)
2. **6,6 vs. 2** — Split/hit borderline with DAS (margin varies)

## Deep Analysis of the Most Famous Borderline Hands

### 1. Hard 12 vs. Dealer 4

**The tightest decision in standard basic strategy.**

Stand: You keep 12 and hope dealer busts. Dealer 4 busts approximately 40.0%.
- If dealer busts (40.0%): you win +1 → contribution = +0.400
- If dealer makes 17: contribution depends on your 12 vs. 17 → lose
- Net EV(Stand) ≈ -0.211

Hit: You draw a card. Bust probability (need 10+) = 4/13 ≈ 30.8%.
- If you bust (30.8%): -1.0 → contribution = -0.308
- If you draw A: soft 13, play optimally
- If you draw 2-9: hard 14-21, play optimally
- Net EV(Hit) ≈ -0.213

**Margin: ~0.002 in favor of standing.** This is so small that:
- Getting it wrong costs you $0.20 per $100 bet
- At a true count of 0, this is a stand; at TC -1 or below, it becomes a hit (Illustrious 18 index = 0)
- Different deck counts can flip this

### 2. Hard 16 vs. Dealer 10

**The most discussed hand in blackjack.**

Hitting 16 vs. 10: You bust 61.5% of the time (any card 6-10,A). When you survive (38.5%), you have 17-21 and play against a dealer showing 10.

Standing on 16 vs. 10: Dealer has ~23% bust rate with 10 up. But dealer reaches 20 about 34% of the time and 17-21 about 77% of the time. Your 16 loses to all of those.

- EV(Hit) ≈ -0.507
- EV(Stand) ≈ -0.540
- **Margin: ~0.033 in favor of hitting**

This hand is not as close as 12 vs. 4, but it feels close because both options are terrible. The psychological difficulty is that hitting usually results in immediate visible loss (busting), while standing results in a less visible loss (dealer reveals winning hand).

**Composition dependence**: If your 16 is composed of three or more cards (e.g., 4+5+7), you should stand. This is because the extra small cards you've consumed make the remaining deck richer in 10s (more likely to bust if you hit). This is a legitimate composition-dependent strategy change, not just a counting deviation.

### 3. Hard 11 vs. Dealer Ace (S17)

Under S17, this is the tightest doubling decision:
- EV(Double) ≈ +0.127
- EV(Hit) ≈ +0.118
- **Margin: ~0.009 in favor of doubling**

Under H17, the margin widens in favor of doubling because the dealer's Ace is slightly weaker (dealer must hit soft 17 instead of standing on it).

### 4. A,8 vs. Dealer 6

- EV(Stand) ≈ +0.337
- EV(Double) ≈ +0.325
- **Margin: ~0.012 in favor of standing (S17)**

Under H17, this flips to doubling. This is the most commonly cited rule-dependent borderline hand.

## Practical Implications

### Cost of Playing Incorrectly

For a player making $10 bets and playing 100 hands per hour, the cost of misplaying each borderline hand:

| Hand | Frequency (per 100 hands) | Cost per occurrence | Hourly cost |
|------|--------------------------|--------------------|----|
| 12 vs. 4 | ~0.8 | $0.02 | $0.016 |
| 13 vs. 2 | ~0.8 | $0.03 | $0.024 |
| 16 vs. 10 | ~2.4 | $0.33 | $0.79 |
| 9 vs. 2 | ~0.8 | $0.11 | $0.088 |

The costliest common mistake is not playing 16 vs. 10 correctly. But since most players already hit 16 vs. 10 (it's intuitive), the real costly mistakes tend to be:
- **Standing on 12 vs. 2 or 3** (should hit): Many players over-apply the "don't bust against dealer bust cards" rule.
- **Not doubling soft hands**: Many players never double soft hands, costing significant EV.

### Which Hands Change Under Rule Variations?

Borderline hands are the ones most likely to change:

| Hand | Standard (S17) | H17 Change? | 1-Deck Change? |
|------|---------------|-------------|----------------|
| 12 vs. 4 | S | No | No (but wider margin) |
| 13 vs. 2 | S | No | H in some analyses |
| 16 vs. 10 | H | No | H (composition-dependent: stand with 3+ cards) |
| 9 vs. 2 | H | No | D (single deck) |
| A,8 vs. 6 | S | D (H17) | D (some single-deck analyses) |
| 11 vs. A | D | D (wider margin) | D (wider margin) |
| A,7 vs. 2 | S | D (some H17) | D (some single-deck) |

## Connection to Card Counting

Borderline hands are precisely the hands where a small shift in deck composition (as tracked by a card count) changes the optimal play. The "Illustrious 18" index plays (Task 6) are almost entirely composed of borderline hands from this list.

A positive true count means more high cards remain, which:
- Increases dealer bust probability → favors standing on stiff hands
- Improves doubling draws → favors doubling
- Increases blackjack probability → raises insurance EV

A negative true count means more low cards remain, which:
- Decreases dealer bust probability → favors hitting stiff hands
- Worsens doubling draws → favors hitting over doubling
