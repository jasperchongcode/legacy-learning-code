
# value is [0,1), score is [0,12]


# todo need to write definition for cards
#todo need to write a way to define the game
#todo need to write a way to evaluate the best hand/value of hand
# need to write a function like is_flush, is_straight etc.


# can use get index or smth to find the value
RANKS = ('2', '3', '4', '5', '6', '7','8','9','10', 'j', 'q', 'k', 'a')

SUITS = ('h','d','c','s')

# how many decimal places to take values to


# can use the floor to evaluate what type of hand smth is
VALUE_FIGS = 3

class Card:
    """ Abstract class for cards
    cards have 4 suits, and 13 ranks within that suit. the order of this is important
    """
    def __init__(self, rank, suit):
        """precondition, rank in RANKS"""
        self.rank = rank
        self.suit = suit

    def get_value(self) -> int:
        """ for determining highcards."""
        return RANKS.index(self.rank)
    
    def get_rank(self) -> str:
        return self.rank
    
    def get_suit(self) -> str:
        return self.suit
    
class Heart(Card):
    """class for heart cards"""

    def __init__(self, rank):
        super().__init__(rank, 'h')

class Diamond(Card):
    """class for diamond cards"""

    def __init__(self, rank):
        super().__init__(rank, 'd')

class Club(Card):
    """class for clubs cards"""

    def __init__(self, rank):
        super().__init__(rank, 'c')

class Spade(Card):
    """class for spade cards"""

    def __init__(self, rank):
        super().__init__(rank, 's')

#todo need to make sure that a 0 is not returned unless it doesnt exist
#? will need to consider the best high card outside of the pair etc.

class Hand:
    """Used to distinctly rank card combinations, for an undefined hand size"""

    def __init__(self, cards: list[Card]) -> None:
        self.cards = cards

    def get_rank_list(self) -> list[str]:
        return [card.get_rank() for card in self.cards]
    
    def get_heatmap_score(self, heatmap) -> float:
        """gets the score from a heatmap"""
        try: 
            highest_index = len(heatmap) -1-heatmap[::-1].index(True)
            # 1 is added so that it is never 0 unless it doesnt exist
            value = (highest_index+1)/(len(heatmap)+1)
        except ValueError:
            return 0

        return round(value, VALUE_FIGS)

    def add_card(self, card: Card) -> None:
        self.cards.append(card)

    def highcard_value(self) -> float:
        """returns a value from [0,1) of how good the highcard is"""
        if not self.cards: # if there are no cards
            return 0
        
        return round(((max(card.get_value() for card in self.cards)+1)/(len(RANKS)+1)), VALUE_FIGS)

    
    def pair_value(self) -> float:
        """Returns best pair "value" from [0,1).
         iff one pair """
        # as only care about ranks
    
        rank_heatmap = [self.get_rank_list().count(rank) == 2 for rank in RANKS]

        # there is no single pair
        if sum(rank_heatmap) != 1:
            return 0
        # get the index of the highest item with an exact pair in the heatmap
        return self.get_heatmap_score(rank_heatmap)
    
    def two_pair_value(self) -> float:
        """Returns nonzero [0-1) iff there is a two pair"""
        # check there is two pairs
        rank_heatmap = [self.get_rank_list().count(rank) == 2 for rank in RANKS]

        if sum(rank_heatmap) != 2: # check if there are two pairs
            return 0
        
        # get value of the first pair
        score1 = self.get_heatmap_score(rank_heatmap)
        # remove the highest value True
        index = rank_heatmap.index(True)
        updated_heatmap = [True if i==index else False for i, _ in enumerate(rank_heatmap)]
        # get value of second pair

        score2 = self.get_heatmap_score(updated_heatmap)
 
        # as score 1 is more important than score 2, append them
        hand_score = float(str(score1)+str(score2)[2:]) # remove decimal places

        return hand_score

    def trips_value(self) -> float:
        """return the value of a trips hand from [0-1). 0 iff no trips in hand"""

        rank_heatmap = [self.get_rank_list().count(rank) == 3 for rank in RANKS]

        # check if there is one trip
        if sum(rank_heatmap) != 1:
            return 0
        
        hand_score = self.get_heatmap_score(rank_heatmap)

        return hand_score

    def straight_value(self) -> float:
        """Returns straight value [0,1)"""
        # the value of the straight is the same as the highest card in the straight
        # need to determine 5 in a row
        # ace may work top or bottom
        
        # set to remove duplicates
        rank_set = set(self.get_rank_list())
        possible_straights = [[RANKS[i] for i in range(x,x+5)] for x in range(-1, len(RANKS)-4)]
        value = 0

        for straight in possible_straights:
            if set(straight).issubset(rank_set):
                #the highest part of the straight is the last index
                value = (RANKS.index(straight[-1])+1)/(len(RANKS)+1)

        return round(value, VALUE_FIGS)

        


# thoughs: return a number for the highcard, and then squish it from (0,1) and add it so some constant represneting how inherintely good each hand is

class Poker:
    pass

def main():
    cards = [Spade('a'), Diamond('k'), Spade('a'), Diamond('k'), Heart('q'), Club('j')]
    hand = Hand(cards)
    print(hand.straight_value())

if __name__ == '__main__':
    main()