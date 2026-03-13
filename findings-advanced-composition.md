# Advanced Topic: Composition-Dependent Strategy

## Introduction

Basic strategy considers only the **total** of the player's hand and whether it is soft or hard. Composition-dependent strategy (CDS) considers the **specific cards** that make up the total. For most hands, composition doesn't matter. But for a few critical situations, it changes the optimal play.

## Why Composition Matters

In a finite shoe, each card dealt changes the remaining distribution. When you hold specific cards, you have information about what's NOT in the remaining shoe. This "card removal effect" changes the probabilities of subsequent draws.

Example: Hard 16 composed as 10+6 vs. Hard 16 composed as 9+7:
- With 10+6: One fewer 10-value card in the shoe → hitting is slightly less dangerous (fewer 10s to bust you) and slightly more likely to draw a small card
- With 9+7: Normal 10-density → standard bust probability

The effect is small in multi-deck games but measurable in single and double-deck.

## Hands Where Composition Matters

### Hard 16 vs. 10 (The Most Important CDS)

This is the most famous composition-dependent hand. Basic strategy says "hit 16 vs. 10" but composition matters:

**Two-card 16s:**
| Composition | Contains 10? | Optimal (6-deck) | Optimal (1-deck) |
|------------|-------------|-------------------|-------------------|
| 10+6 | Yes | Hit | Hit (stronger) |
| 9+7 | No | Hit | Hit (barely) |
| 8+8 | No | Split | Split |

**Three-card 16s:**
| Composition | Optimal (6-deck) | Optimal (1-deck) |
|------------|-------------------|-------------------|
| 5+5+6 | Stand | Stand |
| 4+5+7 | Stand | Stand |
| 3+6+7 | Stand | Stand |
| 2+4+10 | Hit | Hit (marginal) |

**Key insight**: When your 16 is composed of 3+ cards, you have likely consumed small cards (reducing their density in the remaining shoe), which means the remaining shoe is richer in 10s. This makes:
- Hitting more dangerous (more 10s to bust you)
- Dealer more likely to bust too (but dealer acts second)

For multi-card 16 vs. 10, standing is often correct because the card removal effect shifts enough probability to make standing marginally better.

**Rule of thumb**: If your 16 vs. 10 contains no 4s or 5s, hit. If it contains a 4 or 5 (indicating you've consumed small cards), stand.

### Hard 12 vs. 4

Basic strategy: Stand. But composition matters:

| Composition | Optimal | Reasoning |
|------------|---------|-----------|
| 10+2 | Hit | The 10 in your hand means fewer 10s in the shoe → less likely to bust. Hit is correct by ~0.005. |
| 9+3 | Stand | Standard composition, stand is correct |
| 8+4 | Stand | 4 is gone, marginally better to stand |
| 7+5 | Stand | 5 is gone, better to stand |
| 6+6 | Split* | Should split 6,6 vs. 4 |

With 10+2 specifically, the removal of a 10 from the shoe reduces bust probability from 30.8% to about 30.5% (6-deck) or 29.4% (single-deck), which is enough to tip this already-borderline hand toward hitting.

### Hard 15 vs. 10

Similar to 16 vs. 10 but less pronounced:

| Composition | Effect |
|------------|--------|
| 10+5 | More inclined to hit (10 removed) |
| 9+6 | Neutral |
| 8+7 | Neutral |
| 5+5+5 | Three 5s consumed → deck is rich in high cards → stand |
| Multi-card 15 with small cards | Lean toward standing |

### Hard 13 vs. 2

This is borderline (margin ~0.003). With composition:
- 10+3 vs. 2: the removed 10 slightly favors hitting → may shift to hit
- 9+4 vs. 2: neutral → stand
- 7+6 vs. 2: neutral → stand

## Effect Magnitude by Deck Count

The composition effect is inversely proportional to shoe size:

| Decks | Typical CDS magnitude (EV shift) |
|-------|----------------------------------|
| 1 | 0.005-0.020 |
| 2 | 0.002-0.010 |
| 6 | 0.001-0.003 |
| 8 | 0.0005-0.002 |

In single-deck, CDS can shift several hands compared to total-dependent strategy. In 6/8-deck, the effect is nearly negligible.

## Total-Dependent vs. Composition-Dependent: How Much Does CDS Help?

### House Edge Reduction from CDS

| Game | Basic Strategy HE | CDS HE | Improvement |
|------|-------------------|---------|-------------|
| Single-deck S17 | 0.17% | 0.02% | 0.15% |
| Double-deck S17 | 0.35% | 0.28% | 0.07% |
| 6-deck S17 | 0.40% | 0.38% | 0.02% |
| 8-deck S17 | 0.43% | 0.42% | 0.01% |

The improvement from CDS is small even in single-deck (~0.15%). For shoe games, it's nearly meaningless.

## Practical CDS Rules

For players who want to apply composition-dependent strategy without memorizing every case:

### Single-Deck CDS Rules

1. **16 vs. 10**: If your 16 consists of 3+ cards, stand. If it's two cards, hit.
2. **12 vs. 4**: If your 12 is 10+2, hit. Otherwise, stand.
3. **12 vs. 3**: If your 12 contains a 10, lean toward hitting even more strongly.
4. **13 vs. 2**: If your 13 is 10+3, consider hitting (very marginal).

### Multi-Deck CDS Rules

Effectively: don't bother. The improvement is less than 0.02% and adds mental overhead that could cause other errors.

## Relationship to Card Counting

CDS is conceptually different from card counting but related:
- **Card counting** tracks the entire shoe composition through a running count
- **CDS** uses only the information in your own hand

A card counter who also applies CDS gains a very small additional edge. In practice, the mental overhead of CDS is better spent on accurate counting and bet sizing.

## Extended CDS: Hand Interaction Effects

In a multi-player game, observing other players' cards before acting provides additional composition information. For example:
- If three other players at the table all show 10-value cards, the remaining shoe is depleted in 10s
- This affects your optimal play for borderline hands

However:
1. Multi-deck shoes minimize this effect
2. The mental overhead of tracking other players' cards is significant
3. The improvement is tiny (<0.01%)

Professional counters gain more from tracking the overall count than from individual card observation.

## CDS vs. Infinite Deck Assumption

The basic strategy tables derived in Tasks 1-3 use the infinite deck assumption (each card drawn doesn't affect future probabilities). This is:
- Exact for continuous shuffling machines (CSM)
- Very close for 6-8 deck shoes (differs by <0.02%)
- Noticeably off for single-deck (differs by 0.1-0.15%)

For shoe games (which are the vast majority of modern blackjack), the infinite-deck basic strategy is essentially correct. CDS corrections are in the noise.

## Conclusion

Composition-dependent strategy is a fascinating theoretical topic that demonstrates the information content in individual card knowledge. However, its practical value is limited:
- **Single-deck**: Worth learning the 3-4 key CDS rules (saves ~0.15%)
- **Multi-deck**: Not worth the effort (saves <0.02%)
- **For card counters**: The count-based deviations (Illustrious 18) already capture most of the composition information that matters
