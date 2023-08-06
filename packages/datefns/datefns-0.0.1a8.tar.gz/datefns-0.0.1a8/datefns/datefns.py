"""
Various utilities for dates.
"""

from collections import namedtuple
import csv
import datetime
from datetime import timedelta
from calendar import month_name, monthrange, day_name
from pathlib import Path
import sqlite3
from typing import Dict, List, NamedTuple, Optional

__all__ = [
    'week_ending',
    'date_table',
    'load_date_table',
    'holiday_name',
    'date_table_to_csv',
    'eomonth',
    'date_table_insert_sql',
    'date_range',
    'by_month',
]

class DatefnError(Exception):
    pass

class BadDay(DatefnError):
    pass

def week_ending(date: datetime.date, week_ends_on: Optional[str] = 'Sat') -> datetime.date:
    "Return the date of"
    days = {
        'Mon' : 'Mon',
        'M' : 'Mon',
        'Tue' : 'Tue',
        'Tu' : 'Tue',
        'Wed' : 'Wed',
        'W' : 'Wed',
        'Thu' : 'Thu',
        'Th' : 'Thu',
        'Fri' : 'Fri',
        'F' : 'Fri',
        'Sat' : 'Sat',
        'Sa' : 'Sat',
        'Sun' : 'Sun',
        'Su' : 'Sun',
        'Sunday' : 'Sun',
        'Monday' : 'Mon',
        'Tuesday' : 'Tue',
        'Wednesday' : 'Wed',
        'Thursday' : 'Thu',
        'Friday' : 'Fri',
        'Saturday' : 'Sat',
    }
    if week_ends_on not in days:
        raise BadDay("Cannot understand '%s' for week_ends_on argument" % week_ends_on)
    offsets = {
        'Mon' : 6,
        'Tue' : 5,
        'Wed' : 4,
        'Thu' : 3,
        'Fri' : 2,
        'Sat' : 1,
        'Sun' : 0,
    }
    offset = offsets[days[week_ends_on]]
    start = date - timedelta(days=(date.weekday() + offset) % 7)
    end = start + timedelta(days=6)
    return end


def holiday_name(date: datetime.date, special_holidays: dict = None):
    "Return the holiday name (if any) for the date provided"
    holidays = special_holidays or {}
    if date in holidays:
        return holidays[date]

    first_weekday_of_month = monthrange(date.year, date.month)[0]
    if date.weekday() >= first_weekday_of_month:
        delta = date.weekday() - first_weekday_of_month
    else:
        delta = 7 + date.weekday() - first_weekday_of_month
    first_sameday_of_month = datetime.date(date.year, date.month, 1) + timedelta(days=delta)
    nth_day_of_month = (date - first_sameday_of_month).days // 7 + 1
    day_of_week = day_name[date.weekday()]

    if date.month == 1 and date.day == 1:
        return "New Year's"
    if date.month == 1 and day_of_week == 'Monday' and nth_day_of_month == 3:
        return 'Martin Luther King'
    if date.month == 2 and day_of_week == 'Monday' and nth_day_of_month == 3:
        return "President's Day"
    if date.month == 5 and day_of_week == 'Monday' and (date + timedelta(days=7)).month != date.month:
        return 'Memorial Day'
    if date.month == 7 and date.day == 4:
        return '4th of July'
    if date.month == 9 and day_of_week == 'Monday' and nth_day_of_month == 1:
        return 'Labor Day'
    if date.month == 11 and day_of_week == 'Thursday' and nth_day_of_month == 4:
        return 'Thanksgiving'
    if date.month == 11 and day_of_week == 'Friday':
        first_day_of_month = day_name[datetime.date(date.year, date.month, 1).weekday()]
        if first_day_of_month == 'Friday' and nth_day_of_month == 5:
            return 'Day After Thanksgiving'
        elif first_day_of_month != 'Friday' and nth_day_of_month == 4:
            return 'Day After Thanksgiving'
    if date.month == 12 and date.day == 24:
        return 'Christmas Eve'
    if date.month == 12 and date.day == 25:
        return 'Christmas'
    if date.month == 12 and date.day == 31:
        return "New Year's Eve"
    return None

def num_business_days_in_month(date: datetime.date, special_holidays: dict = None) -> int:
    "Return the number of business days in the month of the given date"
    this_date = datetime.date(date.year, date.month, 1)
    end_date = datetime.date(date.year, date.month, monthrange(date.year, date.month)[1])
    num_bus_days = 0
    while this_date <= end_date:
        if holiday_name(this_date) is None and this_date.weekday() < 5:
            num_bus_days += 1
        this_date += timedelta(days=1)
    return num_bus_days


def date_table(start_date: datetime.date, end_date: datetime.date) -> List[NamedTuple]:
    """
    Create a dates table for use in data warehouse environment
    
    The table will have one day for each day between "start_date" and
    "end_date" (inclusive of both).

    Fields included in table:
        - date_id (incrementing integer)
        - date_int (eg, 20140131)
        - date (eg, 2014-01-31)
        - year (eg, 2014)
        - quarter_int (eg, 3)
        - quarter (eg, Q3)
        - month_int (eg, 4)
        - month_name (eg, April)
        - month_end (eg, 2018-04-30)
        - day_of_month (eg, 27)
        - week_ending (eg, 2018-07-28) - note, weeks end on a saturday
        - day_of_week_int (0 = sunday, 7 = saturday)
        - day_of_week (eg, Monday)
        - year_month (eg, 201407)
        - holiday (eg, New Year's)
        - is_weekday (Yes/No)
        - is_holiday (Yes/No)
        - is_workday (Yes/No)
        - num_weekdays (1 for weekday, 0 otherwise)
        - num_holidays (1 for holiday, 0 otherwise)
        - num_workdays (1 for workday, 0 otherwise - workday = Mon-Fri and not a holiday)
        - week_num (eg, 1 = 1st week of year)
        - week_num_of_year (eg, 1 / 53 or 1 / 52)
        - weeks_remaining_in_year (eg, 52 if on week one in week with 53 weeks)
        - business_day_of_month (eg, 20)
        - business_days_in_month (eg, 22)
        - workday_number_of_year
        - day_number_of_year
        - is_last_day_of_week
        - is_last_day_of_month
    """
    assert end_date >= start_date, "end_date must be after start_date"
    assert start_date.month == 1 and start_date.day == 1, "Currently need to start on Jan 1 or metrics won't work correctly"
    DateRow = namedtuple('DateRow', [
        'date_id',
        'date_int',
        'date',
        'year',
        'quarter_int',
        'quarter',
        'month_int',
        'month_name',
        'month_end',
        'day_of_month',
        'week_ending',
        'day_of_week_int',
        'day_of_week',
        'year_month',
        'year_quarter',
        'holiday',
        'is_weekday',
        'is_holiday',
        'is_workday',
        'num_weekdays',
        'num_holidays',
        'num_workdays',
        'week_num',
        'week_num_of_year',
        'weeks_remaining_in_year',
        'business_day_of_month',
        'business_days_in_month',
        'business_day_of_year',
        'day_number_of_year',
        'is_last_day_of_week',
        'is_last_day_of_month',
    ])
    date = datetime.date(start_date.year, start_date.month, 1)
    dates = [] # type: ignore
    bus_days_in_month = {} # type: Dict[str, int]
    bus_day_of_mo = 0
    day_of_year = 0
    bus_day_of_year = 0
    while date <= end_date:
        qtr = (date.month - 1) // 3 + 1
        holiday = holiday_name(date)
        if date.day == 1:
            bus_day_of_mo = 0
            bus_days_in_month[date.strftime("%Y%m")] = num_business_days_in_month(date)
            if date.month == 1:
                bus_day_of_year = 0
                day_of_year = 0
        if holiday is None and date.weekday() < 5:
            # is a workday
            bus_day_of_mo += 1
            bus_day_of_year += 1
        if date < start_date:
            date += timedelta(days=1)
            continue
        day_of_year += 1
        dates.append(DateRow(
            len(dates),
            int(date.strftime('%Y%m%d')),
            date,
            date.year,
            qtr,
            'Q%d' % qtr,
            date.month,
            month_name[date.month],
            datetime.date(date.year, date.month, monthrange(date.year, date.month)[1]),
            date.day,
            week_ending(date, week_ends_on='Saturday'),
            (date.weekday() + 1) % 7, # default function has Monday = 0, Sunday = 6
            date.strftime("%A"),
            int(date.strftime("%Y%m")),
            date.strftime("%Y") + ('Q%d' % qtr),
            holiday,
            'Yes' if date.weekday() < 5 else 'No', # is weekday?
            'Yes' if holiday else 'No', # is holiday?
            'Yes' if date.weekday() < 5 and holiday is None else 'No', # is workday?
            1 if date.weekday() < 5 else 0,
            1 if holiday else 0, # num holidays
            1 if not holiday and date.weekday() < 5 else 0, # num workdays
            date.isocalendar()[1],
            None,
            None,
            bus_day_of_mo,
            bus_days_in_month[date.strftime("%Y%m")],
            bus_day_of_year, # business day number of year
            day_of_year, # day number of year
            'Yes' if week_ending(date, week_ends_on='Saturday') == date else 'No', # is last day of week?
            'Yes' if datetime.date(date.year, date.month, monthrange(date.year, date.month)[1]) == date else 'No', # is last day of month?
        ))
        date += timedelta(days=1)
    return dates


def date_table_create_sql(ignore_if_exists: Optional[bool] = True) -> str:
    "Return SQL that can be used to 'create table' for data returned from 'date_table'"
    return '''
Create Table {}dates (
    date_id Integer Not Null Primary Key On Conflict Ignore
  , date_int Integer Not Null Unique
  , date Date Not Null
  , year Integer Not Null
  , quarter_int Integer Not Null
  , quarter Char(2) Not Null
  , month_int Integer Not Null
  , month_name Varchar(20) Not Null
  , month_end Date Not Null
  , day_of_month Integer Not Null
  , week_ending Date Not Null
  , day_of_week_int Integer Not Null
  , day_of_week Varchar(10) Not Null
  , year_month Integer Not Null
  , year_quarter Char(6) Not Null
  , holiday Varchar(30)
  , is_weekday Varchar(3) Not Null
  , is_holiday Varchar(3)
  , is_workday Varchar(3)
  , num_weekdays Boolean Not Null
  , num_holidays Boolean
  , num_workdays Boolean
  , week_num Integer Not Null
  , week_num_of_year Varchar(5)
  , weeks_remaining_in_year Integer
  , workday_day_of_month Integer
  , workdays_in_month Integer
  , workday_number_of_year Integer Not Null
  , day_number_of_year Integer Not Null
  , is_last_day_of_week Boolean Not Null
  , is_last_day_of_month Boolean Not Null
)
'''.format("If Not Exists " if ignore_if_exists else "")


def date_table_insert_sql() -> str:
    return '''
Insert Into dates Values (
    ? , ? , ? , ? , ? , ? , ? , ? , ? , ?
  , ? , ? , ? , ? , ? , ? , ? , ? , ? , ?
  , ? , ? , ? , ? , ? , ? , ? , ? , ? , ?
  , ?
)
'''


def load_date_table(conn: sqlite3.Connection, date_table) -> bool:
    "Create date table and load it with data"
    curs = conn.cursor()
    curs.execute(date_table_create_sql())
    curs.executemany(date_table_insert_sql(), date_table)
    conn.commit()
    return True


def date_table_to_csv(date_table: List[NamedTuple], path: Path, overwrite: bool = False):
    if isinstance(path, str):
        path = Path(path)
    if path.exists():
        if overwrite is False:
            raise FileExistsError(f"Can't overwrite {path}. Delete and try again.")
    with path.open('w', encoding='utf8', newline='') as io:
        writer = csv.writer(io)
        writer.writerow(date_table[0]._fields)
        writer.writerows(date_table)


def eomonth(date: datetime.date, num_months: int = 1) -> datetime.date:
    years = num_months // 12
    months = num_months % 12
    y = date.year + years
    m = (date.month + months - 1) % 12 + 1
    if m < date.month:
        y += 1
    d = monthrange(y, m)[1]
    return datetime.date(y, m, d)


def date_range(fr: datetime.date, to: datetime.date, by = lambda d: d + datetime.timedelta(days=1)) -> List[datetime.date]:
    ds = [fr]
    nxt = by(fr)
    while nxt <= to:
        ds.append(nxt)
        nxt = by(nxt)
    return ds


def by_month(d: datetime.date):
    return eomonth(d, 1)
