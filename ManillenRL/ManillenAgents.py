import random
import numpy as np

class Agent:

    actions = []
    def __init__(self):
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
                self.actions.append({"suit": suit, "value": value, "rank": rank,"owner":-1})

    def getTroef(self,cards):
        suitScore = [0, 0, 0, 0]
        for card in cards:
            if card["value"] == 7:
                suitScore[card["suit"]] += 15
            elif card["value"] == 6:
                suitScore[card["suit"]] += 14
            elif card["value"] == 5:
                suitScore[card["suit"]] += 13
            elif card["value"] == 4:
                suitScore[card["suit"]] += 12
            elif card["value"] == 3:
                suitScore[card["suit"]] += 11
            else:
                suitScore[card["suit"]] += 10

        return np.argmax(suitScore)

    def setNextState(self,state):
        pass

    def giveReward(self,reward):
        pass

    def saveModel(self,file):
        pass

    def loadModel(self,file):
        pass

class RandomAgent(Agent):
    def getMove(self,moves,state):
        return random.choice(moves)


class FirstMoveAgent(Agent):
    def getMove(self,moves,state):
        return moves[0]
        
class LastMoveAgent(Agent):
    def getMove(self,moves,state):
        return moves[-1]
    

class HighestValueAgent(Agent):
    def getMove(self,moves,state):
        return max(moves,key=lambda x: x["value"])

class LowestValueAgent(Agent):
    def getMove(self,moves,state):
        return min(moves,key=lambda x: x["value"])

class SmartAgent(Agent):
    def getMove(self,moves,state):

        if state["cardsOnTable"] == 0:
            tenCards = [card for card in moves if card["rank"] == 10]
            if len(tenCards) > 0:
                return tenCards[0]
            else:
                return min(moves,key=lambda x: x["value"])

        else:
            if state["teamWinning"]:
                return max(moves,key=lambda x: x["value"])
            else:
                return min(moves,key=lambda x: x["value"])

class SmartAgentV2(Agent):
    def getMove(self,moves,state):

        if state["cardsOnTable"] == 0:
            tenCards = [card for card in moves if card["rank"] == 10]
            if len(tenCards) > 0:
                return tenCards[0]
            else:
                return min(moves,key=lambda x: x["value"])

        else:
            if state["teamWinning"]:
                nonTroef = [move for move in moves if move["suit"] != state["troef"]]
                if len(nonTroef) > 0:
                    return max(nonTroef,key=lambda x: x["value"])
                return max(moves,key=lambda x: x["value"])
            else:
                return min(moves,key=lambda x: x["value"])


class LearningAgent(Agent):
    Qtable = np.zeros((33,33,9,4,4,2,32))
    state = None
    action = None
    nextState = None
    alpha = 0.5
    gamma = 0.5

    def getQActions(self,state):
        return self.Qtable[self.linAction(state["winningCard"])][self.linAction(state["firstCard"])][state["setNumber"]][state["troef"]][state["cardsOnTable"]][int(state["teamWinning"])]

    def linAction(self,action):
        if action == None:
            return 32
        return action["suit"]*8 + action["value"]

    def getMove(self,moves,state):
        QActions = self.getQActions(state)
        bestQValue = -1000000
        bestAction = None
        for move in moves:
            if QActions[self.linAction(move)] > bestQValue:
                bestQValue = QActions[self.linAction(move)]
                bestAction = move
        self.state = state
        self.action = bestAction
        return bestAction

    def setNextState(self,state):
        self.nextState = state
    
    def giveReward(self, reward):
        linAction = self.linAction(self.action)
        self.getQActions(self.state)[linAction] = (1-self.alpha)*self.getQActions(self.state)[linAction] + self.alpha*(reward + self.gamma*np.max(self.getQActions(self.nextState)))
        self.state = None
        self.nextState = None
        self.action = None 

    def saveModel(self,file):
        np.save(file,self.Qtable)

    def loadModel(self,file):
        print("loading model from " + file)
        self.Qtable = np.load(file)
