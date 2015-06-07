# -*- coding: utf-8 -*-

from datetime import date, datetime

from backcheck.helpers import season_by_date

class PlayerSeason(object):
    def __init__(self, season: str, is_playoff: bool, team: str, gp: int, g: int, a: int, pm: int, pim: int, ppg: int, shg: int, gwg: int, s: int, sp: float):
        self.season = season
        self.is_playoff = is_playoff
        self.team = team
        self.gp = gp
        self.g = g
        self.a = a
        self.pm = pm
        self.pim = pim
        self.ppg = ppg
        self.shg = shg
        self.gwg = gwg
        self.s = s
        self.sp = sp

    def __str__(self):
        return '{0}: {1}{2}'.format(self.season, self.team, ' / PO' if self.is_playoff else '')

class Player(object):
    def __init__(self, id: int, first_name: str, last_name: str, birth_date: date, birth_place: str, number:int, position:str, shoots: str, height: str, weight: int):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.birth_place = birth_place
        self.number = number
        self.position = position
        self.shoots = shoots
        self.height = height
        self.weight = weight
        self.seasons = []

    def __str__(self):
        return '{0} {1}'.format(self.first_name, self.last_name)

    def add_season(self, season: PlayerSeason):
        self.seasons.append(season)

    def find_seasons(self, season: str, is_playoff: bool=False):
        return [s for s in self.seasons if s.season == season and s.is_playoff == is_playoff]

    def get_current_season(self, is_playoff: bool=False):
        season = season_by_date(datetime.utcnow())
        matching_seasons = self.find_seasons(season, is_playoff)
        if len(matching_seasons) > 0:
            return matching_seasons[0]
        return None