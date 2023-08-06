import xml.sax
from sports.models import Game
from sports.models import Inning
from sports.models.AtBat import AtBat

class InningsAllXml(xml.sax.ContentHandler):
    def __init__(self):
        self.currentInning = None
        self.currentAtBat  = None

        self.game = Game()

    def startElement(self, name, attrs):
        if name == 'game':
            # Add all the attrbutes for the Game
            for k, v in attrs.items():
                setattr(self.game, k, v)
        elif name == 'inning':
            # Finished Processing the Previous Inning
            if self.currentInning != None:
              self.game.innings.append(self.currentInning)

            # Add all the attributes for the Inning
            self.currentInning = Inning()
            for k,v in attrs.items():
                setattr(self.currentInning,k,v)
        elif name == 'atbat':
            # Finished processing the previous at bat
            if self.currentAtBat != None:
                self.currentInning.at_bats.append(self.currentAtBat)
            self.currentAtBat = AtBat()
            for k,v in attrs.items():
                setattr(self.currentAtBat,k,v)
        elif name == 'pitch':
            self.currentAtBat.pitches.append(attrs.items())
        elif name == 'runner':
            self.currentAtBat.runners.append(dict(attrs))