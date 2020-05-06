# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"

    print "Start:", problem.getStartState()
    #x si y unde incepe pacman

    #print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    #adica si-a dat spawn direct pe mancare, nu am reusit sa o fac sa dea true pana acum



    startDFS = problem.getStartState()
    DFSVisited = []

    #punctul din care incepe cautarea, adica unde si-a dat spawn pacman

    DFStack = util.Stack()
    DFStack.push(([], startDFS))

    #dfs clasic cu stack in care punem varfurile in care se poate ajunge din varful curent
    #aici caram pe stack si lista de miscari pe care le face pacman pentru a ajunge in varful respectiv

    #cat timp nu e goala stiva
    while (not (DFStack.isEmpty())):

        #examinare nod
        actionList, currentNode = DFStack.pop()

        #nod deja vizitat, ramane scos din stiva si sarim peste
        if currentNode in DFSVisited:
            continue

        #am ajuns la goal, se ajunge aici o singura data si se returneaza lista de miscari care a dus aici
        if problem.isGoalState(currentNode):
            return actionList


        #analizam succesorii, adica unde se poate ajunge cu miscari legale din locatia curenta
        #uselessValue e acolo degeaba, ma intereseaza doar urmatorul pas

        for DFSNext, DFSNextAction, uselessValue in problem.getSuccessors(currentNode):

            #lista de miscari care duce la urmatoarea locatie
            DFSNewAction = actionList + [DFSNextAction]

            #merge pe stack urmatoarea locatie
            DFStack.push((DFSNewAction, DFSNext))

        #locatia curenta a fost vizitata in totalitate
        DFSVisited.append(currentNode)

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    #Dam mare copy paste la DFS si schimbam stack in queue si nici ca mai facem altceva
    print "Start:", problem.getStartState()
    # x si y unde incepe pacman

    # print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    # adica si-a dat spawn direct pe mancare, nu am reusit sa o fac sa dea true pana acum

    startBFS = problem.getStartState()
    BFSVisited = []

    # punctul din care incepe cautarea, adica unde si-a dat spawn pacman

    BFSQueue = util.Queue()
    BFSQueue.push(([], startBFS))

    # dfs clasic cu stack in care punem varfurile in care se poate ajunge din varful curent
    # aici caram pe stack si lista de miscari pe care le face pacman pentru a ajunge in varful respectiv

    # cat timp nu e goala stiva
    while (not (BFSQueue.isEmpty())):

        # examinare nod
        actionList, currentNode = BFSQueue.pop()

        # nod deja vizitat, ramane scos din stiva si sarim peste
        if currentNode in BFSVisited:
            continue

        # am ajuns la goal, se ajunge aici o singura data si se returneaza lista de miscari care a dus aici
        if problem.isGoalState(currentNode):
            return actionList

        # analizam succesorii, adica unde se poate ajunge cu miscari legale din locatia curenta
        # uselessValue e acolo degeaba, ma intereseaza doar urmatorul pas

        for BFSNext, BFSNextAction, uselessValue in problem.getSuccessors(currentNode):
            # lista de miscari care duce la urmatoarea locatie
            BFSNewAction = actionList + [BFSNextAction]

            # merge pe stack urmatoarea locatie
            BFSQueue.push((BFSNewAction, BFSNext))

        # locatia curenta a fost vizitata in totalitate
        BFSVisited.append(currentNode)

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    # Dam mare copy paste la BFS si schimbam queue in priorityQueue, cu prioritatea in functie de cost
    print "Start:", problem.getStartState()
    # x si y unde incepe pacman

    # print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    # adica si-a dat spawn direct pe mancare, nu am reusit sa o fac sa dea true pana acum

    startBFS = problem.getStartState()
    BFSVisited = []

    # punctul din care incepe cautarea, adica unde si-a dat spawn pacman

    BFSQueue = util.PriorityQueue()
    BFSQueue.push(([], startBFS, 0), 0)

    # dfs clasic cu stack in care punem varfurile in care se poate ajunge din varful curent
    # aici caram pe stack si lista de miscari pe care le face pacman pentru a ajunge in varful respectiv

    # cat timp nu e goala stiva
    while (not (BFSQueue.isEmpty())):

        # examinare nod
        actionList, currentNode, BFSCost = BFSQueue.pop()

        # nod deja vizitat, ramane scos din stiva si sarim peste
        if currentNode in BFSVisited:
            continue

        # am ajuns la goal, se ajunge aici o singura data si se returneaza lista de miscari care a dus aici
        if problem.isGoalState(currentNode):
            return actionList

        # analizam succesorii, adica unde se poate ajunge cu miscari legale din locatia curenta
        # uselessValue e acolo degeaba, ma intereseaza doar urmatorul pas

        for BFSNext, BFSNextAction, BFSNextCost in problem.getSuccessors(currentNode):
            # lista de miscari care duce la urmatoarea locatie
            BFSNewAction = actionList + [BFSNextAction]

            BFSNewCost = BFSCost + BFSNextCost
            # merge pe stack urmatoarea locatie
            BFSQueue.push((BFSNewAction, BFSNext, BFSNewCost), BFSNewCost)

        # locatia curenta a fost vizitata in totalitate
        BFSVisited.append(currentNode)

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
