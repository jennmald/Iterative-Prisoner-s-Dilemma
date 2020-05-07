#!/usr/bin/env python3
import random

####    Agent CLASS   ####
#       DESCRIPTION      #
# Stores information for #
# agents including probs #
# names, and scores.     #
# Creates clones of obj  #
# Chooses C or D based   #
# on probabilities and   #
# the opponents choice   #
##########################

class Agent:
    ## Initializing all the information needed to declare an agent ##
    def __init__(self, probFirst, probC, probD, name="Agent"):
        self.p1 = probFirst
        self.pC = probC
        self.pD = probD
        self.name = name
        self.gameMemory = [] # game only 
        self.gameScore = 0
        self.tournamentScore = 0

    ## Creates a clone of a given Agent object ##
    def clone(self):
        newAgent = Agent(self.p1, self.pC, self.pD, self.name)
        return newAgent 

    # randomly return "C" with probability p, else return "D"
    def randomCorD(self, p):
        r = random.random()
        if r < p:
            return "C"
        else:
            return "D"
    
    # Picks the value (C,D) based on probabilities and helper method          
    def choose(self, opponent):
        # the game round number (1-based, not 0-based)
        #  can be calculated from the amount of data stored in memory
        currentRoundNumber = len(self.gameMemory) + 1
        if currentRoundNumber == 1:
            return self.randomCorD( self.p1 )
        else: # currentRoundNumber > 1
            previousRoundNumber = currentRoundNumber - 1
            previousRoundMemoryIndex = previousRoundNumber - 1
            opponentChoice = opponent.gameMemory[previousRoundMemoryIndex]
            if opponentChoice == "C":
                return self.randomCorD( self.pC )
            else:
                return self.randomCorD( self.pD )

    #Clears the GAME only, not to use for Tournaments
    def gameClear(self):
        self.gameMemory = []
        self.gameScore = 0

    #Clears the TOURNAMENT only, not to use for games
    def tournamentClear(self):
        self.tournamentScore = 0


####     GAME CLASS   ####
#       DESCRIPTION      #
# Plays a single game.   #
# Computes points earned #
# by each player by      #
# their choices.         #
# ______________________ #
# Updates an agents      #
# game score and memory  #
# in the Agent class     #
##########################
class Game():
    @staticmethod
    def evaluate(myChoice, opponentChoice):
        if myChoice == "C" and opponentChoice == "C":
            return 3
        elif myChoice == "C" and opponentChoice == "D":
            return 0
        elif myChoice == "D" and opponentChoice == "C":
            return 5
        elif myChoice == "D" and opponentChoice == "D":
            return 1
        else:
            return "Error"

    @staticmethod
    def play(agentA, agentB, numRounds):
        agentA.gameClear()
        agentB.gameClear()
        for i in range(1, numRounds+1):
            choiceA = agentA.choose(agentB)
            choiceB = agentB.choose(agentA)
            agentA.gameMemory.append(choiceA)
            agentB.gameMemory.append(choiceB)

            agentA.gameScore += Game.evaluate(choiceA, choiceB)
            agentB.gameScore += Game.evaluate(choiceB, choiceA)


#### AGENTUTILS CLASS ####
#       DESCRIPTION      #
# Extra methods to aid   #
# in the creation and    #
# agent management of    #
# Tournaments and        #
# Evolution              #
##########################
class AgentUtils():
    # if given a dictionary of agent prototypes and counts,
    #  convert to actual list of agents
    @staticmethod
    def convertToAgentList( agentDictList ):
        agentList = []
        for agentDict in agentDictList:
            agent = agentDict["agent"]
            count = agentDict["count"]
            for i in range(0, count):
               agentList.append(agent.clone())
        return agentList

    ## Determines the number of each agent type in a list of agents ##
    @staticmethod
    def agentCounts(playerList):
        agentNames = []
        for agent in playerList:
            if agent.name not in agentNames:
                agentNames.append(agent.name)

        agentCounts = {}
        for name in agentNames:
            agentCounts[name] = 0
        for agent in playerList:
            agentCounts[agent.name] += 1
        return agentCounts       

#### TOURNAMENT CLASS ####
#       DESCRIPTION      #
# Runs a series of games #
# depending on the       #
# population size        #
# ______________________ #
# Updates an agents      #
# tournament score in    #
# the Agent class        #
##########################

class Tournament():
    #runs tournament eliminating repeats and increments the score
    # returns: playerList
    @staticmethod
    def run( playerList ):

        # type checking:
        # if players is a list of dictionaries of agents,
        #  convert to list of agents
        if type( playerList[0] ) is dict:
            playerList = AgentUtils.convertToAgentList( playerList )

        # just in case
        if type( playerList[0] ) is not Agent:
            Exception("Player parameter does not contain agents")

        # shuffle for testing
        random.shuffle( playerList )
        
        for agent in playerList:
            agent.tournamentClear()
            
        for indexA in range(0, len(playerList)):
            for indexB in range(indexA+1, len(playerList)):
                agentA = playerList[indexA]
                agentB = playerList[indexB]
                Game.play(agentA, agentB, 10)
                agentA.tournamentScore += agentA.gameScore
                agentB.tournamentScore +=agentB.gameScore

        debug = False
        if (debug):
            # determine which agent names are present
            agentNames = []
            for agent in playerList:
                if agent.name not in agentNames:
                    agentNames.append(agent.name)

            # count how many of each agent name there is
            agentCounts = {}
            for name in agentNames:
                agentCounts[name] = 0
            for agent in playerList:
                agentCounts[agent.name] += 1
        return playerList


#### EVOLUTION CLASS  ####
#       DESCRIPTION      #
# Runs a series of tour. #
# depending on the       #
# population size        #
# ______________________ #
#                        #
##########################
class Evolution():

    def __init__(self, init_C, init_D, init_TFT):
        self.round = 0
        self.init_C = init_C
        self.init_D = init_D
        self.init_TFT = init_TFT
        
        self.Cpop = init_C
        self.Dpop = init_D
        self.TFTpop = init_TFT

        self.round_history  = []
        self.C_history = [self.init_C]
        self.D_history = [self.init_D]
        self.TFT_history = [self.init_TFT]


    def run( self, agentList, numOfTournaments ):
        # N times:
        for n in range(0, numOfTournaments+1):
            # incrementing the round number #
            self.round_history.append(n)
            # run a tournament with agentList
            agentList = Tournament.run(agentList)
            
            #Count the agents after each tournament here from the agentList
            ###############################################################
            agentCounts = AgentUtils.agentCounts(agentList)

            if 'All-C' in agentCounts:
                self.C_history.append(agentCounts['All-C'])
            else:
                self.C_history.append(0)
                
            if 'All-D' in agentCounts:
                self.D_history.append(agentCounts['All-D'])
            else:
                self.D_history.append(0)
            
            if 'T-F-T' in agentCounts:
                self.TFT_history.append(agentCounts['T-F-T'])
            else:
                self.TFT_history.append(0)
            ###############################################################

            # rank agents by tournament score
            agentList = sorted(agentList, key = lambda x: x.tournamentScore, reverse = True)
            # destroy bottom 50%, clone top 50%
            newAgentList = []
            half = int(len(agentList)/2)
            for agentIndex in range(0, half):
                agent = agentList[agentIndex]
                newAgentList.append( agent )
                newAgentList.append( agent.clone() )
            # set this to be new agent list
            agentList = newAgentList

        # summarize final population at end of evolution process
        return AgentUtils.agentCounts(agentList)
