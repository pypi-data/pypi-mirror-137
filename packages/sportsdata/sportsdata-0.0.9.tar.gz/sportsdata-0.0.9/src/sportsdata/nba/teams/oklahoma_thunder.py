from sports.nba.nba_team import NBA_Team


class OklahomaThunder(NBA_Team):
    """
    NBA Golden State Warriors Static Information

    """
    full_name = "Oklahoma Thunder"
    name = "Thunder"
    team_id = 1610612760

    def __init__(self):
        """
        """
        super().__init__()