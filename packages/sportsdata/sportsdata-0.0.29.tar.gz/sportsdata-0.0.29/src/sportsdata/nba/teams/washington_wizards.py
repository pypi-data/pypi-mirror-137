from sports.nba.nba_team import NBA_Team


class WashingtonWizards(NBA_Team):
    """
    NBA's Washington Wizards Static Information

    """
    full_name = "Washington Wizards"
    name = "Wizards"
    team_id = 1610612764

    def __init__(self):
        """
        """
        super().__init__()
