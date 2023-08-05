from datetime import date


class NBA_Season_2001(object):
    def __init__(self):
        self.description    = "2001–02 NBA season"
        self.start_date     = date(year=2001,month=10, day=30)
        self.end_date       = date(year=2002, month=4, day=17)

        self.playoff_start_date = date(year=2002, month=4, day=20)
        self.playoff_end_date   = date(year=2002, month=6, day=2)