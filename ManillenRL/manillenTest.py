from ManillenEnv import manillenEnviroment
from ManillenAgents import *

p0 = SmartAgentV2()
p1 = SimpleLearningAgent()


me = manillenEnviroment()


for i in range(1000):
    troef = i%4 

    seed = random.random()
    for shift in range(0,1):
        me.reset(seed,shift)
        me.setTroef(troef)
        done = False
        while not done:
            currentPlayer = me.playerTurn
            allMoves = me.getLegalActions(currentPlayer)
            state = me.getObservationState(currentPlayer)
            move0 = p0.getMove(allMoves,state)
            move1 = p1.getMove(allMoves,state)
            if move0 != move1:
                print(move0,move1)
                print(state)
                input()

            done, reward, winner = me.step(move0)