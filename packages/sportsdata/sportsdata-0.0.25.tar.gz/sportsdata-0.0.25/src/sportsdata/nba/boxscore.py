class NbaBoxScore(object):
    def _set_attributes(self, attributes):
        for key, value in attributes.items():
            setattr(self, key, value)

    def __init__(self):
        self.players = []
        self.teams   = []

        # Set via the boxscore_summary endpoint
        self.attendance         =   None
        self.game_date          =   None
        self.game_time          =   None
        self.home_team_id       =   None
        self.visitor_team_id    =   None
        self.winning_team_id    =   None    #Not sure where set yet
