from ManillenEnv import manillenEnviroment
from ManillenAgents import *



learningIterations = 0

evaluationIterations = 20000

p1 = SmartAgentV2()
p3 = SmartAgentV2()
p2 = SmartAgentV2()
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

team1CumulativeReward = 0
team2CumulativeReward = 0

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
        team1CumulativeReward += team1Reward
        team2CumulativeReward += team2Reward

    if i%5000 == 0:
        print(f"evaluating: {i}/{evaluationIterations}")

print("ALL ITERATIONS DONE")
print(f"Final Score: {team1CumulativeReward} | {team2CumulativeReward}")
print(f'Score percentile: {team1CumulativeReward/(team1CumulativeReward+team2CumulativeReward)*100}%')