from datetime import date


class NBA_Season_2018(object):
    def __init__(self):
        self.description    = "2018–19 NBA season"
        self.start_date     = date(year=2018,month=10, day=16)
        self.end_date       = date(year=2019, month=4, day=10)

        self.playoff_start_date = date(year=2019, month=4, day=13)
        self.playoff_end_date   = None

        self.finals_start_date = date(year=2010, month=6, day=8)
        self.finals_end_date = date(year=2010, month=6, day=20)
