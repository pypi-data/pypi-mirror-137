from datetime import date


class NBA_Season_2002(object):
    def __init__(self):
        self.description    = "2002–03 NBA season"
        self.start_date     = date(year=2002,month=10, day=29)
        self.end_date       = date(year=2003, month=4, day=16)

        self.playoff_start_date = date(year=2003, month=4, day=19)
        self.playoff_end_date   = date(year=2003, month=5, day=29)

        self.final_start_date   = None
        self.final_end_date     = None