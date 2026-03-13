# Advanced Topic: Side Bet Analysis

## Introduction

Side bets are optional wagers in blackjack that pay based on specific card combinations. They typically carry much higher house edges than the base game (2-15%+), but some are vulnerable to card counting or advantage play techniques.

## Common Side Bets Analyzed

### 1. Insurance

**Mechanics**: 2:1 payout if dealer has blackjack when showing Ace. Costs half the original bet.

**House edge at neutral count**: 7.69%

**Card counting vulnerability**: HIGH. Insurance is the most countable side bet because it depends entirely on 10-density.

| True Count | Player Edge on Insurance |
|-----------|-------------------------|
| 0 | -7.69% |
| +1 | -4.61% |
| +2 | -1.54% |
| +3 | +1.54% |
| +4 | +4.61% |
| +5 | +7.69% |

Insurance becomes profitable at TC >= +3 in a 6-deck game. Since insurance opportunities arise ~7.7% of hands, and the edge at high counts is significant, insurance is the most valuable card-counting deviation (as noted in Task 6).

### 2. Perfect Pairs

**Mechanics**: Bet that your first two cards form a pair.

**Payouts** (typical):
- Mixed pair (different color, e.g., 2♠ 2♥): 5:1
- Colored pair (same color, different suit, e.g., 2♠ 2♣): 10:1
- Perfect pair (same suit, e.g., 2♠ 2♠): 30:1

**Probabilities (8-deck)**:
- P(any pair) = 14.38%
  - P(mixed pair) = 7.47%
  - P(colored pair) = 4.74%
  - P(perfect pair) = 2.17%
- P(no pair) = 85.62%

**Expected value calculation**:
- EV = 0.0747(5) + 0.0474(10) + 0.0217(30) - 0.8562(1)
- EV = 0.3735 + 0.474 + 0.651 - 0.8562
- EV = +0.6423 ... this seems too favorable.

Let me recalculate more carefully:
- In an 8-deck shoe: 416 cards, 32 of each rank × 8 suits = 32 of each of 13 ranks
- Actually: 4 suits × 8 decks = 32 cards per rank? No: 13 ranks, 4 suits per deck × 8 decks = 32 cards per suit-rank pair...

Let me be precise. 8 decks: 52 × 8 = 416 cards. Each rank has 4 × 8 = 32 cards. Each specific card (e.g., 2♠) appears 8 times.

First card: any card. Second card from remaining 415 cards.
- P(perfect pair) = 7/415 (7 remaining copies of same suit-rank) = 1.687%
- P(colored pair) = 8/415 (8 copies of same-rank different-suit same-color) ...

Actually, for "colored pair" (same color, different suit): Each rank has 2 suits per color × 8 decks = 16 cards per color. First card drawn, say 2♠ (black). Same-rank same-color different-suit: 2♣ appears 8 times in the deck. So P(colored, diff suit) = 8/415 = 1.928%.

For "mixed pair" (different color): Same rank, different color. Two other suits of different color, each appearing 8 times = 16 cards. P(mixed) = 16/415 = 3.855%.

For "perfect pair" (exact same card): 7/415 = 1.687%.

Total pair probability: (7 + 8 + 16) / 415 = 31/415 = 7.47%

Hmm, let me check: 32 cards of same rank - 1 (the first card) = 31 remaining same-rank cards out of 415 total.
- Perfect pair: 7 copies of exact same card
- Colored pair: same-color, different suit: 8 copies
- Mixed pair: different-color suits: 16 copies
- Total: 31/415 = 7.47%

**Revised EV (8-deck, 30:10:5 payouts)**:
- EV = (7/415)(30) + (8/415)(10) + (16/415)(5) - (384/415)(1)
- EV = 0.5060 + 0.1928 + 0.1928 - 0.9253
- EV = -0.0337

**House edge: 3.37%**

Some casinos use different payout structures (25:12:6, etc.), shifting the edge.

**Card counting vulnerability**: MODERATE. If you track specific ranks, you can determine when the remaining shoe is enriched in specific ranks (increasing pair probability). However, the effect is small unless the shoe is very depleted.

### 3. 21+3 (Poker-Style Side Bet)

**Mechanics**: Uses your two cards + dealer's upcard to form a 3-card poker hand.

**Payouts** (typical):
- Suited three-of-a-kind: 100:1
- Straight flush: 40:1
- Three-of-a-kind: 30:1
- Straight: 10:1
- Flush: 5:1

**Probabilities (6-deck)**:
- Suited trips: ~0.0045%
- Straight flush: ~0.098%
- Three-of-a-kind (unsuited): ~0.235%
- Straight: ~3.26%
- Flush: ~6.29%
- Nothing: ~90.11%

**House edge**: Approximately 3.2-8.8% depending on paytable. The most common paytable yields about 3.2%.

**Card counting vulnerability**: LOW. The combinations depend on multiple card properties (rank and suit), making them difficult to track with standard counting systems.

### 4. Lucky Ladies

**Mechanics**: Pays based on player's first two cards totaling 20, with bonuses for specific combinations.

**Payouts** (typical):
- Queen of Hearts pair: 1000:1 (or 200:1 without dealer BJ match)
- Matched 20 (same rank and suit): 25:1
- Suited 20 (same suit): 10:1
- Any 20: 4:1

**House edge**: 17-25% depending on paytable. One of the highest-edge common side bets.

**Card counting vulnerability**: HIGH at extreme counts. At very high TC, the density of 10-value cards increases dramatically, making 20s much more likely. At TC >= +6, Lucky Ladies can become positive EV. However, such extreme counts are rare.

### 5. Royal Match

**Mechanics**: Pays if your first two cards are suited, with a bonus for King-Queen suited ("Royal Match").

**Payouts** (typical):
- Royal Match: 25:1
- Suited pair: 2.5:1 or 5:2

**Probabilities (6-deck)**:
- P(suited) = (5 × 6)/(6 × 52 - 1) × ... Let me compute properly.
- First card: any. Second card from same suit: (6 × 13 - 1) / (6 × 52 - 1) = 77/311 = 24.76%
- P(Royal Match) = P(suited K-Q) = very small

**House edge**: Approximately 3.7-6.7% depending on paytable.

**Card counting vulnerability**: LOW to MODERATE. Suit-tracking is needed, which is beyond standard counting.

### 6. Super Sevens

**Mechanics**: Pays escalating amounts based on receiving 7s.

**Payouts**:
- First card is 7: 3:1
- First two cards are 7s (unsuited): 50:1
- First two cards are 7s (suited): 100:1
- Three 7s (unsuited): 500:1
- Three 7s (suited): 5000:1

**House edge**: Approximately 11-12%. Very high house edge.

**Card counting vulnerability**: LOW. Would require tracking 7s specifically.

### 7. Bust It / Buster Blackjack

**Mechanics**: Pays when the dealer busts, with higher payouts for more cards in the dealer's busted hand.

**Typical payouts**:
- Dealer busts with 3 cards: 2:1
- 4 cards: 3:1
- 5 cards: 5:1
- 6 cards: 15:1
- 7 cards: 50:1
- 8+ cards: 250:1

**House edge**: Approximately 6-8%.

**Card counting vulnerability**: MODERATE. At negative counts (deck rich in small cards), the dealer is more likely to bust with many cards (drawing small cards repeatedly before busting). Some advantage players have exploited this.

## Side Bet Vulnerability Summary

| Side Bet | House Edge | Counting Vulnerability | Practical Edge Possible? |
|----------|-----------|----------------------|------------------------|
| Insurance | 7.7% | Very High | Yes (TC >= +3) |
| Perfect Pairs | 3-8% | Moderate | Rarely (need deep pen.) |
| 21+3 | 3-9% | Low | No |
| Lucky Ladies | 17-25% | High at extremes | Rarely (TC >= +6) |
| Royal Match | 4-7% | Low-Moderate | No |
| Super Sevens | 11-12% | Low | No |
| Buster BJ | 6-8% | Moderate | Marginal |

## General Side Bet Advice

1. **For basic strategy players**: Avoid all side bets. The house edge on every side bet is significantly higher than the base game (~0.5%).

2. **For card counters**: Insurance is the only consistently exploitable side bet. Lucky Ladies at extreme positive counts is theoretically beatable but the counts needed are rare.

3. **For the house**: Side bets are major profit centers. Players attracted by large payouts willingly accept 5-25% house edges, far exceeding the base game's ~0.5%.

4. **Mathematical perspective**: Side bets are essentially lottery tickets attached to a blackjack game. The high house edges compensate the casino for the jackpot-style payouts.

## Hole-Carding

A separate advantage technique: if the dealer inadvertently exposes the hole card (poor dealing technique or angled mirrors), knowing the hole card gives the player approximately a 10% edge on the base game. This also makes side bets either trivially beatable or irrelevant.

Hole-carding is legal (using visual information available to all players) but casinos will remove dealers with poor card-protection technique.

## Shuffle Tracking

Advanced technique: tracking groups ("slugs") of cards through a shuffle to predict where high-density or low-density regions of the shoe will appear.

- Requires poor shuffling procedure (e.g., simple riffle-strip-riffle)
- Can provide 1-2% edge if executed correctly
- Extremely difficult to do accurately in real-time
- Mostly obsolete with modern shuffle machines

## Edge Sorting

Exploiting manufacturing imperfections in card backs to identify specific cards:
- Made famous by Phil Ivey's baccarat cases
- Can provide enormous edges if specific high-value cards can be identified
- Casinos now use this as grounds for voiding winnings
- Legally gray area (courts have ruled both ways)
