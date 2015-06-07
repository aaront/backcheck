# -*- coding: utf-8 -*-

from datetime import datetime

def season_by_date(date: datetime):
    year = date.year
    if date.month >= 10:
        return '{0}-{1}'.format(year, year+1)
    else:
        return '{0}-{1}'.format(year-1, year)

def get_ascii_content(cell_content: str):
    return cell_content.replace('\n', '').encode('ascii', 'ignore').strip().decode('utf8')

def get_int(s) -> int:
    s = s.strip()
    return int(s) if s else 0

def get_float(s) -> float:
    s = s.strip()
    return float(s) if s else 0