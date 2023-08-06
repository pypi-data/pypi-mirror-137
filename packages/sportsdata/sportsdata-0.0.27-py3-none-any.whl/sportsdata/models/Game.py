class Game(dict):
    def __init__(self, **kw):
        dict.__init__(self, kw)
        self.__dict__.update(kw)

        # Assigned via game.xml
        self.home_team= None
        self.away_team = None
        self.stadium = None

        # Assigned via ????
        self.innings = []

        # Assigned Via game_events.xml
        self.at_bats = []

