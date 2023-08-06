from datetime import date


class NBA_Season_2000(object):
    def __init__(self):
        self.description    = "2000–01 NBA season"
        self.start_date     = date(year=2000,month=10, day=31)
        self.end_date       = date(year=2001, month=4, day=18)

        self.playoff_start_date = date(year=2001, month=4, day=21)
        self.playoff_end_date   = date(year=2001, month=6, day=15)