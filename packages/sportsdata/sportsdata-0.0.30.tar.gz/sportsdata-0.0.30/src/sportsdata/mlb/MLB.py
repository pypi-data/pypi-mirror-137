import logging
import requests
import requests_cache
import json
import xml
from sports.mlb.handlers import BenchXml
from sports.mlb.handlers import InningsAllXml
from sports.mlb.handlers.InningHit import InningHitXml
from sports.mlb.handlers.InningScoresXml import InningScoresXml
from sports.mlb.handlers.BoxscoreXml import BoxscoreXml
from sports.mlb.handlers.ScoreboardXml import ScoreboardXml
from sports.mlb.handlers.GameXml import GameXml
from sports.mlb.handlers.GamedaySynXml import GamedaySynXml
from sports.mlb.handlers import GameEventsXml

class MLB:
    domain_name = 'mlb.com'
    pitch_types = { 'CH':'Changeup',
                    'CU':'Curveball',
                    'FC':'Cutter',
                    'EP':'Eephus',
                    'FO':'Forkball',
                    'FA':'Four-Seam Fastball',
                    'KN':'Knuckleball',
                    'KC':'Knuckle-curve',
                    'SC':'Screwball',
                    'SI':'Sinker',
                    'SL':'Slider',
                    'FS':'Splitter',
                    'FT':'Two-Seam Fastball'
                    }

    def __init__(self, cache_name='sports.mlb', cache_backend='sqlite', cache_expire_after=1209600):
        if cache_name != None:
            requests_cache.install_cache(cache_name, backend=cache_backend, expire_after=cache_expire_after)


    def _getRequest(self, url, no_cache=False):
        """
        Get URL from cache unless it was disabled
        Args:
            url: URL to retrieve
            no_cache: Controls if Cache will be checked

        Returns:
            req

        """
        if (no_cache==False):
            req = requests.get(url)
        else:
            with requests_cache.disabled():
                req = requests.get(url)
        return req

    def benchXml(self, game_id, returnXml = False):
        """
        Retrieves and optionally processes the bench.xml for a given game
        Args:
            game_id: Identifier for the game

        Returns:

        """
        url = "http://gd2.mlb.com/components/game/mlb/year_{0}/month_{1}/day_{2}/gid_{3}/bench.xml"
        year, month, day, _discard = game_id.split('_', 3)
        url = url.format(year, month, day, game_id)
        req = requests.get(url)

        if returnXml == True:
            return req.text

        bench_xml = BenchXml()
        xml.sax.parseString(req.text, bench_xml)
        return bench_xml.bench


    def benchOXml(self, game_id, returnXml = False):
        """
        Retrieves and optionally processes the benchO.xml for a given game
        (The 'official' bench xml file)

        Args:
            game_id: Identifier for the game
            returnXml:

        Returns:

        """
        url = "http://gd2.mlb.com/components/game/mlb/year_{0}/month_{1}/day_{2}/gid_{3}/benchO.xml"
        year, month, day, _discard = game_id.split('_', 3)
        url = url.format(year, month, day, game_id)
        req = requests.get(url)

        if returnXml == True:
            return req.text

        bench_xml = BenchXml()
        xml.sax.parseString(req.text, bench_xml)
        return bench_xml.bench

    def boxscoreXml(self, game_id, returnXml = False):
        """
        Retrieves, and optionally processes the boxscore.xml file

        Args:
            game_id: Identifier for the game
        :return:
        """
        url = "http://gd2.mlb.com/components/game/mlb/year_{0}/month_{1}/day_{2}/gid_{3}/boxscore.xml"
        year, month, day, _discard = game_id.split('_', 3)
        url = url.format(year, month, day, game_id)
        req = requests.get(url)
        print(url)

        if returnXml == True:
            return req.text

        boxscore_xml = BoxscoreXml()
        xml.sax.parseString(req.text,boxscore_xml)
        return boxscore_xml.boxscore

    def careerHittingJson(self,player_id,game_type,returnJson=False):
        """

        Args:
            player_id:
            game_type:
            returnJson:

        Returns:

        """
        url = "http://lookup-service-prod.mlb.com/json/named.sport_career_hitting.bam?league_list_id='mlb'&game_type={0}&player_id={1}"
        url = url.format(game_type, player_id)
        req = requests.get(url)
        json_data = str(req.text, 'ISO-8859-1').encode('utf8')

        if returnJson:
            return json_data

        data = json.loads(json_data)
        return data

    def careerHittingLeagueJson(self,player_id,game_type,returnJson=False):
        """

        Args:
            player_id:
            game_type:
            returnJson:

        Returns:

        """
        url = "http://lookup-service-prod.mlb.com/json/named.sport_career_hitting_lg.bam?league_list_id='mlb'&game_type={0}&player_id={1}"
        url = url.format(game_type, player_id)
        req = requests.get(url)
        json_data = str(req.text, 'ISO-8859-1').encode('utf8')

        if returnJson:
            return json_data

        data = json.loads(json_data)
        return data

    def careerPitchingJson(self,player_id,game_type,returnJson=False):
        """

        Args:
            player_id:
            game_type:
            returnJson:

        Returns:

        """
        url = "http://lookup-service-prod.mlb.com/json/named.sport_career_pitching.bam?league_list_id='mlb'&game_type={0}&player_id={1}"
        url = url.format(game_type, player_id)
        req = requests.get(url)
        json_data = str(req.text, 'ISO-8859-1').encode('utf8')

        if returnJson:
            return json_data

        data = json.loads(json_data)
        return data

    def careerPitchingLeagueJson(self,player_id,game_type,returnJson=False):
        """

        Args:
            player_id:
            game_type:
            returnJson:

        Returns:

        """
        url = "http://lookup-service-prod.mlb.com/json/named.sport_career_pitching_lg.bam?league_list_id='mlb'&game_type={0}&player_id={1}"
        url = url.format(game_type, player_id)
        req = requests.get(url)
        json_data = str(req.text, 'ISO-8859-1').encode('utf8')

        if returnJson:
            return json_data

        data = json.loads(json_data)
        return data

    def copyrightTxt(self):
        """
        Retrieves the MLBAM License governing the usage of their data
        :return: (String) Copyright Text
        """
        url = "http://gdx.mlb.com/components/copyright.txt"
        req = requests.get(url)
        return req.text

    def gameXml(self, game_id, returnXml = False):
        """
        Retrieves, and optionally processes the game.xml file

        Args:
            game_id: Identifier for the game
        Returns:
        """
        url = "http://gd2.mlb.com/components/game/mlb/year_{0}/month_{1}/day_{2}/gid_{3}/game.xml"
        year, month, day, _discard = game_id.split('_', 3)
        url = url.format(year, month, day, game_id)
        req = requests.get(url)

        if returnXml == True:
            return req.text

        game_xml = GameXml()
        xml.sax.parseString(req.text, game_xml)
        return game_xml.game

    def gameday_SynXml(self, game_id, returnXml = False):
        """

        :param game_id:
        :return:
        """
        url = "http://gd2.mlb.com/components/game/mlb/year_{0}/month_{1}/day_{2}/gid_{3}/gameday_Syn.xml"
        year, month, day, _discard = game_id.split('_', 3)
        url = url.format(year, month, day, game_id)
        req = requests.get(url)
        print(url)

        if returnXml == True:
            return req.text

        gameday_syn_xml = GamedaySynXml()
        xml.sax.parseString(req.text,gameday_syn_xml)


    def gameEventsXml(self, game_id, returnXml = False, no_cache=False):
        """
        Retrieve, and optionally process, the game_events.xml file

        Args:
            game_id: Identifier for the game

        Returns:
        """
        url = "http://gd2.mlb.com/components/game/mlb/year_{0}/month_{1}/day_{2}/gid_{3}/game_events.xml"
        year, month, day, _discard = game_id.split('_', 3)
        url = url.format(year, month, day, game_id)
        req = self._getRequest(url, no_cache)
        #print(url)
        if returnXml == True:
            return req.text

        game_events_xml = GameEventsXml()
        xml.sax.parseString(req.text,game_events_xml)
        game_events_xml.game.game_id = game_id
        return game_events_xml.game


    def inningsAllXml(self, game_id, returnXml = False):
        """
        Retrieves, and optionally parses the inning_all.xml

        Args:
            game_id:  MLB game id
            returnXml: Controls if the xml data

        Returns:
            inning_all.xml's content or a Game object
        """

        url = "http://gd2.mlb.com/components/game/mlb/year_{0}/month_{1}/day_{2}/gid_{3}/inning/inning_all.xml"
        year, month, day, _discard = game_id.split('_', 3)
        url = url.format(year, month, day, game_id)
        req = requests.get(url)
        print(url)

        if returnXml == True:
            return req.text

        innings_all_xml = InningsAllXml()
        xml.sax.parseString(req.text, innings_all_xml)
        return innings_all_xml.game

    def inningHitXml(self, game_id, returnXml = False):
        """

        :param game_id:
        :return:
        """
        url = "http://gd2.mlb.com/components/game/mlb/year_{0}/month_{1}/day_{2}/gid_{3}/inning/inning_hit.xml"
        year, month, day, _discard = game_id.split('_', 3)
        url = url.format(year, month, day, game_id)
        req = requests.get(url)

        if returnXml == True:
            return req.text

        inning_hit_xml = InningHitXml()
        xml.sax.parseString(req.text, inning_hit_xml)
        return inning_hit_xml.hits

    def inningScoresXml(self, game_id, returnXml=False):
        """

        :param:
            game_id

        :return:
        @todo Correctly Parse this xml file
        """
        url = "http://gd2.mlb.com/components/game/mlb/year_{0}/month_{1}/day_{2}/gid_{3}/inning/inning_Scores.xml"
        year, month, day, _discard = game_id.split('_', 3)
        url = url.format(year, month, day, game_id)
        req = requests.get(url)

        if returnXml:
            return req.text

        inning_scores_xml = InningScoresXml()
        xml.sax.parseString(req.text,inning_scores_xml)
        return inning_scores_xml.hits


    def playerInfoJson(self, player_id, returnJson=False):
        """
        Retrieves, and optionally process, the player_info.bam JSON endpoint

        Args:
            player_id:

        Returns:

        """
        url = "http://lookup-service-prod.mlb.com/json/named.player_info.bam?sport_code='mlb'&player_id='{0}'"
        url = url.format(player_id)
        req = requests.get(url)

        if (returnJson==True):
            return req.text

        data = json.loads(req.text)
        return data['player_info']['queryResults']['row']

    def playerTeams(self, season=None, player_id=None):
        """

        Args:
            player_id: Player ID (Required)
            season:
        Returns:

        """
        url = "http://lookup-service-prod.mlb.com/json/named.player_teams.bam?season='{0}'&player_id='{1}'"

        url = url.format(season, player_id)

    def projectedHittingJson(self,player_id,season=None,returnJson=False):
        """

        Args:
            player_id:
            season:
            returnJson:

        Returns:

        """
        url = "http://lookup-service-prod.mlb.com/json/named.proj_pecota_hitting.bam?player_id={0}".format(player_id)

        if season!=None:
            url += "&season={0}".format(season)

        req = requests.get(url)
        json_data = str(req.text, 'ISO-8859-1').encode('utf8')

        if returnJson:
            return json_data

        data = json.loads(json_data)
        return data

    def projectedPitchingJson(self,player_id,season=None,returnJson=False):
        """

        Args:
            player_id:
            season:
            returnJson:

        Returns:

        """
        url = "http://lookup-service-prod.mlb.com/json/named.proj_pecota_pitching.bam?player_id={0}".format(player_id)

        if season!=None:
            url += "&season={0}".format(season)

        req = requests.get(url)
        json_data = str(req.text, 'ISO-8859-1').encode('utf8')

        if returnJson:
            return json_data

        data = json.loads(json_data)
        return data

    def rawboxscoreXml(self, game_id, returnXml = False):
        """

        :param game_id:
        :return:
        """
        url = "http://gd2.mlb.com/components/game/mlb/year_{0}/month_{1}/day_{2}/gid_{3}/rawboxscore.xml"
        year, month, day, _discard = game_id.split('_', 3)
        url = url.format(year, month, day, game_id)
        req = requests.get(url)

        if returnXml:
            return req.text

        boxscore_xml = BoxscoreXml()
        xml.sax.parseString(req.text, boxscore_xml)
        return boxscore_xml.boxscore


    def scoreboardXml(self, lookup_date, returnXml=False, no_cache=False):
        """
        Retrieves, and optionally processes the scoreboard.xml file for a given date.
        :param:
            lookup_date

        :returns:
            Scoreboard, if returnXml == False
            (XML) string, if returnXml == True
        """
        url = "http://gd2.mlb.com/components/game/mlb/year_{0}/month_{1:02d}/day_{2:02d}/scoreboard.xml"
        url = url.format(lookup_date.year, lookup_date.month, lookup_date.day)
        req = self._getRequest(url,no_cache)
        logging.debug("scoreboardXml URL: {0}".format(url))

        if returnXml:
            return req.text

        scoreboardXml = ScoreboardXml()
        xml.sax.parseString(req.text, scoreboardXml)
        return scoreboardXml.scoreboard


    def searchPlayerAllJson(self,active_sw=None,name_part=None,returnJson=False):
        """

        Args:
            active_sw:
            name_part:

        Returns:

        """
        url = "http://lookup-service-prod.mlb.com/json/named.search_player_all.bam?sport_code = 'mlb'"


        if (active_sw):
            url += "&active_sw={0}".format(active_sw)

        if (name_part):
            url += "&name_part={0}".format(name_part)

        req = requests.get(url)
        json_data = str(req.text, 'ISO-8859-1').encode('utf8')

        if returnJson:
            return json_data

        data = json.loads(json_data)
        return data


    def sportHittingJson(self,player_id, game_type, season, returnJson=False):
        """

        Args:
            player_id:
            game_type:
            season:
            returnJson:

        Returns:

        """
        url = "http://lookup-service-prod.mlb.com/json/named.sport_hitting_tm.bam?league_list_id='mlb'&game_type={0}&season={1}&player_id={2}"
        url = url.format(game_type,season,player_id)
        req = requests.get(url)
        json_data = str(req.text, 'ISO-8859-1').encode('utf8')

        if returnJson:
            return json_data

        data = json.loads(json_data)
        return data

    def sportPitchingJson(self, player_id, game_type, season, returnJson=False):
        """
        Args:
            game_type:
            season:
            player_id
        Returns:

        """
        url = "http://lookup-service-prod.mlb.com/json/named.sport_pitching_tm.bam?league_list_id='mlb'&game_type={0}&season={1}&player_id={2}"
        url = url.format(game_type,season,player_id)
        req = requests.get(url)
        json_data = str(req.text, 'ISO-8859-1').encode('utf8')

        if returnJson:
           return json_data

        data = json.loads(json_data)
        return data
