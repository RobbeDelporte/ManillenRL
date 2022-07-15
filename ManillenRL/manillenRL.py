from ManillenEnv import manillenEnviroment
from ManillenAgents import *



learningIterations = 0

evaluationIterations = 5000

p0 = SmartAgent()
p1 = SmartAgent()
p2 = SmartAgent()
p3 = SmartAgent()

players1 = [p0,p1,p2,p3]



me = manillenEnviroment()

for i,player in enumerate(players1):
    player.loadModel(f"player{i}.npy")

for i in range(learningIterations):
    troef = i%4 


    players = players1
    me.reset(i)
    me.setTroef(troef)    
    done = False
    while not done:
        currentPlayer = me.playerTurn
        allMoves = me.getLegalActionsOfCurrentPlayer()
        state = me.getObservationStateOfCurrentPlayer()
        move = players[currentPlayer].getMove(allMoves,state)
        done, reward, winner = me.step(move)
        players[currentPlayer].setNextState(me.getObservationState(currentPlayer))
        if reward != None:
            players[winner].giveReward(reward)
            players[(winner+2)%4].giveReward(reward)
            players[(winner+1)%4].giveReward(-1*reward)
            players[(winner+3)%4].giveReward(-1*reward)

    if i%5000 == 0:
        print(f"learning: {i}/{learningIterations}")


for i,player in enumerate(players1):
    player.saveModel(f"player{i}.npy")

print("LEARNING DONE!")

team1CumulativePoints = 0
team2CumulativePoints = 0

for i in range(evaluationIterations):
    troef = i%4 

    for s in range(0,4):

        players = players1
        me.reset(i)
        me.setFirstPlayer(s)
        me.setTroef(troef)    
        done = False
        while not done:
            currentPlayer = me.playerTurn
            allMoves = me.getLegalActionsOfCurrentPlayer()
            state = me.getObservationStateOfCurrentPlayer()
            move = players[currentPlayer].getMove(allMoves,state)
            done, reward, winner = me.step(move)

        team1Points, team2Points = me.getRewards()
        team1CumulativePoints += team1Points
        team2CumulativePoints += team2Points

    if i%5000 == 0:
        print(f"evaluating: {i}/{evaluationIterations}")

print("ALL ITERATIONS DONE")
print(f"Final Score: {team1CumulativePoints} | {team2CumulativePoints}")
print(f'Score percentile: {team1CumulativePoints/(team1CumulativePoints+team2CumulativePoints)*100}%')