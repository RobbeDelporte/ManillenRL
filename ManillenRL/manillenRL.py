from ManillenEnv import manillenEnviroment
from ManillenAgents import *



learningIterations = 40000

evaluationIterations = 20000

p1 = LearningAgent()
p2 = SmartAgentV2()
p3 = LearningAgent()
p4 = SmartAgentV2()

players1 = [p1,p2,p3,p4]



me = manillenEnviroment()

for i in range(learningIterations):
    troef = i%4 

    for s in range(2):

        players = np.roll(players1,s)
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

print("LEARNING DONE")

team1CumulativePoints = 0
team2CumulativePoints = 0

for i in range(evaluationIterations):
    troef = i%4 

    for s in range(2):

        players = np.roll(players1,s)
        me.reset(i)
        me.setTroef(troef)    
        done = False
        while not done:
            currentPlayer = me.playerTurn
            allMoves = me.getLegalActionsOfCurrentPlayer()
            state = me.getObservationStateOfCurrentPlayer()
            move = players[currentPlayer].getMove(allMoves,state)
            done, reward, winner = me.step(move)
        if s == 0:
            team1Reward, team2Reward = me.getRewards()
        else:
            team2Reward, team1Reward = me.getRewards()
        team1CumulativePoints += team1Reward
        team2CumulativePoints += team2Reward

    if i%5000 == 0:
        print(f"evaluating: {i}/{evaluationIterations}")

print("ALL ITERATIONS DONE")
print(f"Final Score: {team1CumulativePoints} | {team2CumulativePoints}")
print(f'Score percentile: {team1CumulativePoints/(team1CumulativePoints+team2CumulativePoints)*100}%')