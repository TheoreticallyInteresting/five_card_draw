import random
from collections import Counter

# suites 
RANKS = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
SUITS = ['♠','♥','♦','♣']
CARD_VALUES = {r:i for i,r in enumerate(RANKS, start=2)}  

# decks
def create_deck():
    return [(rank, suit) for rank in RANKS for suit in SUITS]

def draw_card(deck):
    return deck.pop() if deck else None

# hand evaluation
HAND_NAMES = {
    8: "Straight Flush",
    7: "Four of a Kind",
    6: "Full House",
    5: "Flush",
    4: "Straight",
    3: "Three of a Kind",
    2: "Two Pair",
    1: "One Pair",
    0: "High Card"
}

def hand_rank(hand):
    """Return a tuple comparable"""
    values = sorted([CARD_VALUES[r] for r,_ in hand], reverse=True)
    suits = [s for _,s in hand]
    rank_counts = Counter(values)
    counts = sorted(rank_counts.values(), reverse=True)
    unique = sorted(rank_counts.keys(), reverse=True)

    is_flush = len(set(suits)) == 1
    is_straight = len(unique) == 5 and (unique[0] - unique[4] == 4)

    # highest rank to lowest
    #straight flush
    if is_straight and is_flush:
        return (8, unique)             
    # four
    if counts == [4,1]:
        return (7, unique)   
        # full house
    if counts == [3,2]:
        return (6, unique)  
    # flush
    if is_flush:
        return (5, values)
    # straight
    if is_straight:
        return (4, unique)  
     # three 
    if counts == [3,1,1]:
        return (3, unique)                      # Three of a Kind
    if counts == [2,2,1]:
        # two pair
        pairs = [v for v in unique if rank_counts[v]==2]
        kicker = [v for v in unique if rank_counts[v]==1][0]
        return (2, max(pairs), min(pairs), kicker)
    if counts == [2,1,1,1]:
        # One pair
        pair = [v for v in unique if rank_counts[v]==2][0]
        kickers = sorted([v for v in unique if rank_counts[v]==1], reverse=True)
        return (1, pair, *kickers)
    # high card
    return (0, *values)

def computer_discard(hand):
    """Return list of indices to discard, keeps pairs"""
    values = [CARD_VALUES[r] for r,_ in hand]
    counts = Counter(values)
    discard = []
    for i, (r,_) in enumerate(hand):
        if counts[CARD_VALUES[r]] == 1:
            discard.append(i)
    return discard
