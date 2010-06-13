import time
import random
import pygame
from pygame.locals import *
from pgu import gui

class PongUI(gui.Table):
    def __init__(self,**params):
        gui.Table.__init__(self,**params)


        fg = (0,255,255)

        #self.value = 'pp'
        #self.tr()
        #self.tt = gui.Label(value = self.value,color=fg, name='gg')
        #self.td(self.tt,colspan=2)
        
        self.tr()
        self.td(gui.Label("alpha: ",color=fg),align=-1)
        slider = gui.HSlider(10, 0, 100, size=20, width=100, height=16, name='alphaSlider')
        label = gui.Input(value = slider.value/100.0, size=5, name='alphaLabel')
        slider.connect(gui.CHANGE, self.slideChange, label.name, slider, 100.0)
        self.td(label, align=1)
        self.td(slider, colspan=2)

        self.tr()
        self.td(gui.Label("gamma: ",color=fg),align=-1)
        slider = gui.HSlider(90, 0, 100, size=20, width=100, height=16, name='gammaSlider')
        label = gui.Input(value=slider.value/100.0, size=5, name='gammaLabel')
        slider.connect(gui.CHANGE, self.slideChange, label.name, slider, 100.0)
        self.td(label, align=1)
        self.td(slider, colspan=2)

        self.tr()
        self.td(gui.Label("epsilon: ",color=fg),align=-1)
        slider = gui.HSlider(10, 0, 100, size=20, width=100, height=16, name='epsilonSlider')
        label = gui.Input(value=slider.value/100.0, size=5, name='epsilonLabel')
        slider.connect(gui.CHANGE, self.slideChange, label.name, slider, 100.0)
        self.td(label, align=1)
        self.td(slider, colspan=2)

        self.tr()
        self.td(gui.Label("fps: ",color=fg),align=-1)
        slider = gui.HSlider(60, 30, 1000, size=20, width=100, height=16, name='fpsSlider')
        label = gui.Input(value=slider.value, size=5, name='fpsLabel')
        slider.connect(gui.CHANGE, self.slideChange, label.name, slider, 1)
        self.td(label, align=1)
        self.td(slider, colspan=2)


        self.tr()
        self.td(gui.Label("# step: ",color=fg),align=-1)
        label = gui.Input(value=0, size=10, name='stepLabel')
        self.td(label, align=1)

        self.tr()
        self.td(gui.Label("# episode: ",color=fg),align=-1)
        label = gui.Input(value=0, size=10, name='episodeLabel')
        self.td(label, align=1)

        self.tr()
        self.td(gui.Label("Player 1 Score: ",color=fg),align=-1)
        label = gui.Input(value=0, size=10, name='player1Score')
        self.td(label, align=1)

        self.tr()
        self.td(gui.Label("Player 2 Score: ",color=fg),align=-1)
        label = gui.Input(value=0, size=10, name='player2Score')
        self.td(label, align=1)

        self.tr()
        start = gui.Button("Start")
        start.connect(gui.CLICK, self.start)
        self.td(start)

        stop = gui.Button("Stop")
        stop.connect(gui.CLICK, self.stop)
        self.td(stop)

        self.tr()
        self.td(gui.Spacer(0,30))

        self.tr()
        self.td(gui.Label("Player 1 Option: ",color=fg),align=-1)


        #self.tr()
        #self.td(gui.Label("Type: ",color=fg),align=-1)

        self.tr()
        g = gui.Group(name = 'player_type', value='SARSA')
        self.td(gui.Label("  SARSA: ",color=fg),align=-1)
        r = gui.Radio(g,value='SARSA')
        r.connect(gui.CLICK, self.changePlayer, r.value)
        self.td(r)

        self.tr()
        self.td(gui.Label("  Human: ",color=fg),align=-1)
        r = gui.Radio(g,value='Human')
        r.connect(gui.CLICK, self.changePlayer, r.value)
        self.td(r)

        self.tr()
        button = gui.Button("Load")
        button.connect(gui.CLICK, self.load, 'RL-Agent1.txt', 0)
        self.td(button)

        button = gui.Button("Save")
        button.connect(gui.CLICK, self.save, 'RL-Agent1.txt', 0)
        self.td(button)

        #self.tr()
        #self.td(gui.Label("  Q_Learning: ",color=fg),align=-1)
        #r = gui.Radio(g,value='Q_Learning')
        #r.connect(gui.CLICK, self.changePlayer, r.value)
        #self.td(r)



        self.tr()
        self.td(gui.Spacer(0,30))
        self.tr()
        self.td(gui.Label("Player 2 Option: ",color=fg),align=-1)

        self.tr()
        button = gui.Button("Load")
        button.connect(gui.CLICK, self.load, 'RL-Agent2.txt', 1)
        self.td(button)

        button = gui.Button("Save")
        button.connect(gui.CLICK, self.save, 'RL-Agent2.txt', 1)
        self.td(button)


    def slideChange(self, label, slider, scale):
        self.find(label).value  = str(slider.value/scale)
    def setStartListener(self, startFunc):
        self.startFunc = startFunc
    def start(self):
        self.startFunc()
    def setStopListener(self, func):
        self.stopFunc = func
    def stop(self):
        self.stopFunc()

    def setSaveHandler(self, func):
        self.saveFunc = func
    def save(self, filename, playerNumber):
        self.saveFunc(filename, playerNumber)

    def setLoadHandler(self, func):
        self.loadFunc = func
    def load(self, filename, playerNumber):
        self.loadFunc(filename, playerNumber)

    def setPlayerHandler(self, handler):
        self.playerHandler = handler
    def changePlayer(self, value):
        self.playerHandler[value]()

if __name__ == "__main__":
    app = gui.App()
    form = gui.Form()
    ui = PongUI()
    frame = gui.Container(align=-1,valign=-1)
    frame.add(ui,0,0)
    app.init(frame)

    pygame.init()
    screen = pygame.display.set_mode((640,480),SWSURFACE)
    clock = pygame.time.Clock()
            
    done = False
    while not done:
        app.paint(screen)
        pygame.display.flip()
        pygame.time.wait(10)
        for e in pygame.event.get():
            if e.type is QUIT: 
                done = True
            elif e.type is KEYDOWN and e.key == K_ESCAPE: 
                done = True
            else:
                app.event(e)


