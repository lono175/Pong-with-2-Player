class StartControl:
    def __init__(self):
        self.isStart = False
        self.playerType = 'SARSA'
        self.isReset = False
    def start(self):
        self.isStart = True
    def stop(self):
        self.isStart = False
    def changePlayer(self, type):
        self.playerType = type
    def reset(self):
        self.isReset = True
def Save(agentList, filename, playerNumber): 
    import pickle
    output = open(filename, 'wb')
    pickle.dump(agentList[playerNumber], output)
    output.close()
def Load(agentList, filename, playerNumber):
    import pickle
    input = open(filename, 'rb')
    agentList[playerNumber] = pickle.load(input)
def ChangeToSARSA(form, agentList, flowMgr):
    agentList[0] = SARSA(float(form['alphaLabel'].value) , float(form['epsilonLabel'].value), float(form['gammaLabel'].value), (-1, 1))
    flowMgr.changePlayer('SARSA')
    flowMgr.reset()

def ChangeToHuman(agentList, flowMgr):
    flowMgr.changePlayer('Human')
    flowMgr.reset()
    
if __name__ == "__main__":
    from SARSA import SARSA
    from PongUI import PongUI
    from Environment import Environment
    from pgu import gui
    import sys,pygame


    app = gui.App()
    form = gui.Form()
    ui = PongUI()

    frame = gui.Container(align=-1,valign=-1)
    frame.add(ui,0,0)
    app.init(frame)

    gameScreenSize = 400, 600
    uiSize = 400, 600
    assert uiSize[1] == gameScreenSize[1]
    screenSize = (gameScreenSize[0] + uiSize[0], gameScreenSize[1])
    gameScreenSize = 400, 400
    discrete_size = 20
    delay = 100
    interval = 50
    action = 0

    pygame.init()
    pygame.key.set_repeat(delay, interval)
    clock=pygame.time.Clock()
    screen = pygame.display.set_mode(screenSize)


    agentList = []
    #agentList.append(SARSA(0.01, 0.1, 0.95, (-1, 1)))
    agentList.append(SARSA(float(form['alphaLabel'].value) , float(form['epsilonLabel'].value), float(form['gammaLabel'].value), (-1, 1)))
    agentList.append(SARSA(float(form['alphaLabel'].value) , float(form['epsilonLabel'].value), float(form['gammaLabel'].value), (-1, 1)))

    start = StartControl()
    ui.setStartListener(start.start)
    ui.setStopListener(start.stop)
    ui.setSaveHandler(lambda filename, playerNumber: Save(agentList, filename, playerNumber))
    ui.setLoadHandler(lambda filename, playerNumber: Load(agentList, filename, playerNumber))

    ui.setPlayerHandler( dict( 
        SARSA= (lambda : ChangeToSARSA(form, agentList, start)),
        Human= (lambda : ChangeToHuman(agentList, start)),
        Q_Learning= (lambda : True)
        ))

    episodeNum = 0
    stepNum = 0

    lastWin = False
    while 1:
        agent = agentList[0]
        agentEnemy = agentList[1]
        env = Environment(gameScreenSize, discrete_size)
        state = env.start(lastWin)

        if start.playerType == 'Human':
           action = 0
        else:
           action = agent.start(state)

        actionEnemy = agentEnemy.start(state)

        episodeNum += 1
        start.isReset = False
        while 1:

            #remove me
            agent = agentList[0]
            agentEnemy = agentList[1]

            #update game status here
            form['stepLabel'].value = stepNum
            form['episodeLabel'].value = episodeNum
            #clock.tick(1000)
            clock.tick(float(form['fpsLabel'].value))
            for event in pygame.event.get():
               if start.playerType == 'Human':
                  action = 0
               if event.type == pygame.QUIT: sys.exit()
               elif event.type==pygame.KEYDOWN and start.playerType == 'Human':
                    if event.key==pygame.K_LEFT:
                        action = -1
                    if event.key==pygame.K_RIGHT:
                        action = 1
               else:
                    app.event(event)
            screen.blit(env.getScreen(), (uiSize[0], 0))
            app.paint(screen)
            #print reward
            #print state
            #print isTerminal
            pygame.display.flip()
            if start.isReset:
                break
            if start.isStart:
                (reward, state, isTerminal) = env.step(action, actionEnemy)
                #print state

                if reward > 0:
                    lastWin = True
                    form['player1Score'].value = 1 + int(form['player1Score'].value) 
                elif reward < 0:
                    lastWin = False
                    form['player2Score'].value = 1 + int(form['player2Score'].value)

                if start.playerType != 'Human':
                    action = agent.step(reward, state)

                actionEnemy = agentEnemy.step(-reward, state)
                stepNum += 1
                if isTerminal:
                    agent.end(reward)
                    agentEnemy.end(-reward)
                    break

