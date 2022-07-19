import random
import numpy as np

class Agent:

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

    def addNextState(self,state):
        pass

    def giveReward(self,reward):
        pass

    def learn(self,state,reward,nextState):
        pass

    def saveModel(self):
        pass

    def loadModel(self):
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

    def saveModel(self):
        np.save("AgentV1.npy",self.Qtable)

    def loadModel(self):
        print("loading model from AgentV1.npy")
        self.Qtable = np.load("AgentV1.npy")

class SimpleLearningAgent(Agent):
    Qtable = np.zeros((4,4,2,32))
    states = []
    actions = []
    nextStates = []
    alpha = 0.5
    gamma = 0.8


    def getQActions(self,state):
        return self.Qtable[state["troef"]][state["cardsOnTable"]][int(state["teamWinning"])]

    def linAction(self,action):
        if action == None:
            return 32
        return action["suit"]*8 + action["value"]

    def getMove(self,moves,state):
        QActions = self.getQActions(state)
        bestQValue = -99999999
        bestAction = None
        for move in moves:
            if QActions[self.linAction(move)] > bestQValue:
                bestQValue = QActions[self.linAction(move)]
                bestAction = move
        self.states.append(state)
        self.actions.append(bestAction)
        return bestAction

    def addNextState(self,state):
        self.nextStates.append(state)
    
    def giveReward(self, reward):
        for i in range(len(self.actions)):
            action = self.actions[i]
            state = self.states[i]
            nextState = self.nextStates[i]
            linAction = self.linAction(action)
            self.getQActions(state)[linAction] = (1-self.alpha)*self.getQActions(state)[linAction] + self.alpha*(reward + self.gamma*np.max(self.getQActions(nextState)))
        self.states = []
        self.nextStates = []
        self.actions = []

    def printStateShort(self,state):
        return f"troef: {state['troef']} cot: {state['cardsOnTable']} tw: {int(state['teamWinning'])}  "
        

    def saveModel(self):
        np.save("SimpleAgentV1.npy",self.Qtable)

    def loadModel(self):
        print("loading model from SimpleAgentV1.npy")
        self.Qtable = np.load("SimpleAgentV1.npy")
        print(self.Qtable.shape)
