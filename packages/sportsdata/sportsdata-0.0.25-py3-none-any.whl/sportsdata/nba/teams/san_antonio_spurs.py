
from sports.nba.nba_team import NBA_Team


class SanAntonioSpurs(NBA_Team):
    """
    NBA Golden State Warriors Static Information

    """

    full_name = "San Antonio Spurs"
    name = "Spurs"
    team_id = 1610612759
    def __init__(self):
        """
        """
        super().__init__()