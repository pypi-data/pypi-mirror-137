import xml.sax
from sports.models.Game import Game
from sports.models.AtBat import AtBat
from sports.models.Bunch import Bunch

class GameEventsXml(xml.sax.ContentHandler):
    def __init__(self):
        self.game = Game()
        self.currentAtBat = None
        self.currentAction = None
        self.currentPitch = None

    def startElement(self, name, attrs):
        if name == 'atbat':
            if self.currentAtBat is not None:
                self.game.at_bats.append(self.currentAtBat)
            self.currentAtBat = AtBat(**attrs)
        elif name == 'atBat':
            pass
        elif name == 'action':
            #For some strange reason you can find actions outside of atbats, game id: 2016_06_19_tormlb_balmlb_1
            if ((self.currentAction is not None) and (self.currentAtBat is not None)):
                self.currentAtBat.actions.append(self.currentAction)
            self.currentAction = Bunch(**attrs)
        elif name == 'bottom':
            pass
        elif name == 'deck':
            pass
        elif name == 'game':
            self.game = Game(**attrs)
        elif name == 'hole':
            pass
        elif name == 'inning':
            pass
        elif name == 'pitch':
            if self.currentPitch is not None:
                self.currentAtBat.pitches.append(self.currentPitch)
            self.currentPitch = Bunch(**attrs)
        elif name == 'top':
            pass
        else:
            print(name)