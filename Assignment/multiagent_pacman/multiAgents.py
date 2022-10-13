# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from calendar import c
from matplotlib.pyplot import close
from util import manhattanDistance
from game import Directions
import random
import util
import numpy as np

from game import Agent


class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(
            gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(
            len(scores)) if scores[index] == bestScore]
        # Pick randomly among the best
        chosenIndex = random.choice(bestIndices)

        "Add more of your code here if you wajnt to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [
            ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        # return successorGameState.getScore()
        food = currentGameState.getFood()
        currentPos = list(successorGameState.getPacmanPosition())
        distance = float("-Inf")

        foodList = food.asList()

        if action == 'Stop':
            return float("-Inf")

        for state in newGhostStates:
            if state.getPosition() == tuple(currentPos) and (state.scaredTimer == 0):
                return float("-Inf")

        for x in foodList:
            tempDistance = -1 * (manhattanDistance(currentPos, x))
            if (tempDistance > distance):
                distance = tempDistance

        return distance


def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn='betterEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()
        def alphabeta(state):
            bestValue, bestAction = None, None
            # print(state.getLegalActions(0))
            value = []
            for action in state.getLegalActions(0):
                if action != 'Stop':
                    #value = max(value,minValue(state.generateSuccessor(0, action), 1, 1))
                    succ = minValue(state.generateSuccessor(0, action), 1, 1)
                    value.append(succ)
                    if bestValue is None:
                        bestValue = succ
                        bestAction = action
                    else:
                        if succ > bestValue:
                            bestValue = succ
                            bestAction = action
            # print(value,'||',bestAction)
            return bestAction

        def minValue(state, agentIdx, depth):
            if agentIdx == state.getNumAgents():
                return maxValue(state, 0, depth + 1)
            value = None
            for action in state.getLegalActions(agentIdx):
                succ = minValue(state.generateSuccessor(
                    agentIdx, action), agentIdx + 1, depth)
                if value is None:
                    value = succ
                else:
                    value = min(value, succ)

            if value is not None:
                return value
            else:
                return self.evaluationFunction(state)

        def maxValue(state, agentIdx, depth):
            if depth > self.depth:
                return self.evaluationFunction(state)
            value = None
            for action in state.getLegalActions(agentIdx):
                succ = minValue(state.generateSuccessor(
                    agentIdx, action), agentIdx + 1, depth)
                if value is None:
                    value = succ
                else:
                    value = max(value, succ)

            if value is not None:
                return value
            else:
                return self.evaluationFunction(state)

        action = alphabeta(gameState)

        return action

        # def minimax_search(state, agentIndex, depth):
        #     # if in min layer and last ghost
        #     if agentIndex == state.getNumAgents():
        #         # if reached max depth, evaluate state
        #         if depth == self.depth:
        #             return self.evaluationFunction(state)
        #         # otherwise start new max layer with bigger depth
        #         else:
        #             return minimax_search(state, 0, depth + 1)
        #     # if not min layer and last ghost
        #     else:
        #         moves = state.getLegalActions(agentIndex)
        #         # if nothing can be done, evaluate the state
        #         if len(moves) == 0:
        #             return self.evaluationFunction(state)
        #         # get all the minimax values for the next layer with each node being a possible state after a move
        #         next = (minimax_search(state.generateSuccessor(agentIndex, m), agentIndex + 1, depth) for m in moves)

        #         # if max layer, return max of layer below
        #         if agentIndex == 0:
        #             return max(next)
        #         # if min layer, return min of layer below
        #         else:
        #             return min(next)
        # # select the action with the greatest minimax value
        # result = max(gameState.getLegalActions(0), key=lambda x: minimax_search(gameState.generateSuccessor(0, x), 1, 1))

        # return result


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def performAlphaBeta(self, depth, agentIndex, gameState, a, b):
        alpha = a
        beta = b

        if (gameState.isWin() or gameState.isLose() or depth > self.depth):
            return self.evaluationFunction(gameState)

        retList = []  # RM: stores the return value for this node actions
        todo = gameState.getLegalActions(agentIndex)  # Store the actions
        if Directions.STOP in todo:
            todo.remove(Directions.STOP)

        for action in todo:
            successor = gameState.generateSuccessor(agentIndex, action)
            if((agentIndex+1) >= gameState.getNumAgents()):
                ret = self.performAlphaBeta(depth+1, 0, successor, alpha, beta)
            else:
                ret = self.performAlphaBeta(
                    depth, agentIndex+1, successor, alpha, beta)

            # print "ret: ",ret," ,agent: ", agentIndex, " , depth: ", depth, "alpha: ", alpha, " , beta: ", beta
            if(agentIndex == 0 and ret > beta):
                return ret
            if (agentIndex > 0 and ret < alpha):
                return ret

            if (agentIndex == 0 and ret > alpha):
                alpha = ret

            if (agentIndex > 0 and ret < beta):
                beta = ret

            retList += [ret]
        if agentIndex == 0:
            if(depth == 1):  # if back to root, return action, else retList value
                maxscore = max(retList)
                length = len(retList)
                for i in range(length):
                    if (retList[i] == maxscore):
                        return todo[i]
            else:
                retVal = max(retList)

        elif agentIndex > 0:  # ghosts
            retVal = min(retList)

        return retVal

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        pacmanIndex = 0
        return self.performAlphaBeta(1, pacmanIndex, gameState, -99999, 99999)


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()
        # Format of result = [action, score]
        action, score = self.get_value(gameState, 0, 0)

        return action

    def get_value(self, gameState, index, depth):
        """
        Returns value as pair of [action, score] based on the different cases:
        1. Terminal state
        2. Max-agent
        3. Expectation-agent
        """
        # Terminal states:
        if len(gameState.getLegalActions(index)) == 0 or depth == self.depth:
            return "", self.evaluationFunction(gameState)

        # Max-agent: Pacman has index = 0
        if index == 0:
            return self.max_value(gameState, index, depth)

        # Expectation-agent: Ghost has index > 0
        else:
            return self.expected_value(gameState, index, depth)

    def max_value(self, gameState, index, depth):
        """
        Returns the max utility value-action for max-agent
        """
        legalMoves = gameState.getLegalActions(index)
        max_value = float("-inf")
        max_action = ""
        if Directions.STOP in legalMoves:
            legalMoves.remove(Directions.STOP)
        for action in legalMoves:
            successor = gameState.generateSuccessor(index, action)
            successor_index = index + 1
            successor_depth = depth

            # Update the successor agent's index and depth if it's pacman
            if successor_index == gameState.getNumAgents():
                successor_index = 0
                successor_depth += 1

            current_action, current_value = self.get_value(
                successor, successor_index, successor_depth)

            if current_value > max_value:
                max_value = current_value
                max_action = action

        return max_action, max_value

    def expected_value(self, gameState, index, depth):
        """
        Returns the max utility value-action for max-agent
        """
        legalMoves = gameState.getLegalActions(index)
        expected_value = 0
        expected_action = ""

        # Find the current successor's probability using a uniform distribution
        successor_probability = 1.0 / len(legalMoves)
        if Directions.STOP in legalMoves:
            legalMoves.remove(Directions.STOP)
        for action in legalMoves:
            successor = gameState.generateSuccessor(index, action)
            successor_index = index + 1
            successor_depth = depth

            # Update the successor agent's index and depth if it's pacman
            if successor_index == gameState.getNumAgents():
                successor_index = 0
                successor_depth += 1

            # Calculate the action-score for the current successor
            current_action, current_value = self.get_value(
                successor, successor_index, successor_depth)

            # Update expected_value with the current_value and successor_probability
            expected_value += successor_probability * current_value

        return expected_action, expected_value


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    # util.raiseNotDefined()
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newCapsules = currentGameState.getCapsules()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    closestGhost = min([manhattanDistance(newPos, ghost.getPosition())
                       for ghost in newGhostStates])
    if newCapsules:
        closestCapsule = min([manhattanDistance(newPos, caps)
                             for caps in newCapsules])
    else:
        closestCapsule = 0

    if closestCapsule:
        closest_capsule = -3 / closestCapsule
    else:
        closest_capsule = 100

    if closestGhost:
        ghost_distance = -2 / closestGhost
    else:
        ghost_distance = -500

    foodList = newFood.asList()
    if foodList:
        closestFood = min([manhattanDistance(newPos, food)
                          for food in foodList])
    else:
        closestFood = 0

    return -2 * closestFood + ghost_distance - 10 * len(foodList) + closest_capsule


def EvaluationFunction(currentGameState):
   
    game_score = currentGameState.getScore()
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newCapsules = currentGameState.getCapsules()
    closestGhost = min([manhattanDistance(newPos, ghost.getPosition())
                       for ghost in newGhostStates])

    if newCapsules:
        closestCapsule = min([manhattanDistance(newPos, caps)
                             for caps in newCapsules])
    else:
        closestCapsule = 0

    if closestCapsule:
        closest_capsule_score = 3 / closestCapsule
    else:
        closest_capsule_score = 100

    ghost_score = 0
    for ghost in newGhostStates:
        ghost_distance = manhattanDistance(newPos, ghost.getPosition())
        if ghost.scaredTimer == 0:
            if ghost_distance:
                ghost_score += -2 / ghost_distance
            else:
                ghost_score += -1000
        else:
            if closestGhost:
                ghost_score += 20 / ghost_distance
            else:
                ghost_score += 500

    foodList = newFood.asList()
    if foodList:
        closestFood = min([manhattanDistance(newPos, food)
                          for food in foodList])
    else:
        closestFood = 0

    return 20*game_score - 2 * closestFood + ghost_score - 10 * len(foodList) + closest_capsule_score


# Abbreviation
better = betterEvaluationFunction
