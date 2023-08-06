from sports.nba.nba_team import NBA_Team


class PhoenixSuns(NBA_Team):
    """
    NBA Golden State Warriors Static Information

    """
    full_name = "Phoenix Suns"
    name = "Suns"
    team_id = 1610612756

    def __init__(self):
        """
        """
        super().__init__()
