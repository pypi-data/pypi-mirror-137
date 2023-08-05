from enum import Enum


class Conference(Enum):
    ALL                     = ''
    EAST                    = 'East'
    WEST                    = 'West'

class Division(Enum):
    ALL                     = ''
    ATLANTIC                = 'Atlantic'
    CENTRAL                 = 'Central'
    NORTHWEST               = 'Northwest'
    PACIFIC                 = 'Pacific'
    SOUTHEAST               = 'Southeast'
    SOUTHWEST               = 'Southwest'

class Direction(Enum):
    DESC                    = 'DESC'
    ASC                     = 'ASC'

class GameSegment(Enum):
    FULL_GAME               =   ''
    FIRST_HALF              =   'First Half'
    SECOND_HALF             =   'Second Half'
    OVERTIME                =   'Overtime'

class League(Enum):
    NBA                     =   '00'
    ABA                     =   '01'

class Location(Enum):
    ALL                     =   ''
    HOME                    =   'Home'
    AWAY                    =   'Away'

class Outcome(Enum):
    ALL                     =   ''
    WIN                     =   'W'
    LOSS                    =   'L'

class PlayerOrTeam(Enum):
    PLAYER                  =   'P'
    TEAM                    =   'T'

class SeasonSegment(Enum):
    FULL_SEASON             =   ''
    PRE_ALL_STAR            =   'Pre All-Star'
    POST_ALL_STAR           =   'Post All-Star'


class MeasureType(Enum):
    BASE                    =   'Base'
    ADVANCED                =   'Advanced'
    MISC                    =   'Misc'
    FOUR_FACTORS            =   'Four Factors'
    SCORING                 =   'Scoring'
    OPPONENT                =   'Opponent'
    USAGE                   =   'Usage'

class Period(Enum):
    ALL_PERIODS             =   '0'
    FIRST_QUARTER           =   '1'
    SECOND_QUARTER          =   '2'
    THIRD_QUARTER           =   '3'
    FOURTH_QUARTER          =   '4'
    OVERTIME_1              =   '5'
    OVERTIME_2              =   '6'
    OVERTIME_3              =   '7'
    OVERTIME_4              =   '8'


class PerMode(Enum):
    TOTALS                  =   "Totals"
    MINUTES                 =   'MinutesPer'
    MINUTE                  =   'PerMinute'
    GAME                    =   "PerGame"
    PER_48                  =   "Per48"
    PER_40                  =   'Per40'
    PER_36                  =   "Per36"
    PER_POSSESSION          =   'PerPossession'
    PER_PLAY                =   'PerPlay'
    Per100Possessions       =   'Per100Possessions'
    PER_100_PLAYS           =   'Per100Plays'


class SeasonType(Enum):
    ALL_STAR                =   "All-Star"
    REGULAR_SEASON          =   "Regular Season"
    PRE_SEASON              =   "Pre Season"
    PLAYOFFS                =   "Playoffs"

class StatCategory(Enum):
    POINTS                  =   'PTS'
    FIELD_GOALS_MADE        =   'FGM'
    FIELD_GOALS_ATTEMPTS    =   'FGA'
    FIELD_GOAL_PCT          =   'FG%'
    FIELD_GOAL3M            =   '3PM'
    FIELD_GOAL3A            =   '3PA'
    FIELD_GOAL3_PCT         =   '3P%'
    FREE_THROW_MADE         =   'FTM'
    FREE_THROW_ATTEMPTS     =   'FTA'
    FREE_THROW_PCT          =   'FT%'
    OFFENSIVE_REBOUND       =   'OREB'
    DEFENSIVE_REBOUND       =   'DREB'
    REBOUNDS                =   'REB'
    ASSISTS                 =   'AST'
    STEALS                  =   'STL'
    BLOCKS                  =   'BLK'
    TURNOVER                =   'TOV'
    EFF                     =   'EFF'
    ASSIST_TURNOVER_RATIO   =   'AST/TO'
    STEAL_TURNOVER_RATIO    =   'STL/TOV'