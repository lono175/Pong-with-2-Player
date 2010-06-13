class Controller:
    def __init__(self):
        
    def start(self, observation):
        self.lastObservation = observation
        #for action in actionList:
        #for each action a
        #if highest valued action valueFunction(observation,a)
        #then store a as lastAction
        return self.lastAction
    def step(self, reward, observation):
        update(valueFunction, lastObservation, lastAction, reward, observation)
        newAction = selectAction(observation, valueFunction)
        self.lastObservation = observation
        self.lastAction = newAction
        return newAction
    def end(reward):
        update(valueFunction, lastObservation, lastAction, reward)
    



