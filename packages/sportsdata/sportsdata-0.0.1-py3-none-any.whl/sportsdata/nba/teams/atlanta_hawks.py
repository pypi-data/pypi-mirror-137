from sports.nba.nba_team import NBA_Team

class AtlantaHawks(NBA_Team):
    """
    NBA Atlanta Hawks Static Information

    """
    full_name = "Atlanta Hawks"
    name = "Hawks"
    team_id = 1610612737

    def __init__(self):
        """
        """
        super().__init__()