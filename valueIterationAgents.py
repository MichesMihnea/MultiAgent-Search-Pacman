# valueIterationAgents.py
# -----------------------
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



import mdp, util, copy

from learningAgents import ValueEstimationAgent


class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0

        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        #mdp este procesul de decizii, care este cunoscut (spre deosebire de q learning,
        #unde nu este cunoscut modelul
        for iteration in range(iterations): #se itereaza de iterations ori
            currentStepValues = self.values.copy() #valorile Q ale pasului curent, deci mereu in pasul k + 1 se porneste cu valorile din pasul k
            for nextState in mdp.getStates(): #toata lista de stari posibile, in cazul nostru toate patratele de pe harta
                if mdp.isTerminal(nextState):#starea terminala nu isi mai schimba valoarea Q
                    continue
                currentStepValues[nextState] = self.computeQValueFromValues(nextState, self.computeActionFromValues(nextState))#update la valori, defapt singura operatie dintr-o iteratie
                #se recalculeaza valoarea q a acestei stari in functie de valoarea precedenta
                #print("VALUE IS: ")  # sa vedem frumos ce se intampla
                #print(currentStepValues[nextState])
            self.values = currentStepValues.copy()#salvam valorile noi


    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        actionProbabilityPair = self.mdp.getTransitionStatesAndProbs(state, action)#toate tranzitiile posibile cu probabilitatile lor in starea curenta
        currentQValue = 0.0
        for nextState, probability in actionProbabilityPair:
            currentQValue += probability * (#formula aia nasoala de la reinforcement
                        self.mdp.getReward(state, action, nextState) + self.discount * self.getValue(nextState))
        return currentQValue

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"

        if self.mdp.isTerminal(state):#nu mai avem actiuni
            return None

        else:
            #QValues = util.Counter()
            actions = self.mdp.getPossibleActions(state)#toate actiunile posibile in starea asta
            #for action in actions:
            #    QValues[action] = self.computeQValueFromValues(state, action)#se calculeaza valorile Q pentru aceste actiuni
            #si se alege actiunea care da valoarea Q maxima
            #return QValues.argMax()
            #sau varianta b
            valueActionPairs = []
            for legalAction in actions:
                valueActionPairs.append((self.getQValue(state, legalAction), legalAction))
            # lista cu toate actiunile si valorile lor q
            for valueActionPair in valueActionPairs:
            # cauta actiunea cu valoarea q maxima
                if valueActionPair == max(valueActionPairs):
                    maxActionPair = valueActionPair

            # returneaza doar actiunea cu valoarea q maxima
            return maxActionPair[1]



    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
