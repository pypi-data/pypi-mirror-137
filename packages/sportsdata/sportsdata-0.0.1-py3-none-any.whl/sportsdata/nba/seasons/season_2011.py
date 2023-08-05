from datetime import date


class NBA_Season_2011(object):
    def __init__(self):
        self.description    = "2011–12 NBA season"
        self.start_date     = date(year=2011,month=10, day=31)
        self.end_date       = date(year=2012, month=4, day=18)

        self.playoff_start_date = date(year=2012, month=4, day=21)
        self.playoff_end_date   = date(year=2012, month=6, day=15)

        self.finals_start_date = date(year=2012, month=6, day=8)
        self.finals_end_date = date(year=2012, month=6, day=20)