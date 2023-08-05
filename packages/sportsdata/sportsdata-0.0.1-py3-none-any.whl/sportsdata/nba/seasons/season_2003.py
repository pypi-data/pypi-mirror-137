from datetime import date


class NBA_Season_2003(object):
    def __init__(self):
        self.description    = "2003–04 NBA season"
        self.start_date     = date(year=2003,month=10, day=28)
        self.end_date       = date(year=2004, month=4, day=14)

        self.playoff_start_date = date(year=2004, month=4, day=17)
        self.playoff_end_date   = date(year=2004, month=7, day=1)