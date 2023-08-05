from datetime import date


class NBA_Season_2005(object):
    def __init__(self):
        self.description    = "2005–06 NBA season"
        self.start_date     = date(year=2005, month=10, day=31)
        self.end_date       = date(year=2006, month=4, day=18)

        self.playoff_start_date = date(year=2006, month=4, day=21)
        self.playoff_end_date   = date(year=2006, month=6, day=15)