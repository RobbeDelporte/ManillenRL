from ManillenEnv import manillenEnviroment
from ManillenAgents import *



learningIterations = 0
evaluationIterations = 100

p0 = SimpleLearningAgent()
p1 = SmartAgentV2()
p2 = SimpleLearningAgent()
p3 = SmartAgentV2()

players = [p0,p1,p2,p3]

# team0 = LearningAgent()
# team1 = SmartAgentV2()

# players = [team0,team1,team0,team1]

me = manillenEnviroment()


for i in range(learningIterations):
    troef = i%4 

    seed = random.random()
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
            players[currentPlayer].addNextState(me.getObservationState(currentPlayer))

            if reward != None:
                players[(winner+0)%4].giveReward(reward)
                players[(winner+1)%4].giveReward(-1*reward)
                players[(winner+2)%4].giveReward(reward)
                players[(winner+3)%4].giveReward(-1*reward)

    if i%2000 == 0:
        print(f"learning: {i}/{learningIterations}")


# for player in players:
#     player.saveModel()

print("LEARNING DONE!")


team1CumulativePoints = 0
team2CumulativePoints = 0

for i in range(evaluationIterations):
    troef = i%4 

    seed = random.random()
    for shift in range(0,4):
        me.reset(seed,shift)
        me.setTroef(troef)
        done = False
        while not done:
            currentPlayer = me.playerTurn
            allMoves = me.getLegalActions(currentPlayer)
            state = me.getObservationState(currentPlayer)
            move = players[currentPlayer].getMove(allMoves,state)
            done, team1reward, team2reward = me.step(move)

        team1Points, team2Points = me.getScores()
        team1CumulativePoints += team1Points
        team2CumulativePoints += team2Points

    if i%2000 == 0:
        print(f"evaluating: {i}/{evaluationIterations}")

print("ALL ITERATIONS DONE")
print(f"Final Score: {team1CumulativePoints} | {team2CumulativePoints}")
print(f'Score percentile: {team1CumulativePoints/(team1CumulativePoints+team2CumulativePoints)*100}%')






