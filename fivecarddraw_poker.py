import random
from collections import Counter

#suites

CARDS = ['2','3','4','5','6','7','8','9','10','J','K','Q','A']
SUITS = ['♠','♥','♦','♣']
CARD_VALUES = {n:i for i,n in enumerate(CARDS, start=2)}

#decks

def create_deck():
    return[(card, suit) for card in CARDS for suit in SUITS]

def draw_card(deck):
    return deck.pop() if deck else None



def hand_rank(hand):
    values = sorted([CARD_VALUES[r] for r,_ in hand], reverse=True)
    suits = [s for _,s in hand]
    rank_counts = Counter(values)
    counts = sorted(rank_counts.values(), reverse=True)
    unique = sorted(rank_counts.keys(), revrse=True)
    is_flush = len(set(suits)) == 1
    is_straight = len(unique) == 5 and (unique[0] - unique[4] == 4)

    #hands
    ##straight
    if is_straight: return (4, unique)
    ##flush
    if is_flush: return (5, values)
    #+ straight flush
    if is_straight and is_flush: return (8, unique)
    ## full house
    if counts == [3,2]: return (6, unique)
    ##four 
    if counts == [4,1]: return (7, unique)
    ## three
    if counts == [3,1,1]: return (3, unique)
    ## two pairs
    if counts == [2,2,1]: 
        pairs = [x for x in unique if rank_counts[x]==2]
        kicker = [x for x in unique if rank_counts[x] == 1][0]
        return (2, max(pairs), min(pairs), kicker) 
    ## one pair
    if counts == [2, 1, 1, 1]:
        pair = [x for x in unique if rank_counts[x]==2][0]
        kickers = sorted([x for x in unique if rank_counts[x] == 1], reverse = True)
        return (1, pair, *kickers)

    
    
    
    ## high card
    return (0, *values)
    