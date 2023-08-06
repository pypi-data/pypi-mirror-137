from datetime import date


class NBA_Season_2007(object):
    def __init__(self):
        self.description    = "2007–08 NBA season"
        self.start_date     = date(year=2007,month=10, day=31)
        self.end_date       = date(year=2008, month=4, day=18)

        self.playoff_start_date = date(year=2008, month=4, day=21)
        self.playoff_end_date   = date(year=2008, month=6, day=15)

        self.finals_start_date = date(year=2008, month=6, day=8)
        self.finals_end_date = date(year=2008, month=6, day=20)