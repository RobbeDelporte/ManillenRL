from matplotlib.pyplot import table
import numpy as np
import random


DEBUG = False

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
    winningPlayer = 0
    firstCard = None
    troef = 0
    done = False


    def reset(self,seed):
        self.team1points = 0
        self.team2points = 0
        self.tableCards = [None,None,None,None]
        self.doneCards = []
        self.playerTurn = 0
        self.setNumber = 0
        self.cardsOnTable = 0
        self.winningCard = None
        self.winningPlayer = 0
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
        
        random.seed()
        random.shuffle(self.allCards)

        for i,card in enumerate(self.allCards):
            card["owner"] = i%4
            self.playerCards[i%4].append(card)

        for player in range(4):
            self.playerCards[player] = sorted(self.playerCards[player],key=lambda x: 13*x["suit"]+x["value"])

    def setTroef(self,troef):
        self.troef = troef
    
    def step(self,card):
        if DEBUG:
            print(f'\nPlayer{card["owner"]} makes move {card}')
        
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
            self.playerTurn = self.winningPlayer
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

    
    def getLegalActionsOfCurrentPlayer(self):
        return self.getLegalMoves(self.playerCards[self.playerTurn])

    def getObservationState(self,player):
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

    def getObservationStateOfCurrentPlayer(self):
        return self.getObservationState(self.playerTurn)
                
    def render(self):
        print("__________________________\n")
        for player in range(4):
            print(f'Player{player}: {len(self.playerCards[player])} cards.')
        print(f'Table: {self.tableCards}')
        print(f'WinningCard: {self.winningCard}')
        print(f'Troef: {self.troef}')
        print(f'SCORE: {self.team1points} | {self.team2points}')


    def getRewards(self):
        if not self.done:
            return -1,-1
        else:
            team1Score = 0
            team2Score = 0
            team1Score = (self.team1points > 30)*(self.team1points - 30)
            team2Score = (self.team2points > 30)*(self.team2points - 30)
            return team1Score,team2Score