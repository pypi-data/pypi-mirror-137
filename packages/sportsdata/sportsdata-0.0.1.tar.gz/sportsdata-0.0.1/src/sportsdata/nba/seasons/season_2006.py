from datetime import date


class NBA_Season_2006(object):
    def __init__(self):
        self.description    = "2006–07 NBA season"
        self.start_date     = date(year=2006, month=11, day=1)
        self.end_date       = date(year=2007, month=4, day=19)

        self.playoff_start_date = date(year=2007, month=4, day=22)
        self.playoff_end_date   = date(year=2007, month=6, day=3)

        self.finals_start_date = date(year=2007, month=6, day=8)
        self.finals_end_date   = date(year=2007, month=6, day=20)