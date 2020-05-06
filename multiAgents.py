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


from util import manhattanDistance
from game import Directions
import random, util, math

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.python pacman.py -p ReflexAgent -l testClassic
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()
        

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best
        print("NEW STEP\n")

        "Add more of your code here if you want to"

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
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]


        "*** YOUR CODE HERE ***"

        #deci acum sa facem agentul reflex
        #adica e super simplu, nu se gandeste in avans si merge bine cu o singura fantoma
        #la mai multe fantome e mai nasol
        #deci in fiecare etapa a jocului, analizam tabla la momentul prezent
        #functionam asa: in mod normal, pacman vrea sa mearga dupa mancare
        #totusi, daca o fantoma e periculos de aproape, fuge de fantoma
        #cand se indeparteaza de fantoma, merge iar dupa mancare
        #eu nu am folosit newScaredTimes
        
        newGhostPos = successorGameState.getGhostPositions()
        minDistanceGhost = 99999999
        for ghostPos in newGhostPos:
            distance = math.sqrt((newPos[0] - ghostPos[0]) * (newPos[0] - ghostPos[0]) + (newPos[1] - ghostPos[1]) * (newPos[1] - ghostPos[1]))
            if minDistanceGhost > distance:
                minDistanceGhost = distance

        #aici distanta euclideana, am facut asa si dadea maxim, se inlocuieste cu Manhattan ideal
        #am lasat asa deoarece mergea de punctaj maxim

        minDistanceFood = 99999999
        maxDistanceFood = 0
        
        width = 0
        length = 0

        #cu for-urile parcurgem tabla, am facut asa deoarece nu stiam cum sa fac rost de dimensiunile tablei
        #oricum newFood e mare matrice cu harta
        #parcurgem frumos si vedem unde e de mancare, facem distanta minima pana la mancare

        for widthCount in newFood:
            length = 0
            for lengthCount in newFood[width]:
                if newFood[width][length] == True:
                    #aceeasi chestie cu distanta euclideana vs manhattan
                    distance = math.sqrt((newPos[0] - width) * (newPos[0] - width) + (newPos[1] - length) * (newPos[1] - length))
                    if minDistanceFood > distance:
                        if currentGameState.getPacmanPosition() != newPos:
                            minDistanceFood = distance
                        else:
                            minDistanceFood = 99999

                length += 1
            width += 1

        #cum o gandim pe asta
        #daca pacman e langa mancare, adica urmatoarea mutare e pe mancare
        #facem mutarea, adica dam scor maxim
        #dar doar daca nu e fantoma aproape
        if currentGameState.hasFood(newPos[0], newPos[1]):
            if minDistanceGhost > 1:
                return 999999

        #aici e aproape fantoma
        #incarcam sa maximizam distanta pana la fantoma

        if minDistanceGhost <= 1:
            return minDistanceGhost
        else:
            return 9999 - minDistanceFood

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

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
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
        """
        "*** YOUR CODE HERE ***"

        #vrea sa faca mare arbore minmax
        #adica
        #o data muta pacman si dupa ne gandim ce se intampla daca muta toate fantomele optim
        #si cam asta e un nivel
        #tot asa <depth> nivele
        #si evident merge super greu

        return self.build_max_tree(gameState, 0)  # adica start

    def build_max_tree(self, state, depth):

        #aici suntem pe maxim deci il mutam pe pacman

        #verificam daca e gata
        if state.isWin() or state.isLose():
            return state.getScore()

        #ca la problema cu reflex, asta e lista cu actiuni posibile din pozitia curenta
        actions = state.getLegalActions(0)

        # aici cautam scorul maxim

        max_score = -9999.0
        score = max_score

        best_action = Directions.STOP

        # oricum nu se ajunge la asta

        for action in actions:

            #acum la toate actiunile, bagam simulare de mutare de fantoma
            #deci daca sunt 5 mutari viitoare posibile si mai au si fantomele cate 5
            #facem arbore de inneunim

            score = self.build_min_tree(state.generateSuccessor(0, action), depth,
                                   1)  # acum urmeaza constructia arborelui in functie de miscarea asta
            #functia cu build_min_tree o sa returneze si ea o valoare minima proprie cand e gata
            #cand e gata cu recursivitatea adica e facut arborele sub ea
            #ca arborele se construieste de jos in sus

            if score > max_score:  # aici alege maximul dintre minime de scoruri de noduri viitoare
                max_score = score
                best_action = action

        if depth == 0:  # la intoarcere: cand e gata tot tot, trebuie facuta o mutare
            return best_action
        else:
            return max_score  # aici e inca in ghost_agent, adica alt arbore recursiv si trebuie sa isi returneze
                                #scorul curent, din nou zic ca arborele merge de jos in sus


    def build_min_tree(self, state, depth, ghost):
        if state.isLose() or state.isWin():
            return state.getScore()

        next_agent = ghost + 1  # iterare prin agenti, daca urmeaza fantoma atunci ramanem la adancimea curenta, daca e pacman crestem adancimea
        #adica schimbarea intre mod min si mod max se intampla doar cand ajungem la capatul listei / ramanem fara fantome

        if ghost == state.getNumAgents() - 1:  # am ajuns la capatul listei de agenti
            next_agent = 0

        actions = state.getLegalActions(ghost)  # ce poate face fantoma din pozitia curenta, o gandim la fel ca la pacman

        # interesant e scorul cel mai mic, ca suntem pe nivel de min si mutam cu fantoma

        min_score = 9999.0
        score = min_score

        for action in actions:

            if next_agent == 0:  # se termina nivelul min si urmeaza pacman, deci schimbam min -> max

                if depth == self.depth - 1:  # nu e gata arborele dar vrem sa nu dureze 5 minute o miscare

                    score = self.evaluationFunction(state.generateSuccessor(ghost, action))  # evaluare si ceau

                else:

                    score = self.build_max_tree(state.generateSuccessor(ghost, action),
                                           depth + 1)  # ia-o iar de la pacman, adancime + 1, deci min -> max
            else:

                score = self.build_min_tree(state.generateSuccessor(ghost, action), depth,
                                       next_agent)  # mai sunt fantome care trebuie sa mute

            if score < min_score:  # minimul la scoruri
                min_score = score

        return min_score

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        self.PACMAN = 0
        action = self.build_max_tree(gameState, 0, float("-inf"), float("inf"))
        return action

    def build_max_tree(self, state, depth, alpha, beta):

        #aici suntem pe maxim deci il mutam pe pacman

        #verificam daca e gata
        if state.isWin() or state.isLose():
            return state.getScore()

        #ca la problema cu reflex, asta e lista cu actiuni posibile din pozitia curenta
        actions = state.getLegalActions(0)

        # aici cautam scorul maxim

        max_score = -9999.0
        score = max_score

        best_action = Directions.STOP

        # oricum nu se ajunge la asta

        for action in actions:

            #acum la toate actiunile, bagam simulare de mutare de fantoma
            #deci daca sunt 5 mutari viitoare posibile si mai au si fantomele cate 5
            #facem arbore de inneunim

            score = self.build_min_tree(state.generateSuccessor(0, action), depth,
                                   1, alpha, beta)  # acum urmeaza constructia arborelui in functie de miscarea asta
            #functia cu build_min_tree o sa returneze si ea o valoare minima proprie cand e gata
            #cand e gata cu recursivitatea adica e facut arborele sub ea
            #ca arborele se construieste de jos in sus

            if score > max_score:  # aici alege maximul dintre minime de scoruri de noduri viitoare
                max_score = score
                best_action = action

            # urmatoarele 3 linii sunt noi

            alpha = max(alpha, max_score)

            if max_score > beta:
                return max_score

        if depth == 0:  # la intoarcere: cand e gata tot tot, trebuie facuta o mutare
            return best_action
        else:
            return max_score  # aici e inca in ghost_agent, adica alt arbore recursiv si trebuie sa isi returneze
                                #scorul curent, din nou zic ca arborele merge de jos in sus


    def build_min_tree(self, state, depth, ghost, alpha, beta):
        if state.isLose() or state.isWin():
            return state.getScore()

        next_agent = ghost + 1  # iterare prin agenti, daca urmeaza fantoma atunci ramanem la adancimea curenta, daca e pacman crestem adancimea
        #adica schimbarea intre mod min si mod max se intampla doar cand ajungem la capatul listei / ramanem fara fantome

        if ghost == state.getNumAgents() - 1:  # am ajuns la capatul listei de agenti
            next_agent = 0

        actions = state.getLegalActions(ghost)  # ce poate face fantoma din pozitia curenta, o gandim la fel ca la pacman

        # interesant e scorul cel mai mic, ca suntem pe nivel de min si mutam cu fantoma

        min_score = 9999.0
        score = min_score

        for action in actions:

            if next_agent == 0:  # se termina nivelul min si urmeaza pacman, deci schimbam min -> max

                if depth == self.depth - 1:  # nu e gata arborele dar vrem sa nu dureze 5 minute o miscare

                    score = self.evaluationFunction(state.generateSuccessor(ghost, action))  # evaluare si ceau

                else:

                    score = self.build_max_tree(state.generateSuccessor(ghost, action),
                                           depth + 1, alpha, beta)  # ia-o iar de la pacman, adancime + 1, deci min -> max
            else:

                score = self.build_min_tree(state.generateSuccessor(ghost, action), depth,
                                       next_agent, alpha, beta)  # mai sunt fantome care trebuie sa mute

            if score < min_score:  # minimul la scoruri
                min_score = score

            beta = min(beta, min_score)

            if min_score < alpha:
                return min_score

        return min_score

    #dam copy paste de mai sus cu doua if-uri
    #asa nu mai pierde timpul examinand variante pe care oricum nu le va lua




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

        # Aceeasi faza ca la minmax, doar ca in loc sa avem nivel cu min, avem nivel cu medie
        # deci dam frumos copy paste de mai sus

        return self.build_max_tree(gameState, 0)  # adica start

    def build_max_tree(self, state, depth):

        #aici suntem pe maxim deci il mutam pe pacman

        #verificam daca e gata
        if state.isWin() or state.isLose():
            return state.getScore()

        #ca la problema cu reflex, asta e lista cu actiuni posibile din pozitia curenta
        actions = state.getLegalActions(0)

        # aici cautam scorul maxim

        max_score = -9999.0
        score = max_score

        best_action = Directions.STOP

        # oricum nu se ajunge la asta

        for action in actions:

            #acum la toate actiunile, bagam simulare de mutare de fantoma
            #deci daca sunt 5 mutari viitoare posibile si mai au si fantomele cate 5
            #facem arbore de inneunim

            score = self.build_exp_tree(state.generateSuccessor(0, action), depth,
                                   1)  # acum urmeaza constructia arborelui in functie de miscarea asta
            #functia cu build_min_tree o sa returneze si ea o valoare minima proprie cand e gata
            #cand e gata cu recursivitatea adica e facut arborele sub ea
            #ca arborele se construieste de jos in sus

            if score > max_score:  # aici alege maximul dintre mediile de scoruri de noduri viitoare
                max_score = score
                best_action = action

        if depth == 0:  # la intoarcere: cand e gata tot tot, trebuie facuta o mutare
            return best_action
        else:
            return max_score  # aici e inca in ghost_agent, adica alt arbore recursiv si trebuie sa isi returneze
                                #scorul curent, din nou zic ca arborele merge de jos in sus


    def build_exp_tree(self, state, depth, ghost):
        if state.isLose() or state.isWin():
            return state.getScore()

        #aici avem lista pe care bagam media
        expValues = list()
        avg = 0.0

        next_agent = ghost + 1  # iterare prin agenti, daca urmeaza fantoma atunci ramanem la adancimea curenta, daca e pacman crestem adancimea
        #adica schimbarea intre mod medie si mod max se intampla doar cand ajungem la capatul listei / ramanem fara fantome

        if ghost == state.getNumAgents() - 1:  # am ajuns la capatul listei de agenti
            next_agent = 0

        actions = state.getLegalActions(ghost)  # ce poate face fantoma din pozitia curenta, o gandim la fel ca la pacman

        # interesant e scorul cel mai mic, ca suntem pe nivel de medie si mutam cu fantoma

        min_score = 9999.0
        score = min_score

        for action in actions:

            if next_agent == 0:  # se termina nivelul medie si urmeaza pacman, deci schimbam medie -> max

                if depth == self.depth - 1:  # nu e gata arborele dar vrem sa nu dureze 5 minute o miscare

                    score = self.evaluationFunction(state.generateSuccessor(ghost, action))  # evaluare si ceau

                else:

                    score = self.build_max_tree(state.generateSuccessor(ghost, action),
                                           depth + 1)  # ia-o iar de la pacman, adancime + 1, deci medie -> max
            else:

                score = self.build_exp_tree(state.generateSuccessor(ghost, action), depth,
                                       next_agent)  # mai sunt fantome care trebuie sa mute

            #acum sa calculam media la ce avem pana acum si cam atat, returnam
            expValues.append(score)
            avg = 0.0
            for j in range(len(expValues)):
                avg += expValues[int(j)]
            avg /= len(expValues)

        return avg




def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).
      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"

    util.raiseNotDefined()
# Abbreviation
better = betterEvaluationFunction

