# Advanced Topic: Kelly Criterion for Blackjack Bet Sizing

## Introduction

The Kelly Criterion provides the mathematically optimal bet size to maximize long-term bankroll growth while minimizing the risk of ruin. It is the cornerstone of professional blackjack bankroll management.

## The Kelly Formula

For a simple bet with probability p of winning and probability q = 1-p of losing, with payoff odds b:1, the Kelly fraction is:

**f* = (bp - q) / b**

Where f* is the fraction of bankroll to wager.

For blackjack, this is more complex because:
1. The edge varies with the true count
2. Payoffs are not binary (doubles, splits, blackjacks, pushes)
3. The variance per hand depends on the action taken

## Generalized Kelly for Blackjack

For a bet with expected value E(X) and variance Var(X):

**f* = E(X) / Var(X)**

In blackjack:
- E(X) = player edge (which varies with true count)
- Var(X) ≈ 1.30 (standard deviation ≈ 1.14, so variance ≈ 1.30)

### Kelly Bet at Various True Counts (6-deck, S17, DAS)

| True Count | Player Edge | Kelly Fraction | Bet (for $10,000 BR) |
|-----------|-------------|----------------|---------------------|
| -2 | -1.5% | 0 (min bet) | $10 (table minimum) |
| -1 | -1.0% | 0 (min bet) | $10 |
| 0 | -0.5% | 0 (min bet) | $10 |
| +1 | 0.0% | 0 | $10 |
| +2 | +0.5% | 0.38% | $38 |
| +3 | +1.0% | 0.77% | $77 |
| +4 | +1.5% | 1.15% | $115 |
| +5 | +2.0% | 1.54% | $154 |
| +6 | +2.5% | 1.92% | $192 |

The edge increases by approximately 0.5% per true count above +1.

### Half-Kelly and Fractional Kelly

Full Kelly is aggressive and produces high variance. Most professional players use fractional Kelly:

| Strategy | Growth Rate | Risk of Ruin (500-unit BR) |
|----------|-------------|---------------------------|
| Full Kelly | Maximum | ~13.5% |
| 3/4 Kelly | 93.75% of max | ~5% |
| Half Kelly | 75% of max | ~1.8% |
| 1/4 Kelly | 43.75% of max | ~0.03% |

**Half Kelly is the most common professional recommendation.** It sacrifices 25% of optimal growth rate but dramatically reduces risk of ruin.

## Practical Bet Spreading

### The Spread Problem

In practice, you can't vary bets from $0 to $200 freely. Casino surveillance flags large bet variation. Common spread strategies:

**1:8 Spread (e.g., $25-$200):**
- Bet $25 at TC <= +1
- Bet $50 at TC +2
- Bet $100 at TC +3
- Bet $150 at TC +4
- Bet $200 at TC +5+
- Expected edge: ~0.7% of action
- Hourly EV: ~$25-35/hour at $25 min

**1:12 Spread (e.g., $25-$300):**
- More aggressive, higher EV but higher heat
- Expected edge: ~1.0% of action
- Hourly EV: ~$40-50/hour at $25 min

**Wonging (back-counting + entry at TC >= +2):**
- Dramatically increases average edge (avoid negative counts)
- Effective edge: 1.5-2.0%
- But most casinos prohibit mid-shoe entry

### Calculating Expected Hourly Income

**Formula**: Hourly Income = (Average Bet) × (Hands/Hour) × (Player Edge)

For a 6-deck, S17, DAS game with 1:8 spread, $25 minimum:
- Average bet ≈ $45 (weighted by count distribution)
- Hands/hour ≈ 80 (heads-up) to 60 (full table)
- Player edge ≈ 0.7%
- **Hourly EV ≈ $45 × 70 × 0.007 ≈ $22/hour**

Standard deviation per hour: $45 × sqrt(70) × 1.14 ≈ **$429/hour**

This means a 95% confidence interval for a single hour is roughly -$836 to +$880. The edge only becomes statistically significant over many hours.

## Risk of Ruin

Risk of Ruin (RoR) is the probability of losing the entire bankroll before doubling it (or before some target).

### RoR Formula (Approximate)

**RoR ≈ e^(-2 × edge × bankroll / variance_per_hand)**

For a player with $10,000 bankroll, 0.7% edge, 1.30 variance per hand:
- RoR ≈ e^(-2 × 0.007 × 10000 / 1.30) ≈ e^(-107.7) ≈ effectively 0%

But this assumes optimal bet sizing. With a fixed $100 average bet:
- Units of bankroll = 100 units
- RoR ≈ e^(-2 × 0.007 × 100 / 1.30) ≈ e^(-1.077) ≈ 34%

**Rule of thumb**: You need at least 200 maximum bets in your bankroll for a comfortable risk level with full Kelly, or 100 max bets with half Kelly.

### Bankroll Requirements by Spread

| Spread | Max Bet | Recommended Bankroll | RoR (at this bankroll) |
|--------|---------|---------------------|----------------------|
| 1:4 | $100 | $20,000 | ~5% |
| 1:8 | $200 | $40,000 | ~5% |
| 1:12 | $300 | $60,000 | ~5% |
| 1:16 | $400 | $80,000 | ~5% |

## N0: The "Number of Hands to Get Ahead"

N0 is the number of hands needed for the expected gain to equal one standard deviation — i.e., the point where your edge starts to overcome variance.

**N0 = Variance / Edge^2**

For a card counter with 0.7% edge:
- N0 = 1.30 / (0.007)^2 = 1.30 / 0.000049 ≈ 26,531 hands

At 70 hands/hour, that's approximately **379 hours of play** before you can expect to be "one standard deviation ahead."

This is why professional blackjack requires:
1. Adequate bankroll (to survive the pre-N0 variance)
2. Patience (hundreds of hours before reliable profits)
3. Emotional discipline (enduring losing streaks that can last weeks)

## Kelly Criterion Limitations

1. **Edge estimation uncertainty**: If you overestimate your edge, Kelly overbets and RoR increases dramatically
2. **Non-independent bets**: Sequential hands from the same shoe are correlated
3. **Table limits**: Can't always bet the Kelly-optimal amount
4. **Camouflage cost**: Sometimes you need to make sub-optimal bets to avoid detection
5. **Utilities**: Kelly maximizes log-wealth growth, which assumes logarithmic utility. Some players may prefer different risk/reward tradeoffs

## Recommendations

1. **Use half-Kelly** as a conservative starting point
2. **Minimum bankroll**: 200× your maximum bet
3. **Track results meticulously** to validate your edge matches expectations
4. **Adjust for rules**: Better rules allow smaller bankrolls (higher edge per unit wagered)
5. **Consider team play** to pool bankroll and reduce individual risk
