from sports.nba.nba_team import NBA_Team


class NewOrleansPelicans(NBA_Team):
    """
    NBA's New Orleans Pelicans Static Information

    """

    full_name = "New Orleans Pelicans"
    name = "Pelicans"
    team_id = 1610612740

    def __init__(self):
        """
        """
        super().__init__()