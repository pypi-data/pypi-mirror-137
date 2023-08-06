import xml.sax
from sports.models.Boxscore import Boxscore

class BoxscoreXml(xml.sax.ContentHandler):
    """
    Parse the boxscore.xml file
    """
    def __init__(self):
        self.boxscore = Boxscore()

    def startElement(self, name, attrs):
        if name == 'boxscore':
            self.boxscore.info = dict(attrs)
            for k,v in attrs.items():
                setattr(self.boxscore,k,v)
        elif name == 'linescore':
            self.boxscore.linescore = dict(attrs)
            for k,v in attrs.items():
                self.boxscore.linescore[k] = v
        elif name == 'inning_line_score':
            self.boxscore.inning_line_scores.append(dict(attrs))