from datetime import date


class NBA_Season_2017(object):
    def __init__(self):
        self.description    = "2018–19 NBA season"
        self.start_date     = date(year=2017,month=10, day=17)
        self.end_date       = date(year=2018, month=4, day=11)

        self.playoff_start_date = date(year=2018, month=4, day=13)
        self.playoff_end_date = date(year=2018, month=4, day=13)

        self.finals_start_date = date(year=2018, month=6, day=8)
        self.finals_end_date = date(year=2018, month=6, day=20)
