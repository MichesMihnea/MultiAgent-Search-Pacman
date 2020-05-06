# qlearningAgents.py
# ------------------
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


from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *

import random,util,math

class QLearningAgent(ReinforcementAgent):
    """
      Q-Learning Agent

      Functions you should fill in:
        - computeValueFromQValues
        - computeActionFromQValues
        - getQValue
        - getAction
        - update

      Instance variables you have access to
        - self.epsilon (exploration prob)
        - self.alpha (learning rate)
        - self.discount (discount rate)

      Functions you should use
        - self.getLegalActions(state)
          which returns legal actions for a state
    """
    def __init__(self, **args):
        "You can initialize Q-values here..."
        ReinforcementAgent.__init__(self, **args)

        "*** YOUR CODE HERE ***"
        #modelul de decizii nu este cunoscut
        #trebuie invatat prin incercari
        self.QValues = util.Counter()  # indexed by state and action

    def getQValue(self, state, action):
        """
          Returns Q(state,action)
          Should return 0.0 if we have never seen a state
          or the Q node value otherwise
        """
        "*** YOUR CODE HERE ***"
        return self.QValues[state, action]

    def computeValueFromQValues(self, state):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        "*** YOUR CODE HERE ***"
        # actiunile legale din starea curenta
        legalActions = self.getLegalActions(state)

        # cerinta spune sa returnam 0.0 in starea terminala
        if len(legalActions) == 0:
            return 0.0

        # toate actiunile legale dau valori Q
        # cea mai mare valoare Q din acestea este valoarea Q a starii curente
        else:
            QValues = []
            #QValues = util.Counter()
            for legalAction in legalActions:
                #if self.getQValue(state, legalAction) > QValue:
                #nu se compara cu if-ul asta, nu stiu de ce, cu max() merge
                QValues.append(self.getQValue(state, legalAction))
        # return the highest value
        return max(QValues)

    def computeActionFromQValues(self, state):
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """
        "*** YOUR CODE HERE ***"
        legalActions = self.getLegalActions(state)  # toate actiunile legale din starea curenta
        # din cerinta se cere sa returnam None daca starea este terminala
        if len(legalActions) == 0:
            return None
        #LEGALEEEEE
        valueActionPairs = []
        #aceeasi problema cu comparatia la max ca si mai sus
        QValues = util.Counter()
        for legalAction in legalActions:
            QValues[legalAction] = self.getQValue(state, legalAction)
        return QValues.argMax()
        #sau varianta b
        #for legalAction in legalActions:
            #valueActionPairs.append((self.getQValue(state, legalAction), legalAction))
            #lista cu toate actiunile si valorile lor q
        #for valueActionPair in valueActionPairs:
            #cauta actiunea cu valoarea q maxima
            #if valueActionPair == max(valueActionPairs):
                #maxActionPair = valueActionPair

        # returneaza doar actiunea cu valoarea q maxima
        #return maxActionPair[1]


    def getAction(self, state):
        """
          Compute the action to take in the current state.  With
          probability self.epsilon, we should take a random action and
          take the best policy action otherwise.  Note that if there are
          no legal actions, which is the case at the terminal state, you
          should choose None as the action.

          HINT: You might want to use util.flipCoin(prob)
          HINT: To pick randomly from a list, use random.choice(list)
        """
        # Pick Action
        legalActions = self.getLegalActions(state)
        epsilon = self.epsilon
        action = None

        #functia din cerinta
        #da TRUE cu probabilitate epsilon
        #if (util.flipCoin(epsilon)):
            #daca da true, ne bagam la random
         #   action = random.choice(legalActions)
        #else:
            #altfel facem si noi ceva gandit
            #la modul facem actiunea cu valoarea Q cea mai mare
        action = self.getPolicy(state)

        return action


    def update(self, state, action, nextState, reward):
        """
          The parent class calls this to observe a
          state = action => nextState and reward transition.
          You should do your Q-Value update here

          NOTE: You should never call this function,
          it will be called on your behalf
        """
        "*** YOUR CODE HERE ***"

        alpha = self.alpha
        oldQValue = self.getQValue(state, action)#valoarea la care facem update, Q(s(t), a(t))
        discount = self.discount
        #valoarea CU care facem update, cu formula de pe wikipedia
        newQValue = (1 - alpha) * oldQValue + alpha * (reward + (discount * self.getValue(nextState)))
        #Q(s(t), a(t)) = newQValue
        self.QValues[state, action] = newQValue


    def getPolicy(self, state):
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        return self.computeValueFromQValues(state)


class PacmanQAgent(QLearningAgent):
    "Exactly the same as QLearningAgent, but with different default parameters"

    def __init__(self, epsilon=0.05,gamma=0.8,alpha=0.2, numTraining=0, **args):
        """
        These default parameters can be changed from the pacman.py command line.
        For example, to change the exploration rate, try:
            python pacman.py -p PacmanQLearningAgent -a epsilon=0.1

        alpha    - learning rate
        epsilon  - exploration rate
        gamma    - discount factor
        numTraining - number of training episodes, i.e. no learning after these many episodes
        """
        args['epsilon'] = epsilon
        args['gamma'] = gamma
        args['alpha'] = alpha
        args['numTraining'] = numTraining
        self.index = 0  # This is always Pacman
        QLearningAgent.__init__(self, **args)

    def getAction(self, state):
        """
        Simply calls the getAction method of QLearningAgent and then
        informs parent of action for Pacman.  Do not change or remove this
        method.
        """
        action = QLearningAgent.getAction(self,state)
        self.doAction(state,action)
        return action


class ApproximateQAgent(PacmanQAgent):
    """
       ApproximateQLearningAgent

       You should only have to overwrite getQValue
       and update.  All other QLearningAgent functions
       should work as is.
    """
    def __init__(self, extractor='IdentityExtractor', **args):
        self.featExtractor = util.lookup(extractor, globals())()
        PacmanQAgent.__init__(self, **args)
        self.weights = util.Counter()

    def getWeights(self):
        return self.weights

    def getQValue(self, state, action):
        """
          Should return Q(state,action) = w * featureVector
          where * is the dotProduct operator
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

    def update(self, state, action, nextState, reward):
        """
           Should update your weights based on transition
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

    def final(self, state):
        "Called at the end of each game."
        # call the super-class final method
        PacmanQAgent.final(self, state)

        # did we finish training?
        if self.episodesSoFar == self.numTraining:
            # you might want to print your weights here for debugging
            "*** YOUR CODE HERE ***"
            pass
