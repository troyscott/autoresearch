# autoresearch: Blackjack Basic Strategy

This is an experiment to have the LLM research and optimize blackjack basic strategy.

## Goal

**Research, validate, and optimize blackjack basic strategy.** Basic strategy is the mathematically optimal set of decisions (hit, stand, double, split) for every possible player hand vs. dealer upcard combination. It is nearly deterministic — there is one correct answer for each situation. Your job is to:

1. Validate every decision in the current strategy tables below
2. Document the mathematical reasoning behind each decision
3. Identify borderline hands where the expected value difference between actions is small
4. Research how rule variations change optimal play
5. Find insights that could improve the strategy or confirm it is already optimal

## Current Basic Strategy Specification

The strategy is defined as three lookup tables. The agent's job is to research, validate, and optimize these.

**Actions:** `H` = Hit, `S` = Stand, `D` = Double Down, `P` = Split

### Hard Totals (no Ace counted as 11)

Player total → Dealer upcard (2-11, where 11=Ace):

```
       2    3    4    5    6    7    8    9   10   11
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
17:    S    S    S    S    S    S    S    S    S    S
18+:   S    S    S    S    S    S    S    S    S    S
```

### Soft Totals (hand contains Ace counted as 11)

```
         2    3    4    5    6    7    8    9   10   11
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
          2    3    4    5    6    7    8    9   10   11
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

## Research Tasks

Work through these systematically. For each task, document your findings clearly.

### Task 1: Validate the Hard Totals Table
For each row (player total 5-21), verify the correct action against each dealer upcard (2-11). The key questions:
- Why do we stand on 12 vs. 4/5/6 but hit vs. 2/3?
- Why is 11 always a double but 10 doesn't double vs. 10 or Ace?
- What is the expected value difference between hitting and standing on 16 vs. 10? (This is the most famous borderline hand.)
- Are there cells where the action changes depending on number of decks?

### Task 2: Validate the Soft Totals Table
- Why does A,7 stand vs. 2 but double vs. 3-6?
- Why doesn't A,8 ever double? (Some strategy charts say double vs. 6 — is this wrong or rule-dependent?)
- What makes soft hands special? (The safety net of the Ace converting from 11 to 1)

### Task 3: Validate the Pairs Table
- Why always split Aces and 8s? What's the EV math?
- Why never split 10s or 5s? (5,5 is treated as hard 10 for doubling)
- Why does 9,9 stand vs. 7 but split vs. other cards?
- How does "Double After Split" (DAS) allowed vs. not allowed change pair decisions?

### Task 4: Rule Variations
Research how each rule variation changes optimal play:
- **H17 vs. S17** (dealer hits soft 17 vs. stands): Which cells change?
- **Number of decks** (1, 2, 4, 6, 8): Which cells are deck-dependent?
- **DAS** (double after split): How does this affect pair splitting decisions?
- **Surrender** (early/late): When should you surrender? What cells would add an `R` action?
- **Peek vs. no-peek** (European no-hole-card rule): How does this change play vs. dealer 10/Ace?

### Task 5: Borderline Hands
Identify all hands where the EV difference between two actions is less than 1%. These are the hands that:
- Casual players get wrong most often
- Card counters deviate from first (the "Illustrious 18")
- Change with rule variations

### Task 6: Card Counting Deviations
Research the most important deviations from basic strategy when counting cards:
- What are the "Illustrious 18" index plays?
- At what true count does 16 vs. 10 switch from hit to stand?
- At what true count does insurance become a positive EV bet?
- How much does counting reduce the house edge?

### Task 7: House Edge Analysis
Document the expected house edge under common rule sets:
- 6-deck, H17, DAS, no surrender: ~0.64%
- 6-deck, S17, DAS, no surrender: ~0.40%
- Single deck, S17, no DAS: ~0.17%
- Vegas Strip typical rules
- Downtown Vegas typical rules
- Online casino typical rules

### Task 8: Common Misconceptions
Research and document the most common mistakes players make:
- Standing on 12 vs. 2 or 3 (should hit)
- Not splitting 8,8 vs. 10 (should split)
- Not doubling soft hands
- Taking insurance
- "Never bust" strategy (always stand on 12+) — what's the actual house edge?

## Experimentation

### What you CAN do
- Research blackjack strategy using your knowledge and reasoning
- Modify strategy tables if you find provably better decisions
- Create documentation files with your findings
- Run simulations if you build them (Python stdlib only)

### What you CANNOT do
- Make up probabilities without showing the math
- Change the rules of blackjack

### The experiment loop

LOOP FOREVER:

1. Pick the next research task from the list above
2. Research it thoroughly — use combinatorial analysis, conditional probability, and expected value calculations
3. Document your findings in a clear, structured format
4. If you find a cell in the strategy tables that should change, explain the math and update the tables above
5. Move to the next task
6. After completing all 8 tasks, go deeper — explore sub-topics, edge cases, and advanced strategy

**NEVER STOP**: Once research has begun, do NOT pause to ask the human if you should continue. The human expects you to work autonomously through all tasks and keep going deeper. If you finish the listed tasks, explore: kelly criterion for bet sizing, composition-dependent strategy, multi-hand correlations, tournament strategy, side bet analysis, or any other blackjack optimization topic.
