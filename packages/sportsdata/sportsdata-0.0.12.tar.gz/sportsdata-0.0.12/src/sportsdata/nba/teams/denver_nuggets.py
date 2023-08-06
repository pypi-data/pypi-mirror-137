from sports.nba.nba_team import NBA_Team


class DenverNuggets(NBA_Team):
    full_name   = "Denver Nuggets"
    name        = "Nuggets"
    team_id     = 1610612743

    def __init__(self):
        self.color_schemes   =[['0E2240','FEC524','8B2131','1D428A'],[],[]]
        self.color_years     = [{'start':2018,'end':None},{'start':2003,'end':2017},{'start':1993,'end':2003}]
