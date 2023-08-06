from sports.nba.nba_team import NBA_Team


class NewYorkKnickerbockers(NBA_Team):
    """
    NBA's New York Knickerbockers Static Information

    """

    full_name = "New York Knickerbockers"
    name = "Knickerbockers"
    team_id = 1610612752

    def __init__(self):
        """
        """
        super().__init__()
