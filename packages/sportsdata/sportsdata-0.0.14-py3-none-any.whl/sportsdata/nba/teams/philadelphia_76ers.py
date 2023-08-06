from sports.nba.nba_team import NBA_Team


class Philadelphia76ers(NBA_Team):
    """
    NBA's Philadelphia 76ers Static Information

    """
    full_name = "Philadelphia 76ers"
    name = "76ers"
    team_id = 1610612755

    def __init__(self):
        """
        """
        super().__init__()
