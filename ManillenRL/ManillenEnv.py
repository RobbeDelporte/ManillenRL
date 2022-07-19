import numpy as np
import random

class manillenEnviroment:

    SUITS = ["SPADES","DIAMONDS","CLUBS","HEARTS"]

    team1points = 0
    team2points = 0
    allCards = []
    tableCards = [None,None,None,None]
    doneCards = []
    playerTurn = 0
    setNumber = 0
    cardsOnTable = 0
    winningCard = None
    firstCard = None
    troef = 0
    done = False

   
    def reset(self,seed,shift):
        """resets the enviroment. takes a seed and a shift that can be used to ensure fair games, without having to rely on big numbers

        Args:
            seed (Number): The seed used to shuffle the deck
            
            shift (Int): the Shift determining the first player and which portion of the deck gets assigned to which player. eg: when shift = 1 the player n.1 will
            get the first turn and the same cards that player n.0 would have gotten when shift = 0
        """
        self.team1points = 0
        self.team2points = 0
        self.tableCards = [None,None,None,None]
        self.doneCards = []
        self.playerTurn = 0
        self.setNumber = 0
        self.cardsOnTable = 0
        self.winningCard = None
        self.firstCard = None
        self.troef = 0
        self.done = False

        self.playerCards = [[],[],[],[]]

        self.allCards = []
        for suit in range(4):
            for value in range(8):
                if value == 7:
                    rank = 10
                elif value == 6:
                    rank = 1
                elif value > 2:
                    rank = value + 8
                else:
                    rank = value + 7
                self.allCards.append({"suit": suit, "value": value, "rank": rank,"owner":-1})

        random.seed(seed)
        random.shuffle(self.allCards)

        for i,card in enumerate(self.allCards):
            card["owner"] = (i+shift)%4
            self.playerCards[(i+shift)%4].append(card)

        self.playerTurn = shift%4

        for player in range(4):
            self.playerCards[player] = sorted(self.playerCards[player],key=lambda x: 13*x["suit"]+x["value"])

    def setTroef(self,troef):
        """sets the troef of the game. can be used in the future to include troef chosing algorithms.

        Args:
            troef (Int): 0,1,2 or 3 representing SPADES, DIAMONDS, CLUBS or HEARTS
        """
        self.troef = troef
    
    def step(self,card):
        """The step function of the enviroment. Imprtant to note the only player allowed to make a move is the current player AND the only allowed moves are legal ones.
        This is not verified in the step function for performance reasons.

        Args:
            card (Card): The card/move of the current player

        Returns:
            (bool,int,int): Done, SetScore, WinningPlayer
        """

        if self.cardsOnTable == 0:
            self.firstCard = card
            self.winningCard = card
        elif self.cardWins(card):
            self.winningCard = card

        self.playerCards[self.playerTurn].remove(card)
        self.tableCards[self.playerTurn] = card
        self.cardsOnTable += 1

        if self.cardsOnTable < 4:
            self.playerTurn = (self.playerTurn + 1)%4
            return False, None, None
        else:
            setScore = 0
            for tableCard in self.tableCards:
                self.doneCards.append(tableCard)
                if tableCard["value"] > 2:
                    setScore = setScore + (tableCard["value"] - 2)
            self.cardsOnTable = 0
            self.tableCards = [None,None,None,None]
            self.playerTurn = self.winningCard["owner"]
            self.setNumber += 1
            if self.winningCard["owner"] == 0 or self.winningCard["owner"] == 2:
                self.team1points += setScore
            else:
                self.team2points += setScore
            if self.setNumber == 8:
                self.done = True
                return True, setScore, self.winningCard["owner"]
            return False, setScore, self.winningCard["owner"]

    def getLegalMoves(self,cards):
        """gets the legal moves/card of a set of moves/cards implementing the game rules

        Args:
            cards (List<Card>): The set of cards/moves of which to cacultate the legal moves

        Returns:
            List<Card>: A subset of the cards arg determining the legal moves/cards
        """
        if self.cardsOnTable == 0:
            return cards
            
        legalCards = []
        owner = cards[0]["owner"]
        teamWinning = False
        
        if (self.winningCard["owner"] == 0 or self.winningCard["owner"] == 2) and (owner == 0 or owner == 2):
            teamWinning = True
        if (self.winningCard["owner"] == 1 or self.winningCard["owner"] == 3) and (owner == 1 or owner == 3):
            teamWinning = True
        
        if teamWinning:
            for card in cards:
                if self.cardFollowing(card):
                    legalCards.append(card)
            if len(legalCards) > 0:
                return legalCards
            return cards
        else:
            followingCards = []
            winningCards = []
            for card in cards:
                if self.cardFollowing(card) and self.cardWins(card):
                    legalCards.append(card)
                if self.cardFollowing(card):
                    followingCards.append(card)
                if self.cardWins(card):
                    winningCards.append(card)
            if len(legalCards) > 0:
                return legalCards
            if len(followingCards) > 0:
                return followingCards
            if len(winningCards) > 0:
                return winningCards
            return cards
        
    def cardWins(self,card):
        """Checks wheter or not a card would win the current board

        Args:
            card (Card): A card

        Returns:
            Bool: True if the card would win the board false otherwise
        """
        cardTroef = card["suit"] == self.troef
        winningCardTroef = self.winningCard["suit"] == self.troef
        rankHigher = card["value"] > self.winningCard["value"]
        sameSuit = card["suit"] == self.winningCard["suit"]
        
        if cardTroef and not(winningCardTroef):
            return True
        if cardTroef and winningCardTroef and rankHigher:
            return True
        if sameSuit and rankHigher:
            return True
        return False

    def cardFollowing(self,card):
        if card["suit"] == self.firstCard["suit"]:
            return True
        return False

    
    def getLegalActions(self,player):
        """Handy wrapper function for the getLegalMovesfunction
        """
        return self.getLegalMoves(self.playerCards[player])

    def getObservationState(self,player):
        """Returns the state that a player has access to, the observable state.
        Impotant to note: This is NOT the complete observable state only that which current learning agents require

        Args:
            player (Int): The player in question

        Returns:
            State: The state that the player can see
        """
        state = {}

        state["tableCards"] = self.tableCards
        state["firstCard"] = self.firstCard
        state["winningCard"] = self.winningCard
        state["doneCards"] = self.doneCards
        state["setNumber"] = self.setNumber
        state["cardsOnTable"] = self.cardsOnTable
        state["troef"] = self.troef

        teamWinning = False
        if self.cardsOnTable > 0:
            if (self.winningCard["owner"] == 0 or self.winningCard["owner"] == 2) and (player == 0 or player == 2):
                teamWinning = True
            if (self.winningCard["owner"] == 1 or self.winningCard["owner"] == 3) and (player == 1 or player == 3):
                teamWinning = True

        state["teamWinning"] = teamWinning

        return state

    def renderCards(self,cards):
        if cards == None:
            return 'None | '
        if type(cards) == list:
            r = ""
            for c in cards:
                r += self.renderCards(c)
            return r
        return f"{cards['rank']}{self.SUITS[cards['suit']]} | "
                
    def render(self):
        print("__________________________\n")
        print(len(self.playerCards[0]),len(self.playerCards[1]),len(self.playerCards[2]),len(self.playerCards[3]))
        print(f'Table: {self.renderCards(self.tableCards)}')
        print(f'WinningCard: {self.renderCards(self.winningCard)}')
        print(f'Troef: {self.troef}')
        print(f'SCORE: {self.team1points} | {self.team2points}')


    def getScores(self):
        """The rewards of the current set. This function should only be called at the end of a game

        Returns:
            _type_: _description_
        """
        if not self.done:
            return -1,-1
        else:
            team1Score = 0
            team2Score = 0
            team1Score = (self.team1points > 30)*(self.team1points - 30)
            team2Score = (self.team2points > 30)*(self.team2points - 30)
            return team1Score,team2Score