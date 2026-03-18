import unittest
from fivecarddraw_poker import *
from fivecard_gui import *

class TestHandRank(unittest.TestCase):
    def test_high_card(self):
        hand = [('2','♠'), ('4','♥'), ('7','♣'), ('9','♦'), ('J','♠')]
        self.assertEqual(hand_rank(hand)[0], 0)

    def test_one_pair(self):
        hand = [('2','♠'), ('2','♥'), ('7','♣'), ('9','♦'), ('J','♠')]
        rank = hand_rank(hand)
        self.assertEqual(rank[0], 1)
        self.assertEqual(rank[1], CARD_VALUES['2'])
        self.assertEqual(rank[2:], (CARD_VALUES['J'], CARD_VALUES['9'], CARD_VALUES['7']))

    def test_two_pair(self):
        hand = [('2','♠'), ('2','♥'), ('7','♣'), ('7','♦'), ('J','♠')]
        rank = hand_rank(hand)
        self.assertEqual(rank[0], 2)
        self.assertEqual(rank[1], CARD_VALUES['7'])
        self.assertEqual(rank[2], CARD_VALUES['2'])
        self.assertEqual(rank[3], CARD_VALUES['J'])

    def test_three_kind(self):
        hand = [('2','♠'), ('2','♥'), ('2','♣'), ('7','♦'), ('J','♠')]
        self.assertEqual(hand_rank(hand)[0], 3)

    def test_straight(self):
        hand = [('10','♠'), ('J','♥'), ('Q','♣'), ('K','♦'), ('9','♠')]
        self.assertEqual(hand_rank(hand)[0], 4)

    def test_flush(self):
        hand = [('2','♠'), ('4','♠'), ('7','♠'), ('9','♠'), ('J','♠')]
        self.assertEqual(hand_rank(hand)[0], 5)

    def test_full_house(self):
        hand = [('2','♠'), ('2','♥'), ('2','♣'), ('7','♦'), ('7','♠')]
        self.assertEqual(hand_rank(hand)[0], 6)

    def test_four_kind(self):
        hand = [('2','♠'), ('2','♥'), ('2','♣'), ('2','♦'), ('7','♠')]
        self.assertEqual(hand_rank(hand)[0], 7)

    def test_straight_flush(self):
        hand = [('10','♠'), ('J','♠'), ('Q','♠'), ('K','♠'), ('9','♠')]
        self.assertEqual(hand_rank(hand)[0], 8)

class TestComputerDiscard(unittest.TestCase):
    def test_discard_non_pairs(self):
        hand = [('2','♠'), ('2','♥'), ('7','♣'), ('9','♦'), ('J','♠')]
        discards = computer_discard(hand)
        self.assertEqual(set(discards), {2,3,4})

    def test_keep_all_if_all_pairs(self):
        hand = [('2','♠'), ('2','♥'), ('7','♣'), ('7','♦'), ('7','♠')]
        discards = computer_discard(hand)
        self.assertEqual(discards, [])
    

if __name__ == '__main__':
    unittest.main()