import xml.sax

class InningScoresXml(xml.sax.ContentHandler):
    def __init__(self):
        self.hits = []

    def startElement(self, name, attrs):
        if name == 'hip':
            self.hits.append(dict(attrs))