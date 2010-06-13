import sys,pygame
import copy #for copy objects
class Environment:
    def __init__(self, size, discrete_size):
        self.size = self.width, self.height = size
        self.discrete_size = discrete_size
        self.time_scale = 3
        self.stepNum = 0

    def start(self, lastWin):
        self.ball = pygame.image.load("ball.bmp")
        self.ballRect = self.ball.get_rect()
        self.ballRect.x = self.width/2
        self.ballRect.y = self.height/2

        self.bar = pygame.image.load("bar.bmp")
        self.barRect = self.bar.get_rect()
        self.barRect.bottom = self.height
        self.barRect.x = self.width/2

        self.barEnemy = pygame.image.load("bar.bmp")
        self.barEnemyRect = self.barEnemy.get_rect()
        self.barEnemyRect.top = 0
        self.barEnemyRect.x = self.width/2

        self.speed = [0*self.time_scale,2*self.time_scale]
        #self.leftSpeed = [-2*self.time_scale,-2*self.time_scale]
        #self.rightSpeed = [2*self.time_scale,-2*self.time_scale]
        self.straitSpeed = [0*self.time_scale,-3*self.time_scale]

        #self.leftEnemySpeed = [-2*self.time_scale, 2*self.time_scale]
        #self.rightEnemySpeed = [2*self.time_scale, 2*self.time_scale]
        self.straitEnemySpeed = [0*self.time_scale, 3*self.time_scale]

        self.barSpeed = [3*self.time_scale, 0*self.time_scale]
        self.barEnemySpeed = [3*self.time_scale, 0*self.time_scale]

        self.screen = pygame.Surface(self.size)

        if lastWin:
            self.speed = (self.speed[0], -self.speed[1])
        #return self.getState() + (0, 0, 0, 0)
        return self.getState()

    def step(self, action, enemyAction):
        self.stepNum = self.stepNum + 1
        newState = self.updateState(action, enemyAction)
        state = self.getState()
        flag = self.isTerminal()
        reward = self.getReward()
        #reward = calculate reward for newState
        #set observation equal to newState
        #state = newState
        #diffState = self.getDiffSate()
        return reward, state, flag
        #return reward, diffState, flag

    def getReward(self):
        #if self.ballRect.top > self.height:
        if self.ballRect.bottom > self.height:
            return -1000
        elif self.ballRect.top < 0:
            return 1000
        else:
            return 0

    def isTerminal(self):
        if abs(self.getReward()) == 1000:
            return True
        if self.stepNum > 50000:
            return True
        return False

    def getState(self):
        return (self.ballRect.center[0]/self.discrete_size, self.ballRect.center[1]/self.discrete_size, self.barRect.center[0]/self.discrete_size, self.barEnemyRect.center[0]/self.discrete_size)

    def getDiffSate(self):
        state = self.getState()
        diff = state + (self.lastState[0] - state[0],  self.lastState[1] - state[1],  self.lastState[2] - state[2],  self.lastState[3] - state[3])  
        return diff

    def updateState(self, action, enemyAction):
        self.lastState = self.getState();
        if self.ballRect.colliderect(self.barRect):
            if self.ballRect.left < self.barRect.left:
                #self.speed = copy.copy(self.leftSpeed)
                self.speed = [(self.ballRect.center[0] - self.barRect.center[0])/3, self.straitSpeed[1]]
            elif self.ballRect.right > self.barRect.right:
                #self.speed = copy.copy(self.rightSpeed)
                self.speed = [(self.ballRect.center[0] - self.barRect.center[0])/3, self.straitSpeed[1]]
            else:
                self.speed = copy.copy(self.straitSpeed)
        
        if self.ballRect.colliderect(self.barEnemyRect):
            if self.ballRect.left < self.barEnemyRect.left:
                #self.speed = copy.copy(self.leftEnemySpeed)
                self.speed = [(self.ballRect.center[0] - self.barEnemyRect.center[0])/3, self.straitEnemySpeed[1]]
            elif self.ballRect.right > self.barEnemyRect.right:
                #self.speed = copy.copy(self.rightEnemySpeed)
                self.speed = [(self.ballRect.center[0] - self.barEnemyRect.center[0])/3, self.straitEnemySpeed[1]]
            else:
                self.speed = copy.copy(self.straitEnemySpeed)

        if self.ballRect.left < 0 or self.ballRect.right > self.width:
            self.speed[0] = -self.speed[0]

        #if self.ballRect.top < 0:
            #self.speed[1] = -self.speed[1]

        self.ballRect = self.ballRect.move(self.speed)

        #move the bar
        if action == 1:
            self.barRect = self.barRect.move(self.barSpeed) 
        if action == -1:
            self.barRect = self.barRect.move([-self.barSpeed[0], -self.barSpeed[1]]) 

        if enemyAction == 1:
            self.barEnemyRect = self.barEnemyRect.move(self.barEnemySpeed) 
        if enemyAction == -1:
            self.barEnemyRect = self.barEnemyRect.move([-self.barEnemySpeed[0], -self.barEnemySpeed[1]]) 

        #check the bar stays in the boundary
        if self.barRect.right > self.width:
            self.barRect.right = self.width
        if self.barRect.left < 0:
            self.barRect.left = 0

        #check the bar stays in the boundary
        if self.barEnemyRect.right > self.width:
            self.barEnemyRect.right = self.width
        if self.barEnemyRect.left < 0:
            self.barEnemyRect.left = 0



    def getScreen(self):
        white = 255,255,255
        black = 0, 0, 0
        self.screen.fill(black)
        self.screen.blit(self.ball,self.ballRect)
        self.screen.blit(self.bar,self.barRect)
        self.screen.blit(self.barEnemy,self.barEnemyRect)
        return self.screen

if __name__ == "__main__":
    from SARSA import SARSA
    size = 400, 400
    discrete_size = 10
    delay = 100
    interval = 50
    action = 0

    pygame.init()
    pygame.key.set_repeat(delay, interval)
    clock=pygame.time.Clock()
    screen = pygame.display.set_mode(size)


    agent = SARSA(0.01, 0.1, 0.9, (-1, 1))
    agentEnemy = SARSA(0.01, 0.1, 0.9, (-1, 1))

    lastWin = False

    while 1:
        env = Environment(size, discrete_size)
        state = env.start(lastWin)
        action = agent.start(state)
        actionEnemy = agentEnemy.start(state)
        while 1:
            clock.tick(60)
            for event in pygame.event.get():
               #action = 0
               if event.type == pygame.QUIT: sys.exit()
               #if event.type==pygame.KEYDOWN:
                    #if event.key==pygame.K_LEFT:
                        #action = -1
                    #if event.key==pygame.K_RIGHT:
                        #action = 1
            (reward, state, isTerminal) = env.step(action, actionEnemy)
            if reward > 0:
                lastWin = True
            elif reward < 0:
                lastWin = False
            action = agent.step(reward, state)
            actionEnemy = agentEnemy.step(-reward, state)
            screen.blit(env.getScreen(), (0, 0))
            #print reward
            #print state
            #print isTerminal
            pygame.display.flip()
            if isTerminal:
                agent.end(reward)
                break

