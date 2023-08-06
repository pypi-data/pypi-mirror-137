from sports.nba.nba_team import NBA_Team


class UtahJazz(NBA_Team):
    """
    NBA's Washington Wizards Static Information

    """

    full_name = "Utah Jazz"
    name = "Jazz"
    team_id = 1610612762

    def __init__(self):
        """
        """
        super().__init__()