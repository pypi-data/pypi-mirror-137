import xml.sax
from sports.models.Bench import Bench
class BenchXml(xml.sax.ContentHandler):


    def __init__(self):
        self.bench = Bench()


    def startElement(self, tag, attributes):
        if tag == "away":
            self.bench.isHomeOrAway = tag
            self.bench.awayTeamID   = attributes['tid']
        elif tag == 'batter' and self.bench.isHomeOrAway == 'away':
            self.bench.awayBatters.append(dict(attributes))
        elif tag == 'batter' and self.bench.isHomeOrAway == 'home':
            self.bench.homeBatters.append(dict(attributes))
        elif tag == "pitcher" and self.bench.isHomeOrAway == 'away':
            self.bench.awayPitchers.append(dict(attributes))
        elif tag == "pitcher" and self.bench.isHomeOrAway == 'home':
            self.bench.homePitchers.append(dict(attributes))
        elif tag == "home":
            self.bench.isHomeOrAway = tag
            self.bench.homeTeamID = attributes['tid']