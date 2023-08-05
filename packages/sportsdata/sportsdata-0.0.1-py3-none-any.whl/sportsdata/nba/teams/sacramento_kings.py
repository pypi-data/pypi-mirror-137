from sports.nba.nba_team import NBA_Team


class SacramentoKings(NBA_Team):
    """
    NBA's Sacramento Kings Static Information

    """
    full_name = "Sacramento Kings"
    name = "Kings"
    team_id = 1610612758

    def __init__(self):
        """
        """
        super().__init__()
