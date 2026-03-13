"""
Blackjack Basic Strategy Research Engine

Combinatorial analysis and Monte Carlo simulation for blackjack strategy validation.
Uses Python standard library only (no numpy, no external packages).

Author: Claude Opus 4.6 (autoresearch)
"""

import random
import itertools
import math
from collections import defaultdict
from fractions import Fraction

# =============================================================================
# CONSTANTS
# =============================================================================

# Card values: 2-10, J=Q=K=10, A=11 (or 1)
# In an infinite deck model, each rank 2-9 has probability 1/13,
# and 10-value cards (10,J,Q,K) have probability 4/13.
RANKS = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]  # 11 = Ace
RANK_PROBS_INF = {}  # infinite deck probabilities
for r in range(2, 10):
    RANK_PROBS_INF[r] = 1.0 / 13.0
RANK_PROBS_INF[10] = 4.0 / 13.0
RANK_PROBS_INF[11] = 1.0 / 13.0

# Dealer upcard labels
UPCARDS = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

# =============================================================================
# HAND UTILITIES
# =============================================================================

def hand_value(cards):
    """Calculate the best blackjack value of a hand.
    Returns (total, is_soft) where is_soft means an Ace is counted as 11."""
    total = sum(cards)
    aces = cards.count(11)
    soft = aces > 0
    while total > 21 and aces > 0:
        total -= 10
        aces -= 1
    soft = aces > 0
    return total, soft


def is_bust(cards):
    total, _ = hand_value(cards)
    return total > 21


def is_blackjack(cards):
    """Natural blackjack: exactly 2 cards totaling 21."""
    return len(cards) == 2 and hand_value(cards)[0] == 21


# =============================================================================
# SHOE / DECK MANAGEMENT
# =============================================================================

def make_shoe(num_decks=6):
    """Create a shoe with the given number of decks."""
    deck = []
    for _ in range(num_decks):
        for rank in [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]:
            deck.append(rank)
    random.shuffle(deck)
    return deck


def remaining_probs(shoe_counts, total_remaining):
    """Given counts of each card value remaining, return probability dict."""
    probs = {}
    for val in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]:
        probs[val] = shoe_counts.get(val, 0) / total_remaining if total_remaining > 0 else 0
    return probs


def infinite_deck_probs():
    """Return infinite deck probabilities (no removal effects)."""
    return dict(RANK_PROBS_INF)


# =============================================================================
# DEALER OUTCOME PROBABILITIES (COMBINATORIAL)
# =============================================================================

def dealer_probs(upcard, card_probs=None, stands_soft_17=True):
    """
    Calculate exact dealer final total probabilities using combinatorial analysis.

    upcard: dealer's face-up card value (2-11)
    card_probs: dict of card value -> probability of drawing that card
    stands_soft_17: True = S17 (stand on soft 17), False = H17 (hit soft 17)

    Returns dict: {17: p, 18: p, 19: p, 20: p, 21: p, 'bust': p}
    """
    if card_probs is None:
        card_probs = infinite_deck_probs()

    # State: (hard_total, num_aces_as_11)
    # We track the hand state and accumulate final probabilities
    results = {17: 0.0, 18: 0.0, 19: 0.0, 20: 0.0, 21: 0.0, 'bust': 0.0}

    def _recurse(total, soft_aces, prob):
        """Recursively calculate dealer outcomes."""
        # Calculate effective total
        effective = total
        sa = soft_aces
        while effective > 21 and sa > 0:
            effective -= 10
            sa -= 1

        is_soft = sa > 0

        if effective > 21:
            results['bust'] += prob
            return

        # Dealer stands on 17+ (with S17/H17 rule)
        if effective > 17:
            results[effective] += prob
            return
        if effective == 17:
            if stands_soft_17 or not is_soft:
                results[17] += prob
                return
            # H17: dealer hits soft 17, fall through to draw

        # Dealer must hit
        for card_val, card_prob in card_probs.items():
            if card_prob <= 0:
                continue
            new_total = total + card_val
            new_soft = soft_aces + (1 if card_val == 11 else 0)
            _recurse(new_total, new_soft, prob * card_prob)

    # Initial state: dealer has the upcard
    init_soft = 1 if upcard == 11 else 0
    _recurse(upcard, init_soft, 1.0)

    return results


def dealer_probs_with_peek(upcard, card_probs=None, stands_soft_17=True):
    """
    Dealer probabilities conditional on NOT having a natural blackjack.
    This is the US rule where dealer peeks at hole card.

    If upcard is 10 or Ace, we condition on the hole card NOT making blackjack.
    """
    if card_probs is None:
        card_probs = infinite_deck_probs()

    results = {17: 0.0, 18: 0.0, 19: 0.0, 20: 0.0, 21: 0.0, 'bust': 0.0}

    if upcard == 11:
        # Dealer shows Ace. Peek: hole card is NOT a 10-value.
        # P(hole != 10) = 1 - 4/13 = 9/13
        p_no_bj = 1.0 - card_probs[10]
        if p_no_bj <= 0:
            return results

        for hole_val, hole_prob in card_probs.items():
            if hole_val == 10:
                continue  # These are blackjacks, excluded
            cond_prob = hole_prob / p_no_bj
            # Now dealer has (Ace, hole_val). Total = 11 + hole_val, soft_aces depends.
            total = 11 + hole_val
            soft_aces = 1 + (1 if hole_val == 11 else 0)
            _recurse_dealer(total, soft_aces, cond_prob, card_probs, stands_soft_17, results)

    elif upcard == 10:
        # Dealer shows 10. Peek: hole card is NOT an Ace.
        p_no_bj = 1.0 - card_probs[11]
        if p_no_bj <= 0:
            return results

        for hole_val, hole_prob in card_probs.items():
            if hole_val == 11:
                continue  # Blackjack, excluded
            cond_prob = hole_prob / p_no_bj
            total = 10 + hole_val
            soft_aces = 0
            _recurse_dealer(total, soft_aces, cond_prob, card_probs, stands_soft_17, results)
    else:
        # No peek needed for other upcards
        return dealer_probs(upcard, card_probs, stands_soft_17)

    return results


def _recurse_dealer(total, soft_aces, prob, card_probs, stands_soft_17, results):
    """Helper for dealer recursion after hole card is known."""
    effective = total
    sa = soft_aces
    while effective > 21 and sa > 0:
        effective -= 10
        sa -= 1

    is_soft = sa > 0

    if effective > 21:
        results['bust'] += prob
        return

    if effective > 17:
        results[effective] += prob
        return
    if effective == 17:
        if stands_soft_17 or not is_soft:
            results[17] += prob
            return

    for card_val, card_prob in card_probs.items():
        if card_prob <= 0:
            continue
        new_total = total + card_val
        new_soft = soft_aces + (1 if card_val == 11 else 0)
        _recurse_dealer(new_total, new_soft, prob * card_prob, card_probs, stands_soft_17, results)


# =============================================================================
# EXPECTED VALUE CALCULATIONS
# =============================================================================

def ev_stand(player_total, dealer_upcard, card_probs=None, s17=True, peek=True):
    """
    EV of standing with player_total vs. dealer upcard.
    Assumes player has NOT busted.
    Returns EV where +1 = win 1 unit, -1 = lose 1 unit, 0 = push.
    """
    if peek:
        dp = dealer_probs_with_peek(dealer_upcard, card_probs, s17)
    else:
        dp = dealer_probs(dealer_upcard, card_probs, s17)

    ev = 0.0
    for dtotal in [17, 18, 19, 20, 21]:
        if player_total > dtotal:
            ev += dp[dtotal]  # player wins
        elif player_total < dtotal:
            ev -= dp[dtotal]  # player loses
        # else push: +0
    ev += dp['bust']  # dealer busts, player wins
    return ev


def ev_hit(player_cards, dealer_upcard, card_probs=None, s17=True, peek=True, depth=0):
    """
    EV of hitting. After hitting, player plays optimally (hit or stand only).
    Uses recursive calculation.

    player_cards: list of card values in player's hand
    """
    if card_probs is None:
        card_probs = infinite_deck_probs()

    ev = 0.0
    for card_val, card_prob in card_probs.items():
        if card_prob <= 0:
            continue
        new_cards = player_cards + [card_val]
        total, soft = hand_value(new_cards)

        if total > 21:
            ev += card_prob * (-1.0)  # bust
        elif total == 21:
            ev += card_prob * ev_stand(21, dealer_upcard, card_probs, s17, peek)
        else:
            # Player can hit or stand — choose best
            ev_s = ev_stand(total, dealer_upcard, card_probs, s17, peek)
            if depth < 10:  # prevent infinite recursion
                ev_h = ev_hit(new_cards, dealer_upcard, card_probs, s17, peek, depth + 1)
                ev += card_prob * max(ev_s, ev_h)
            else:
                ev += card_prob * ev_s

    return ev


def ev_double(player_cards, dealer_upcard, card_probs=None, s17=True, peek=True):
    """
    EV of doubling down. Player gets exactly one more card, bet is doubled.
    Returns EV in terms of the ORIGINAL bet (so multiply result by 1 to compare).
    """
    if card_probs is None:
        card_probs = infinite_deck_probs()

    ev = 0.0
    for card_val, card_prob in card_probs.items():
        if card_prob <= 0:
            continue
        new_cards = player_cards + [card_val]
        total, soft = hand_value(new_cards)

        if total > 21:
            ev += card_prob * (-1.0)  # bust (lose doubled bet)
        else:
            ev += card_prob * ev_stand(total, dealer_upcard, card_probs, s17, peek)

    return ev * 2.0  # doubled bet


def ev_split(pair_card, dealer_upcard, card_probs=None, s17=True, peek=True,
             das=True, resplit=False, max_splits=1):
    """
    EV of splitting a pair. Each split hand gets one card, then plays optimally.

    pair_card: value of the paired card (e.g., 8 for 8,8)
    das: double after split allowed

    Returns EV for BOTH hands combined (so comparable to 1 unit bet on the original hand).
    """
    if card_probs is None:
        card_probs = infinite_deck_probs()

    # EV of a single split hand: start with pair_card + new card
    single_ev = 0.0
    for card_val, card_prob in card_probs.items():
        if card_prob <= 0:
            continue
        hand = [pair_card, card_val]
        total, soft = hand_value(hand)

        if pair_card == 11:
            # Split aces: typically only get one card each
            if total > 21:
                single_ev += card_prob * (-1.0)
            else:
                single_ev += card_prob * ev_stand(total, dealer_upcard, card_probs, s17, peek)
        else:
            # Normal split hand: play optimally
            if total > 21:
                single_ev += card_prob * (-1.0)
            else:
                ev_s = ev_stand(total, dealer_upcard, card_probs, s17, peek)
                ev_h = ev_hit(hand, dealer_upcard, card_probs, s17, peek)

                if das and total in [9, 10, 11]:  # reasonable double totals
                    ev_d = ev_double(hand, dealer_upcard, card_probs, s17, peek)
                    single_ev += card_prob * max(ev_s, ev_h, ev_d)
                else:
                    single_ev += card_prob * max(ev_s, ev_h)

    # Two split hands
    return 2.0 * single_ev


def ev_surrender():
    """EV of surrendering. Player loses half the bet."""
    return -0.5


# =============================================================================
# OPTIMAL ACTION DETERMINATION
# =============================================================================

def best_action_hard(player_total, dealer_upcard, card_probs=None, s17=True, peek=True):
    """Find the best action for a hard total."""
    if card_probs is None:
        card_probs = infinite_deck_probs()

    # Build a representative hand for this total
    # For hard totals, we need cards that sum to the total with no soft ace
    if player_total <= 11:
        cards = [2, player_total - 2] if player_total > 4 else [2, 2]
    elif player_total <= 21:
        cards = [10, player_total - 10]
    else:
        return 'S', {}

    # Adjust for edge cases
    if player_total == 4:
        cards = [2, 2]
    elif player_total == 5:
        cards = [2, 3]

    evs = {}
    evs['S'] = ev_stand(player_total, dealer_upcard, card_probs, s17, peek)
    evs['H'] = ev_hit(cards, dealer_upcard, card_probs, s17, peek)
    evs['D'] = ev_double(cards, dealer_upcard, card_probs, s17, peek)

    best = max(evs, key=evs.get)
    return best, evs


def best_action_soft(ace_plus, dealer_upcard, card_probs=None, s17=True, peek=True):
    """Find the best action for a soft total (Ace + ace_plus)."""
    if card_probs is None:
        card_probs = infinite_deck_probs()

    cards = [11, ace_plus]  # Ace counted as 11
    total = 11 + ace_plus

    evs = {}
    evs['S'] = ev_stand(total, dealer_upcard, card_probs, s17, peek)
    evs['H'] = ev_hit(cards, dealer_upcard, card_probs, s17, peek)
    evs['D'] = ev_double(cards, dealer_upcard, card_probs, s17, peek)

    best = max(evs, key=evs.get)
    return best, evs


def best_action_pair(pair_card, dealer_upcard, card_probs=None, s17=True, peek=True, das=True):
    """Find the best action for a pair."""
    if card_probs is None:
        card_probs = infinite_deck_probs()

    cards = [pair_card, pair_card]
    total, soft = hand_value(cards)

    evs = {}
    evs['S'] = ev_stand(total, dealer_upcard, card_probs, s17, peek)
    evs['H'] = ev_hit(cards, dealer_upcard, card_probs, s17, peek)
    evs['D'] = ev_double(cards, dealer_upcard, card_probs, s17, peek)
    evs['P'] = ev_split(pair_card, dealer_upcard, card_probs, s17, peek, das)

    best = max(evs, key=evs.get)
    return best, evs


# =============================================================================
# FULL TABLE GENERATION
# =============================================================================

def generate_hard_table(card_probs=None, s17=True, peek=True):
    """Generate complete hard totals strategy table."""
    table = {}
    ev_table = {}
    for total in range(5, 22):
        table[total] = {}
        ev_table[total] = {}
        for uc in UPCARDS:
            action, evs = best_action_hard(total, uc, card_probs, s17, peek)
            # Don't recommend double for totals that don't make sense
            if total >= 12 and action == 'D':
                # With 12+, doubling is rarely correct for hard hands
                # But let the math decide
                pass
            table[total][uc] = action
            ev_table[total][uc] = evs
    return table, ev_table


def generate_soft_table(card_probs=None, s17=True, peek=True):
    """Generate complete soft totals strategy table."""
    table = {}
    ev_table = {}
    for kicker in range(2, 10):  # A,2 through A,9
        table[kicker] = {}
        ev_table[kicker] = {}
        for uc in UPCARDS:
            action, evs = best_action_soft(kicker, uc, card_probs, s17, peek)
            table[kicker][uc] = action
            ev_table[kicker][uc] = evs
    return table, ev_table


def generate_pair_table(card_probs=None, s17=True, peek=True, das=True):
    """Generate complete pairs strategy table."""
    table = {}
    ev_table = {}
    for pair_val in [11, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
        table[pair_val] = {}
        ev_table[pair_val] = {}
        for uc in UPCARDS:
            action, evs = best_action_pair(pair_val, uc, card_probs, s17, peek, das)
            table[pair_val][uc] = action
            ev_table[pair_val][uc] = evs
    return table, ev_table


# =============================================================================
# MONTE CARLO SIMULATION
# =============================================================================

def simulate_hand(shoe, player_action_fn, s17=True):
    """
    Simulate a single hand of blackjack.

    shoe: list of card values (will pop from end)
    player_action_fn: function(player_cards, dealer_upcard) -> 'H', 'S', 'D', 'P'
    s17: dealer stands on soft 17

    Returns: net result for player (+1 win, -1 lose, 0 push, +1.5 blackjack)
    """
    if len(shoe) < 15:
        return None  # not enough cards

    # Deal
    player_cards = [shoe.pop(), shoe.pop()]
    dealer_cards = [shoe.pop(), shoe.pop()]
    dealer_upcard = dealer_cards[0]

    # Check for naturals
    player_bj = is_blackjack(player_cards)
    dealer_bj = is_blackjack(dealer_cards)

    if player_bj and dealer_bj:
        return 0.0  # push
    if dealer_bj:
        return -1.0
    if player_bj:
        return 1.5  # 3:2 payout

    # Player's turn
    bet_multiplier = 1.0

    action = player_action_fn(player_cards, dealer_upcard)

    if action == 'D':
        bet_multiplier = 2.0
        player_cards.append(shoe.pop())
    elif action == 'S':
        pass
    else:  # Hit
        while action == 'H':
            player_cards.append(shoe.pop())
            total, _ = hand_value(player_cards)
            if total >= 21:
                break
            action = player_action_fn(player_cards, dealer_upcard)

    player_total, _ = hand_value(player_cards)

    if player_total > 21:
        return -bet_multiplier

    # Dealer's turn
    while True:
        dtotal, dsoft = hand_value(dealer_cards)
        if dtotal > 17:
            break
        if dtotal == 17:
            if s17 or not dsoft:
                break
        dealer_cards.append(shoe.pop())

    dealer_total, _ = hand_value(dealer_cards)

    if dealer_total > 21:
        return bet_multiplier
    elif player_total > dealer_total:
        return bet_multiplier
    elif player_total < dealer_total:
        return -bet_multiplier
    else:
        return 0.0


def run_simulation(num_hands=100000, num_decks=6, s17=True, strategy='basic'):
    """Run a Monte Carlo simulation with the given parameters."""
    results = []
    shoe = make_shoe(num_decks)

    for _ in range(num_hands):
        if len(shoe) < 52:  # reshuffle
            shoe = make_shoe(num_decks)

        if strategy == 'basic':
            action_fn = basic_strategy_action
        elif strategy == 'never_bust':
            action_fn = never_bust_action
        else:
            action_fn = basic_strategy_action

        result = simulate_hand(shoe, action_fn, s17)
        if result is not None:
            results.append(result)

    return results


def basic_strategy_action(player_cards, dealer_upcard):
    """Basic strategy lookup."""
    total, soft = hand_value(player_cards)

    # Simplified basic strategy
    if len(player_cards) == 2 and player_cards[0] == player_cards[1]:
        pair_val = player_cards[0]
        return BASIC_PAIRS.get(pair_val, {}).get(dealer_upcard, 'H')

    if soft:
        kicker = total - 11  # the non-ace part
        if kicker >= 2 and kicker <= 9:
            action = BASIC_SOFT.get(kicker, {}).get(dealer_upcard, 'H')
            if action == 'D' and len(player_cards) > 2:
                action = 'H'  # can't double after initial 2 cards
            return action

    action = BASIC_HARD.get(total, {}).get(dealer_upcard, 'S' if total >= 17 else 'H')
    if action == 'D' and len(player_cards) > 2:
        action = 'H'
    return action


def never_bust_action(player_cards, dealer_upcard):
    """Never bust strategy: stand on 12+."""
    total, _ = hand_value(player_cards)
    if total >= 12:
        return 'S'
    return 'H'


# Basic strategy tables (from program-blackjack.md)
BASIC_HARD = {
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
    18: {2:'S',3:'S',4:'S',5:'S',6:'S',7:'S',8:'S',9:'S',10:'S',11:'S'},
    19: {2:'S',3:'S',4:'S',5:'S',6:'S',7:'S',8:'S',9:'S',10:'S',11:'S'},
    20: {2:'S',3:'S',4:'S',5:'S',6:'S',7:'S',8:'S',9:'S',10:'S',11:'S'},
    21: {2:'S',3:'S',4:'S',5:'S',6:'S',7:'S',8:'S',9:'S',10:'S',11:'S'},
}

BASIC_SOFT = {
    2: {2:'H',3:'H',4:'H',5:'D',6:'D',7:'H',8:'H',9:'H',10:'H',11:'H'},
    3: {2:'H',3:'H',4:'H',5:'D',6:'D',7:'H',8:'H',9:'H',10:'H',11:'H'},
    4: {2:'H',3:'H',4:'D',5:'D',6:'D',7:'H',8:'H',9:'H',10:'H',11:'H'},
    5: {2:'H',3:'H',4:'D',5:'D',6:'D',7:'H',8:'H',9:'H',10:'H',11:'H'},
    6: {2:'H',3:'D',4:'D',5:'D',6:'D',7:'H',8:'H',9:'H',10:'H',11:'H'},
    7: {2:'S',3:'D',4:'D',5:'D',6:'D',7:'S',8:'S',9:'H',10:'H',11:'H'},
    8: {2:'S',3:'S',4:'S',5:'S',6:'S',7:'S',8:'S',9:'S',10:'S',11:'S'},
    9: {2:'S',3:'S',4:'S',5:'S',6:'S',7:'S',8:'S',9:'S',10:'S',11:'S'},
}

BASIC_PAIRS = {
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


# =============================================================================
# REPORTING UTILITIES
# =============================================================================

def format_ev_table(ev_dict, actions=['S', 'H', 'D']):
    """Format EV values for display."""
    parts = []
    for a in actions:
        if a in ev_dict:
            parts.append(f"{a}={ev_dict[a]:+.4f}")
    return ", ".join(parts)


def print_dealer_probs(upcard, s17=True, peek=True):
    """Print dealer outcome probabilities for a given upcard."""
    if peek:
        dp = dealer_probs_with_peek(upcard, None, s17)
    else:
        dp = dealer_probs(upcard, None, s17)

    uc_name = 'A' if upcard == 11 else str(upcard)
    print(f"\nDealer upcard {uc_name} (S17={s17}, peek={peek}):")
    for outcome in [17, 18, 19, 20, 21, 'bust']:
        print(f"  {outcome}: {dp[outcome]:.6f} ({dp[outcome]*100:.2f}%)")
    print(f"  Sum: {sum(dp.values()):.6f}")


# =============================================================================
# HOUSE EDGE CALCULATION
# =============================================================================

def calculate_house_edge(num_hands=500000, num_decks=6, s17=True, strategy='basic'):
    """Calculate house edge via Monte Carlo simulation."""
    results = run_simulation(num_hands, num_decks, s17, strategy)
    total = sum(results)
    edge = -total / len(results)  # negative of player's average result = house edge
    return edge, len(results)


# =============================================================================
# FINITE DECK PROBABILITY CALCULATIONS
# =============================================================================

def finite_deck_probs(num_decks, removed_cards=None):
    """
    Calculate card probabilities for a finite shoe.
    removed_cards: list of card values already dealt
    """
    counts = {}
    for val in [2, 3, 4, 5, 6, 7, 8, 9]:
        counts[val] = 4 * num_decks
    counts[10] = 16 * num_decks  # 10, J, Q, K
    counts[11] = 4 * num_decks   # Aces

    if removed_cards:
        for card in removed_cards:
            counts[card] -= 1

    total = sum(counts.values())
    probs = {}
    for val, count in counts.items():
        probs[val] = count / total if total > 0 else 0
    return probs


# =============================================================================
# MAIN ANALYSIS RUNNER
# =============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("BLACKJACK BASIC STRATEGY RESEARCH ENGINE")
    print("=" * 70)

    # Print dealer probabilities for each upcard
    print("\n\n--- DEALER OUTCOME PROBABILITIES (S17, infinite deck, peek) ---")
    for uc in UPCARDS:
        print_dealer_probs(uc, s17=True, peek=True)

    print("\n\n--- GENERATING HARD TOTALS TABLE ---")
    hard_table, hard_evs = generate_hard_table()

    print(f"\n{'':>5}", end='')
    for uc in UPCARDS:
        uc_name = 'A' if uc == 11 else str(uc)
        print(f"{uc_name:>5}", end='')
    print()

    for total in range(5, 22):
        print(f"{total:>5}", end='')
        for uc in UPCARDS:
            print(f"{hard_table[total][uc]:>5}", end='')
        print()

    print("\n\n--- GENERATING SOFT TOTALS TABLE ---")
    soft_table, soft_evs = generate_soft_table()

    print(f"\n{'':>7}", end='')
    for uc in UPCARDS:
        uc_name = 'A' if uc == 11 else str(uc)
        print(f"{uc_name:>5}", end='')
    print()

    for kicker in range(2, 10):
        print(f"  A,{kicker}:", end='')
        for uc in UPCARDS:
            print(f"{soft_table[kicker][uc]:>5}", end='')
        print()

    print("\n\n--- GENERATING PAIRS TABLE ---")
    pair_table, pair_evs = generate_pair_table()

    pair_order = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    print(f"\n{'':>8}", end='')
    for uc in UPCARDS:
        uc_name = 'A' if uc == 11 else str(uc)
        print(f"{uc_name:>5}", end='')
    print()

    for pv in pair_order:
        label = 'A,A' if pv == 11 else f"{pv},{pv}"
        print(f"  {label:>4}:", end='')
        for uc in UPCARDS:
            print(f"{pair_table[pv][uc]:>5}", end='')
        print()

    print("\n\nDone.")
