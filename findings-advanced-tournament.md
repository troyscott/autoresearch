# Advanced Topic: Tournament Blackjack Strategy

## Introduction

Tournament blackjack is fundamentally different from standard "money" blackjack. In a tournament:
- Players compete against each other, not against the house
- The goal is to have the most chips at the end of a fixed number of hands
- You must track opponents' chip counts and adjust strategy accordingly
- EV-maximizing play is often wrong; variance-maximizing (or minimizing) play is correct

## Tournament Structure

### Common Format
- 25-30 hands per round
- Table of 6-7 players
- Top 1-2 players advance
- Multiple elimination rounds leading to a final table

### Key Differences from Money Blackjack
1. **Relative position matters**: Your chip count relative to opponents determines success, not your absolute result
2. **The number of hands is fixed**: You can't grind a small edge over time
3. **Bet sizing is paramount**: More important than playing decisions
4. **Correlation with opponents**: You want your results to diverge from opponents (opposite bets)

## Tournament Betting Strategy

### Early Hands (Hands 1-15)

**Strategy: Moderate, information-gathering**
- Bet slightly above or below table average
- Follow basic strategy for playing decisions
- Track all opponents' chip counts
- Identify who is betting aggressively vs. conservatively

**Typical bet**: 10-20% of starting stack per hand

### Middle Hands (Hands 15-22)

**Strategy: Positioning**
- If behind, increase bet sizes to close the gap
- If ahead, match the leader's bets (correlation play)
- Consider bet timing relative to betting order

### Final Hands (Hands 23-30)

**Strategy: Calculated aggression**

This is where tournament strategy diverges most dramatically from money play.

**If you're the chip leader:**
- Match the second-place player's bet when possible
- If they bet big, bet big (maintain correlation)
- If they bet small, bet small (protect your lead)
- On the very last hand, bet enough to cover a maximum bet by the second-place player

**If you're behind:**
- Bet the opposite of the leader (decorrelation)
- Make large bets to create swing potential
- On the last hand, calculate the exact bet needed to overtake the leader

### The Last Hand

The last hand is the most important strategic moment. You must calculate:

**If behind by X chips:**
- Minimum bet needed: enough so that if you win and the leader loses, you end up ahead
- If leader bets B and you're behind by X: bet at least (X + B) / 2 if you need a win and leader needs a loss
- Consider doubling/splitting as ways to increase bet size

**If ahead by X chips:**
- Determine if you can "lock out" the second-place player
- Lock-out means: even if they win max bet and you lose your bet, you still have more chips
- If lock-out is possible, bet the minimum that maintains it
- If lock-out isn't possible, bet to maintain correlation

### Last Hand Lock-Out Formula

You have C₁ chips, opponent has C₂ chips, where C₁ > C₂.

Your bet: B₁. Opponent's max bet: B₂(max).

**Lock-out condition**: C₁ - B₁ > C₂ + 2 × B₂(max)

(The 2× accounts for the opponent potentially doubling down on the last hand)

If lock-out is possible: bet B₁ = C₁ - C₂ - 2 × B₂(max) - 1 (or table minimum if that's enough)

If lock-out isn't possible: bet aggressively and hope for divergent outcomes.

## Tournament Playing Strategy

### When to Deviate from Basic Strategy

**1. Correlation play (matching the table):**
When you're the chip leader and want to maintain your lead:
- Make the SAME decisions as your opponents
- If everyone stands on 16 vs. 10 (wrong), you might stand too, because winning/losing in sync preserves your lead
- Correct play only matters when your results need to diverge

**2. Variance-increasing deviations:**
When you need to catch up:
- Double on hands you wouldn't normally double
- Split more aggressively (creates two hands = more variance)
- Don't surrender (surrender reduces variance)
- Take insurance as a hedging bet if the leader has a larger bet

**3. Variance-decreasing deviations:**
When you need to protect a lead:
- Play conservatively
- Surrender more freely (limits downside)
- Don't double on borderline hands
- Don't split pairs in borderline situations

### Insurance as a Tournament Tool

Insurance in tournament play is fundamentally different from money play:
- It's a **hedging** tool, not an independent bet
- If you and your opponent both have large bets out and you're ahead, taking insurance can protect your lead
- If you're behind and the leader takes insurance, you should NOT take insurance (you want divergent results)

## Advanced Tournament Concepts

### Betting Order Advantage

In tournament blackjack, there is often a designated "first to bet" and "last to bet" position:
- **Betting last is a significant advantage**: You see opponents' bets before placing yours
- **Betting first is a disadvantage**: You bet blind, and opponents can react

The last-to-bet advantage is worth approximately 2-5% equity in a tournament round.

### Secret Bet Tournaments

Some tournaments use "secret bets" (bets placed face-down). This eliminates the information advantage and makes the game more like poker:
- Optimal strategy involves mixed strategies (randomization)
- Game theory / Nash equilibrium concepts apply
- Similar to sealed-bid auctions

### Surrender Strategy

In tournaments, surrender takes on added meaning:
- **Use surrender to guarantee advancement**: If you're leading and a half-bet loss still keeps you ahead, surrender to eliminate all variance
- **Avoid surrender when behind**: You need variance to catch up

### Multi-Way Last Hand

With 3+ players competing for 1-2 advancement spots, the last hand becomes highly strategic:
- You must consider how each opponent's bet interacts with yours
- It's possible to guarantee advancement even without the chip lead through careful bet sizing
- The mathematics becomes game-theoretic rather than purely probabilistic

## Tournament Bankroll Considerations

Tournament entries have different variance profiles than money play:
- **Buy-in**: Fixed, known cost
- **Payout**: Top-heavy (winner gets most of the prize pool)
- **Expected value**: Usually negative (house takes a cut), but can be positive for skilled players

**ROI for skilled tournament players**: Estimated 10-30% return on tournament buy-ins for top players, compared to the general negative expectation.

**Tournament portfolio approach**: Play many tournaments to smooth variance. A strong tournament player might cash in 20-30% of events but needs to balance that against the 70-80% of events with zero return.

## Example: Final Hand Calculation

**Scenario**:
- You have 1,200 chips, opponent has 1,000 chips
- Table max bet: 500
- You bet first

**Analysis**:
- If you bet 500 and win, you have 1,700
- If you bet 500 and lose, you have 700
- If opponent bets 500 and wins, they have 1,500
- If opponent bets 500 and loses, they have 500

**If you bet 500**:
- You both win: You win (1,700 vs 1,500) ✓
- You win, opponent loses: You win (1,700 vs 500) ✓
- You lose, opponent wins: You lose (700 vs 1,500) ✗
- You lose, opponent loses: You win (700 vs 500) ✓
- You win 3 out of 4 scenarios (75%)

**If you bet minimum (say 25)**:
- Opponent bets 500, both win: You lose (1,225 vs 1,500) ✗
- Opponent bets 500, you win they lose: You win (1,225 vs 500) ✓
- Opponent bets 500, you lose they win: You lose (1,175 vs 1,500) ✗
- Opponent bets 500, you lose they lose: You win (1,175 vs 500) ✓
- You win 2 out of 4 scenarios (50%)

**Conclusion**: The larger bet (correlated with opponent) is correct because it wins in more scenarios. This is the essence of "correlation play."

**Optimal bet**: The exact optimal depends on whether you know the opponent's bet. If you bet first and expect the opponent to bet large:
- Bet enough to cover if you both win: B ≥ opponent's chips + opponent's bet - your chips = 1000 + 500 - 1200 = 300
- Lock-out bet: C₁ - B₁ ≥ C₂ + 2(B₂max) → 1200 - B₁ ≥ 1000 + 1000 → B₁ ≤ -800 (impossible: can't lock out)
- Since lock-out isn't possible, bet 300-500 (high correlation)

## Key Takeaways

1. **Tournament blackjack is a different game** — chip-relative strategy dominates card-play strategy
2. **Bet sizing is more important than playing decisions** in tournaments
3. **The last hand is everything** — spend most mental energy on last-hand calculations
4. **Correlation/decorrelation** is the central concept: match the leader when ahead, oppose the leader when behind
5. **Basic strategy deviations** are justified when they increase/decrease variance as needed
6. **Position advantage** (betting order) is significant and should be exploited
