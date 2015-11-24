# -*- coding: utf-8 -*-

from datetime import date
import unittest

from backcheck.scrapers import player

class TestScrapePlayerSummary(unittest.TestCase):
    def setUp(self):
        pass

    def test_get_player_summary(self):
        scraper = player.PlayerSummaryScraper(1)
        pls = scraper.get([8471676])
        self.assertGreater(len(pls), 0)
        p = pls[0]
        self.assertEqual(p.birth_date, date(1987, 3, 17))
        self.assertEqual(p.first_name, 'Bobby')
        self.assertEqual(p.last_name, 'Ryan')
        self.assertEqual(p.height, '6\' 2"')
        self.assertEqual(p.id, 8471676)
        self.assertEqual(p.number, 6)
        self.assertEqual(p.position, 'Right Wing')
        self.assertEqual(p.shoots, 'Right')
        self.assertAlmostEqual(p.weight, 207, delta=20)
        test_season = p.find_seasons(season='2014-2015', is_playoff=False)
        self.assertEqual(1, len(test_season))
        s = test_season[0]
        self.assertEqual(s.a, 36)
        self.assertEqual(s.g, 18)
        self.assertEqual(s.gp, 78)
        self.assertEqual(s.gwg, 5)
        self.assertEqual(s.is_playoff, False)
        self.assertEqual(s.pim, 24)
        self.assertEqual(s.pm, 5)
        self.assertEqual(s.ppg, 4)
        self.assertEqual(s.s, 221)
        self.assertEqual(s.season, '2014-2015')
        self.assertEqual(s.shg, 0)
        self.assertEqual(s.sp, 8.1)
        self.assertEqual(s.team, 'Senators')
