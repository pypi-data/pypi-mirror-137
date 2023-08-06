import xml.sax
from sports.models.Game import Game
from sports.models.Bunch import Bunch

class GamedaySynXml(xml.sax.ContentHandler):
    def __init__(self):
        self.game = None

    def startElement(self, name, attrs):
        if name == 'game':
            self.game = Game(**attrs)
        elif name == 'date':
            pass
        elif name == 'venue':
            self.game.stadium = Bunch(**attrs)
        elif name == 'game-status':
            pass
        elif name == 'away-team':
            self.game.away_team = Bunch(**attrs)
        elif name == 'home-team':
            self.game.home_team = Bunch(**attrs)
        elif name == 'lineup':
            pass
        elif name == 'batter':
            pass
        elif name == 'pitching':
            pass
        elif name == 'stats':
            pass
        elif name == 'pbp':
            pass
        elif name == 'pickoff-attempt':
            pass
        elif name == 'pitch-by-pitch':
            pass
        elif name == 'pitch':
            pass
        elif name == 'pickoff-attempt':
            pass
        elif name == 'atbat':
            pass
        elif name == 'play-by-play':
            pass
        elif name == 'scoring-summary':
            pass
        elif name == 'score':
            pass
        elif name == 'w':
            pass
        elif name == 'l':
            pass
        elif name == 'era':
            pass
        elif name == 'sv':
            pass
        elif name == 'pitcher':
            pass
        elif name == 'mlb-gde':
            pass
        elif name == 'batting':
            pass
        elif name == 'avg':
            pass
        elif name == 'hr':
            pass
        elif name == 'rbi':
            pass
        elif name == 'sb':
            pass
        elif name == 'on-deck':
            pass
        elif name == 'in-hole':
            pass
        elif name == 'baserunner':
            pass
        elif name == 'r':
            pass
        elif name == 'h':
            pass
        elif name == 'e':
            pass
        elif name == 'atbat-pitch-by-pitch':
            pass
        elif name == 'linescore':
            pass
        elif name == 'atbat-pitch-by-pitch':
            pass
        else:
            print(name)