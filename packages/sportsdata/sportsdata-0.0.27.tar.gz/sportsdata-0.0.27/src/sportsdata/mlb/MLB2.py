import requests
class MLB2:
    """
    Handles all calls from the new statsapi
    """
    url_base = "https://statsapi.mlb.com/api/v1"
    mlb_sport_id = 1


    def conferences(self ,conferenceId, season):
        url = "{0}/api/v1/conferences?conferenceId={0}&season={1}".format(self.url_base,conferenceId, season)
        resp = requests.get(url)
        print(resp.text)



    def config(self):
        url = "{0}/api/v1/gameStatus".format(self.url_base)
        resp = requests.get(url)
        print(resp.text)


    def divisions(self,divisionId, leagueId, sportId):
        url = "https://statsapi.mlb.com/api/v1/divisions?divisionId=200&leagueId=103&sportId=1"
        resp = requests.get(url)
        print(resp.text)


    def draft(self, year):
        "https: // statsapi.mlb.com / api / v1 / draft / 2018?limit = 1 & round = 1 & name = M & school = A & position = P & teamId = 116 & playerId = 663554 & bisPlayerId = 759143"
        resp = requests.get(url)
        print(resp.text)



    def game(self, gameId, timecode):
        url = "{0}/game/{1}/feed/live?".format(self.url_base, gameId)
        resp = requests.get(url)
        print(resp.text)

    def games(self):
        url = "{0}/schedule/games/tied?season={1}&hydrate=linescore".format(self.url_base, season)

    def homeRunDerby(self):
        url = "{0}".format(self.url_base)
        resp = requests.get(url)
        print(resp.text)


    def league(self):
        url = "{0}/league?leagueIds=103&seasons=2018".format(self.url_base)
        resp = requests.get(url)
        print(resp.text)

    def person(self, personsId):
        url = "{0}/people?personsIds={1}".format(self.url_base, personIds)
        resp = requests.get(url)
        print(resp.text)


    def schedule_games(self, season):
        url = "{0}/schedule/games/tied?season={1}&hydrate=linescore".format(self.url_base, season)

    def schedule(self):
        url = "{0}/schedule?sportId=1".format(self.url_base)
        resp = requests.get(url)
        print(resp.text)

    def seasons(self, sportId=1):
        url = "{0}/seasons?sportId={1}".format(self.url_base, sportId)
        resp = requests.get(url)
        print(resp.text)
        return resp.text

    def situationCodes(self):
        url = "{0}/situationCodes".format(self.url_base)
        resp = requests.get(url)
        print(resp.text)

    def sports(self, sportId=1):
        url = "{0}/sports/{1}".format(self.url_base, sportId)
        resp = requests.get(url)
        print(resp.text)

    def standings(self, leagueId, season):
        url = "{0}/standings?leagueId={1}&season={2}".format(self.url_base, leagueId, season)
        resp = requests.get(url)
        print(resp.text)

    def stats(self):
        url = "{0}/stats?stats=season&group=hitting".format(self.url_base)
        resp = requests.get(url)
        print(resp.text)

    def team(self):
        url = "{0}/leaders?leaderCategories=homeRuns&hydrate=team".format(self.url_base)
        resp = requests.get(url)
        print(resp.text)

    def venue(self):
        url = "{0}/venues?venueIds=15".format(self.url_base)
        resp = requests.get(url)
        print(resp.text)