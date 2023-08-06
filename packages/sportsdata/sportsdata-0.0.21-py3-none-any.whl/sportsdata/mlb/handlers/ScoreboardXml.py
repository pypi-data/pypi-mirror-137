import xml.sax
from sports.models.Scoreboard import Scoreboard
from sports.models.Game import Game

class ScoreboardXml(xml.sax.ContentHandler):
    """
    Parse the scoreboard.xml
    """
    def __init__(self):
        self.scoreboard = Scoreboard()
        self.currentGame = None

    def startElement(self, name, attrs):
        if name == 'scoreboard':
            self.scoreboard = Scoreboard()
            for k,v in attrs.items():
                setattr(self.scoreboard,k,v)
        elif name == 'game':
            if self.currentGame != None:
                self.scoreboard.games.append(self.currentGame)

            self.currentGame = Game()
            for k,v in attrs.items():
                setattr(self.currentGame,k,v)
        elif name == 'gameteam':
            pass
        elif name == 'p_pitcher':
            pass
        elif name == 'pitcher':
            pass
        elif name == 'team':
            pass