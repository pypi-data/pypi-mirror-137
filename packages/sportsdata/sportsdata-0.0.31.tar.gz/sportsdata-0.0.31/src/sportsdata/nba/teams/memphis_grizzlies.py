from sports.nba.nba_team import NBA_Team


class MemphisGrizzlies(NBA_Team):
    """
    NBA Memphis Grizzlies Static Information

    """
    full_name = "Memphis Grizzlies"
    name = "Grizzlies"
    team_id = 1610612763

    def __init__(self):
        """
        """
        super().__init__()
