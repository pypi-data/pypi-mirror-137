from sports.nba.nba_team import NBA_Team


class BrooklynNets(NBA_Team):
    """
    NBA Golden State Warriors Static Information

    """
    full_name   = "Brooklyn Nets"
    name        = "Nets"
    team_id     = 1610612751

    def __init__(self):
        """
        """
        super().__init__()
