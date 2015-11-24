# -*- coding: utf-8 -*-

from dateutil.parser import parse
import lxml.html

from .. import scrapers, helpers
from ..models import player


class PlayerSummaryScraper(scrapers.BaseAsyncScraper):
    def __init__(self, concurrency: int):
        super().__init__(concurrency)

    @staticmethod
    def _process_names(container: lxml.html.HtmlElement) -> dict:
        name_str = helpers.get_ascii_content(container.text_content())
        names = name_str.split(' ')
        return dict(
            first=names[0],
            last=names[1],
            number=int(names[2][1:])
        )

    @staticmethod
    def _process_bio(cells: list) -> dict:
        bio = dict()
        for i, cell in enumerate(cells):
            if i % 2 == 0:
                key = helpers.get_ascii_content(cell.text_content().lower())
                if key.strip() == '':
                    continue
                bio[key[:-1]] = helpers.get_ascii_content(cells[i + 1].text_content())
        return bio

    @staticmethod
    def _process_season_stats(table: lxml.html.HtmlElement, is_playoff: bool) -> list:
        stats = []
        rows = table.xpath('.//tr')[1:]
        for row in rows:
            cols = [helpers.get_ascii_content(c.text_content()) for c in row.xpath('.//td')]
            if cols[0] == '':
                continue
            stats.append(
                player.PlayerSeason(cols[0], is_playoff, cols[1], helpers.get_int(cols[2]), helpers.get_int(cols[3]),
                                    helpers.get_int(cols[4]), helpers.get_int(cols[6]), helpers.get_int(cols[7]),
                                    helpers.get_int(cols[8]), helpers.get_int(cols[9]), helpers.get_int(cols[10]),
                                    helpers.get_int(cols[11]), helpers.get_float(cols[12])))
        return stats

    def _process(self, data: dict, page: lxml.html.HtmlElement) -> player.Player:
        names = self._process_names(page.xpath('//div[@id="tombstone"]//h1/div')[0])
        position = page.xpath('//div[@id="tombstone"]/div[2]/div[2]/span')[0].text_content()
        bio = self._process_bio(page.xpath('//table[contains(@class, "bioInfo")]//td'))
        stats_tables = page.xpath('//table[contains(@class, "playerStats")]')
        season_stats = self._process_season_stats(stats_tables[2], False)
        playoff_stats = self._process_season_stats(stats_tables[3], True)
        birth_date = parse(bio['birthdate'].split('(')[0]).date()
        p = player.Player(data['id'], names['first'], names['last'], birth_date, bio['birthplace'],
                               names['number'], position, bio['shoots'], bio['height'], int(bio['weight']))
        for s in season_stats:
            p.add_season(s)
        for s in playoff_stats:
            p.add_season(s)
        return p

    def get(self, ids: list):
        data = [dict(id=id, view='stats') for id in ids]
        return self._get('http://www.nhl.com/ice/player.htm', data)
