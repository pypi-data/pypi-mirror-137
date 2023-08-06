from sports.nba.nba_team import NBA_Team


class TorontoRaptors(NBA_Team):
    """
    NBA's Toronto Raptors Static Information

    """
    full_name = "Toronto Raptors"
    name = "Raptors"
    team_id = 1610612761

    def __init__(self):
        """
        """
        super().__init__()