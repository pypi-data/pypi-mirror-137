from sports.nba.nba_team import NBA_Team


class LosAngelesLakers(NBA_Team):
    """
    NBA Golden State Warriors Static Information

    """
    full_name = "Los Angeles Lakers"
    name = "Lakers"
    team_id = 1610612747

    def __init__(self):
        """
        """
        super().__init__()