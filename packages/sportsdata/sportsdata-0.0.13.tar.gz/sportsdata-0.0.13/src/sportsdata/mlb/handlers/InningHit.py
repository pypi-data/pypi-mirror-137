import xml.sax

class InningHitXml(xml.sax.ContentHandler):
    def __init__(self):
        self.hits = []

    def startElement(self, name, attrs):
        if name == 'hip':
            self.hits.append(dict(attrs))