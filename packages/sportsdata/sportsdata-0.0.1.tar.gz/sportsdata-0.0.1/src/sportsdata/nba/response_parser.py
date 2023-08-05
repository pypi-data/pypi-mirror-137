import json
from pandas import DataFrame
from .scoreboard import Scoreboard
from .nba_boxscore import NBA_BoxScore

class ResponseParser(object):
    pass

    column_name_mappings = {
        'REMAINING_G'       : 'games_remaining'         ,
        'REMAINING_HOME_G'  : 'home_games_remaining'    ,
        'REMAINING_AWAY_G'  : 'away_games_remaining'    ,
    }

    @staticmethod
    def _get_row_set(rs):
        data = []
        for row in rs['rowSet']:
            data_point = dict(zip([h.lower() for h in rs['headers']], row))
            data.append(data_point)
        return data


    @staticmethod
    def get_data_frames(response, rename_to={}):
        """
        Parse the response for any results and load them into data frames
        Args:
            response:
            rename_to:

        Returns:
            All Result Sets Found as Data Frames

        """
        frames = {}
        info = json.loads(response.text)
        result_sets = info['resultSets']
        for rs in result_sets:
            rs_name = rs['name']
            if rs_name in rename_to.keys():
                rs_name = rename_to[rs_name]

            frames[rs_name] = DataFrame(rs['rowSet'], columns=rs['headers'])

        # Check if there is only one result, if so no need for a dictionary
        if len(frames) == 1:
            key = next(iter(frames))
            frames = frames[key]

        return frames

    ###################################
    # Individual API Endpoint Parsing #
    ###################################
    @staticmethod
    def boxscore_player_track(response):
        boxscore = NBA_BoxScore()
        info = json.loads(response.text)
        for rs in info['resultSets']:
            if rs['name'] == 'PlayerStats':
                for row in rs['rowSet']:
                    player = dict(zip([h.lower() for h in rs['headers']], row))
                    hours, seconds = player['min'].split(':')
                    player['seconds_played'] = int(hours) * 60 + int(seconds)
                    boxscore.players.append(player)
            elif rs['name'] == 'TeamStats':
                for row in rs['rowSet']:
                    team = dict(zip([h.lower() for h in rs['headers']], row))
                    boxscore.teams.append(team)
            else:
                print(rs)
                pass
        return boxscore

    @staticmethod
    def boxscore_summary(response):
        boxscore = NBA_BoxScore()
        info = json.loads(response.text)


        if 'resultSets' not in info:
            return boxscore

        for rs in info['resultSets']:
            if rs['name'] == 'GameSummary':
                summary = ResponseParser._get_row_set(rs)[0]
                boxscore._set_attributes(summary)
            elif rs['name'] == 'GameInfo':
                game_info = ResponseParser._get_row_set(rs)[0]
                boxscore._set_attributes(game_info)
            elif rs['name'] == 'LineScore':
                team_stats = ResponseParser._get_row_set(rs)
                # Set Home/Visitor Points
                for team_stat in team_stats:
                    if team_stat['team_id'] == boxscore.home_team_id:
                        boxscore.home_points = team_stat['pts']
                    else:
                        boxscore.visitor_points = team_stat['pts']

                # Set Winning Team Id
                if boxscore.home_points > boxscore.visitor_points:
                    boxscore.winning_team_id = boxscore.home_team_id
                else:
                    boxscore.winning_team_id = boxscore.visitor_team_id
            else:
                #print(rs)
                pass
        return boxscore

    @staticmethod
    def scoreboard_v2(response):
        scoreboard  = Scoreboard()
        info        = json.loads(response.text)
        processed_games = []


        for rs in info['resultSets']:
            if rs['name'] == 'LineScore':
                for row in rs['rowSet']:
                    game = dict(zip([h.lower() for h in rs['headers']], row))
                    if game['game_id'] not in processed_games:
                        scoreboard.games.append(game)
                        processed_games.append(game['game_id'])
            elif rs['name'] == 'SeriesStandings':
                for row in rs['rowSet']:
                    info = dict(zip([h.lower() for h in rs['headers']], row))
                    scoreboard.series_standings.append(info)
            else:
                #print(rs)
                pass

        return scoreboard