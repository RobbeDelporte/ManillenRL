from ManillenEnv import manillenEnviroment
from ManillenAgents import *


trainingIterations = 100
evalutationIterations = 100

# p0 = RandomSearchSimpleOptimalAgent()
# p1 = SmartAgentV2()
# p2 = RandomSearchSimpleOptimalAgent()
# p3 = SmartAgentV2()

# players = [p0,p1,p2,p3]

team0 = RandomSearchSimpleOptimalAgent()
team1 = SmartAgentV2()

players = [team0,team1,team0,team1]

me = manillenEnviroment()

for j in range(trainingIterations):

    team1CumulativePoints = 0
    team2CumulativePoints = 0

    for i in range(evalutationIterations):
        troef = i%4 

        seed = i
        for shift in range(0,4):
            me.reset(seed,shift)
            me.setTroef(troef)  
            done = False
            while not done:
                currentPlayer = me.playerTurn
                allMoves = me.getLegalActions(currentPlayer)
                state = me.getObservationState(currentPlayer)
                move = players[currentPlayer].getMove(allMoves,state)
                done, reward, winner = me.step(move)
        
            team1Points, team2Points = me.getScores()
            team1CumulativePoints += team1Points
            team2CumulativePoints += team2Points

    score = team1CumulativePoints/(team1CumulativePoints+team2CumulativePoints)*100

    team0.giveScore(score)
    team0.randomizeNewQTable()

team0.saveModel()

print("ALL ITERATIONS DONE")
print(f"Best Score: {team0.bestPerformance}")






