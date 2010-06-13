import random
class SARSA:
    def __init__(self, alpha, epsilon, gamma, actionList ):
        self.alpha = alpha
        self.epsilon = epsilon
        self.gamma = gamma
        self.actionList = actionList
        self.Q = {}
    def touch(self, observation, action):
        key = (observation, action)
        if not key in self.Q:
            self.Q[key] = 0 #assign 0 as the initial value
    def selectAction(self, observation):
        #use epsilon-greedy

        if random.random() < self.epsilon:
            #select randomly
            action = self.actionList[int(random.random()*len(self.actionList))]
            self.touch(observation, action)
            return action
        else:
            #select the best action
            v = []
            for action in self.actionList:
                self.touch(observation, action)
                v.append(self.Q[(observation, action)])
            assert len(v) > 0
            m = max(v)
            select = int(random.random()*v.count(m))

            i = 0
            maxCount = 0
            for value in v:
                if value == m:
                    if maxCount == select:
                        action = self.actionList[i]
                        break
                    maxCount = maxCount + 1
                i = i + 1
            return action

    def update(self, lastObservation, lastAction, reward, observation, action):
        newQVal = self.Q[(observation, action)]
        self.updateQ(lastObservation, lastAction, reward, newQVal)
    def updateQ(self, lastObservation, lastAction, reward, newQVal):
        key = (lastObservation, lastAction)
        self.Q[key] = self.Q[key] + self.alpha*(reward + self.gamma * newQVal - self.Q[key])
    def start(self, observation):
        self.lastObservation = observation
        self.lastAction = self.selectAction(observation)
        return self.lastAction
        #for action in actionList:
        #for each action a
        #if highest valued action valueFunction(observation,a)
        #then store a as lastAction
        #return self.lastAction
    def step(self, reward, observation):
        newAction = self.selectAction(observation)
        self.update(self.lastObservation, self.lastAction, reward, observation, newAction)
        self.lastObservation = observation
        self.lastAction = newAction
        return newAction
    def end(self, reward):
        self.updateQ(self.lastObservation, self.lastAction, reward, 0)
    
if __name__ == "__main__":
    
    controller = SARSA(0.5, 0, 0.8, (-1, 1))
    print controller.start((0, 0, 1))
    print controller.Q
    print controller.step(-1, (0, 0, 0))
    print controller.Q
    print controller.step(-1, (0, 0, 0))
    print controller.Q
    print controller.step(-1, (0, 0, 0))
    print controller.Q
    print controller.step(-1, (0, 0, 0))
    print controller.Q
    print controller.step(-1, (0, 0, 0))
    print controller.Q
    print controller.end(1)
    print controller.Q
    import pickle
    output = open('data.pkl', 'wb')
    pickle.dump(controller, output)
    output.close()
    input = open('data.pkl', 'rb')
    ctrl2 = pickle.load(input)
    print "after load"
    print ctrl2.Q
    #pickle.loads(xp)
    #y
    
