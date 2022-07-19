from ManillenEnv import manillenEnviroment
from ManillenAgents import *



def runSimulations():
    learningIterations = 0
    evaluationIterations = 10000

    p0 = SmartAgent()
    p1 = SmartAgent()
    p2 = SmartAgent()
    p3 = SmartAgent()

    players = [p0,p1,p2,p3]

    me = manillenEnviroment()

    for i,player in enumerate(players):
        player.loadModel(f"player{i}.npy")

    for i in range(learningIterations):
        troef = i%4 


        me.reset(i,0)
        me.setTroef(troef)    
        done = False
        while not done:
            currentPlayer = me.playerTurn
            allMoves = me.getLegalActions(currentPlayer)
            state = me.getObservationState(currentPlayer)
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


    for i,player in enumerate(players):
        player.saveModel(f"player{i}.npy")

    print("LEARNING DONE!")

    team1CumulativePoints = 0
    team2CumulativePoints = 0

    for i in range(evaluationIterations):
        troef = i%4 

        seed = random.random()
        for shift in range(0,4):
            """
                reset makes sure that every every game gets played 4 times where each player gets the firstturn and the the same cards the others got whet they had the first turn
            """
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

        if i%5000 == 0:
            print(f"evaluating: {i}/{evaluationIterations}")

    print("ALL ITERATIONS DONE")
    print(f"Final Score: {team1CumulativePoints} | {team2CumulativePoints}")
    print(f'Score percentile: {team1CumulativePoints/(team1CumulativePoints+team2CumulativePoints)*100}%')


def test():
    me = manillenEnviroment()


    p0 = SmartAgent()
    p1 = SmartAgent()
    p2 = SmartAgent()
    p3 = SmartAgent()

    players = [p0,p1,p2,p3]

    me.reset(0,0)
    me.setTroef(0)
    for playerCards in me.playerCards:
        print(playerCards)
    done = False
    me.render()
    while not done:
        currentPlayer = me.playerTurn
        allMoves = me.getLegalActions(currentPlayer)
        state = me.getObservationState(currentPlayer)
        move = players[currentPlayer].getMove(allMoves,state)
        done, reward, winner = me.step(move)
        me.render()

    team1Points, team2Points = me.getRewards()
    print(team1Points,team2Points)

    me.reset(0,1)
    me.setTroef(0)
    for playerCards in me.playerCards:
        print(playerCards)
    me.render()
    done = False
    while not done:
        currentPlayer = me.playerTurn
        allMoves = me.getLegalActions(currentPlayer)
        state = me.getObservationState(currentPlayer)
        move = players[currentPlayer].getMove(allMoves,state)
        done, reward, winner = me.step(move)
        me.render()
    team1Points, team2Points = me.getRewards()
    print(team1Points,team2Points)



runSimulations()