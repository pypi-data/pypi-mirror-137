class NbaTeams:
    """
    A list of all NBA teams and their stats in a given year.

    Finds and retrieves a list of all NBA teams from
    www.basketball-reference.com and creates a Team instance for every team
    that participated in the league in a given year. The Team class comprises
    a list of all major stats and a few identifiers for the requested season.

    Parameters
    ----------
    year : string (optional)
        The requested year to pull stats from.
    season_file : string (optional)
        Optionally specify the filename of a local file to use to pull data
        instead of downloading from sports-reference.com. This file should be
        of the Season page for the designated year.
    """
    def __init__(self, year=None, season_file=None):
        self._teams = []

        # team_data_dict, year = _retrieve_all_teams(year, season_file)
        # self._instantiate_teams(team_data_dict, year)

    def __getitem__(self, abbreviation):
        """
        Return a specified team.

        Returns a team's instance in the Teams class as specified by the team's
        abbreviation.

        Parameters
        ----------
        abbreviation : string
            An NBA team's three letter abbreviation (ie. 'DET' for Detroit
            Pistons).

        Returns
        -------
        Team instance
            If the requested team can be found, its Team instance is returned.

        Raises
        ------
        ValueError
            If the requested team is not present within the Teams list.
        """
        for team in self._teams:
            if team.abbreviation.upper() == abbreviation.upper():
                return team
        raise ValueError('Team abbreviation %s not found' % abbreviation)

    def __call__(self, abbreviation):
        """
        Return a specified team.

        Returns a team's instance in the Teams class as specified by the team's
        abbreviation. This method is a wrapper for __getitem__.

        Parameters
        ----------
        abbreviation : string
            An NBA team's three letter abbreviation (ie. 'DET' for Detroit
            Pistons).

        Returns
        -------
        Team instance
            If the requested team can be found, its Team instance is returned.
        """
        return self.__getitem__(abbreviation)

    def __str__(self):
        """
        Return the string representation of the class.
        """
        teams = [f'{team.name} ({team.abbreviation})'.strip()
                 for team in self._teams]
        return '\n'.join(teams)

    def __repr__(self):
        """
        Return the string representation of the class.
        """
        return self.__str__()

    def __iter__(self):
        """Returns an iterator of all of the NBA teams for a given season."""
        return iter(self._teams)

    def __len__(self):
        """Returns the number of NBA teams for a given season."""
        return len(self._teams)

    def _instantiate_teams(self, team_data_dict, year):
        """
        Create a Team instance for all teams.

        Once all team information has been pulled from the various webpages,
        create a Team instance for each team and append it to a larger list of
        team instances for later use.

        Parameters
        ----------
        team_data_dict : dictionary
            A ``dictionary`` containing all stats information in HTML format as
            well as team rankings, indexed by team abbreviation.
        year : string
            A ``string`` of the requested year to pull stats from.
        """
        if not team_data_dict:
            return
        for team_data in team_data_dict.values():
            team = Team(team_data=team_data['data'],
                        rank=team_data['rank'],
                        year=year)
            self._teams.append(team)

    @property
    def dataframes(self):
        """
        Returns a pandas DataFrame where each row is a representation of the
        Team class. Rows are indexed by the team abbreviation.
        """
        frames = []
        for team in self.__iter__():
            frames.append(team.dataframe)
        return pd.concat(frames)