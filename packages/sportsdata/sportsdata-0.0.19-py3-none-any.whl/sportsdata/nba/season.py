from glob import glob
import os


class NbaSeason:
    @staticmethod
    def my_import(name, classname):
        components = name.split('.')
        mod = __import__(name)
        for comp in components[1:]:
            mod = getattr(mod, comp)

        requested_class = getattr(mod, classname)
        return requested_class

    def __init__(self):
        """
        Load all Season Objects
        """
        self.seasons = {}
        class_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)))
        class_dir += '/seasons/season_*.py'

        for file in glob(class_dir):
            filename = os.path.splitext(os.path.basename(file))[0]
            name, date = filename.split('_')

            season_file = 'sports.source.nba.seasons.{0}'.format(filename)
            my_classname = "NBA_Season_{0}".format(date)
            my_class = self.my_import(season_file, my_classname)
            self.seasons[date]  = my_class()

    def get(self, season:int):
        """

        Args:
            season: Integer for the start of the season

        Returns:
            NBA_Season_YYYY class

        """
        if season not in self.seasons.keys():
            raise KeyError("{0} does not exist or has not been modeled".format(season))

        return self.seasons[season]