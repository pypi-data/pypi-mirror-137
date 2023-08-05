from sports.nba.nba_team import NBA_Team


class GoldenStateWarriors(NBA_Team):
    """
    NBA Golden State Warriors Static Information

    """
    full_name = "Golden State Warriors"
    name = "Warriors"
    team_id = 1610612744
    def __init__(self):
        """
        """
        super().__init__()