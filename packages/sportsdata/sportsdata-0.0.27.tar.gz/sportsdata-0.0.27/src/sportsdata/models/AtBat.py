class AtBat(dict):
    def __init__(self,**kw):
        dict.__init__(self,kw)
        self.__dict__.update(kw)

        self.pitches = []
        self.actions = []
        self.runners = []