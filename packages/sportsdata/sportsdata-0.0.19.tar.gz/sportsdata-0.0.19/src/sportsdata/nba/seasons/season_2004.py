from datetime import date


class NBA_Season_2004(object):
    def __init__(self):
        self.description    = "2004–05 NBA season"
        self.start_date     = date(year=2004,month=11, day=2)
        self.end_date       = date(year=2005, month=4, day=20)

        self.playoff_start_date = date(year=2005, month=4, day=23)
        self.playoff_end_date   = date(year=2005, month=6, day=6)