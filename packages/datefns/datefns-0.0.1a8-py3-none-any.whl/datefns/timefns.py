
import csv
import logging
import os
import sqlite3

__all__ = [
    'time_table',
    'time_table_to_csv',
    'time_table_insert_sql',
    'load_time_table',
]


CREATE_SQL = '''
Create Table If Not Exists time (
    time_key Integer Not Null Primary Key
  , time_24hr Time Not Null Unique
  , hour12 Integer Not Null
  , hour24 Integer Not Null
  , quarter_hour Varchar Not Null Check (quarter_hour In (
      '0–14', '15–29', '30–44', '45–59'
    ))
  , minute Integer Not Null
  , second Integer Not Null
  , second_sequence Integer Not Null Check (second_sequence Between 1 And 86400)
  , period_name Varchar Not Null Check (period_name In (
        '0 - After Midnight'
      , '1 - Early Morning'
      , '2 - Late Morning'
      , '3 - Afternoon'
      , '4 - Evening'
      , '5 - Late Night'
    ))
  , meridiem Char(2) Not Null Check (meridiem In ('AM', 'PM'))
);
'''

INSERT_SQL = '''
Insert Into time (
    time_key
  , time_24hr
  , hour12
  , hour24
  , quarter_hour
  , minute
  , second
  , second_sequence
  , period_name
  , meridiem
) Values (
    ? , ? , ? , ? , ? , ? , ? , ? , ? , ?
) On Conflict Do Nothing
'''

def time_table_insert_sql():
    return INSERT_SQL

def time_table_to_csv(time_table, path_to_csv, overwrite=False):
    if os.path.exists(path_to_csv):
        if overwrite:
            os.remove(path_to_csv)
        else:
            raise OSError(f"'{path_to_csv}' exists and you didn't ask to overwrite")
    with open(path_to_csv, 'w', newline='', encoding='utf-8') as fp:
        writer = csv.writer(fp)
        writer.writerow('time_key time_24hr hour12 hour24 quarter_hour minute second second_sequence period_name meridiem'.split())
        writer.writerows(time_table)
    logging.debug("Wrote time_table to '{path_to_csv}'")


def load_time_table(conn: sqlite3.Connection, time_table) -> bool:
    "Create time table and load it with data"
    with conn:
        curs = conn.cursor()
        curs.execute(CREATE_SQL)
        curs.executemany(INSERT_SQL, time_table)
    return True


def time_table():
    tbl = []
    for hour in range(0, 24):
        for minute in range(0, 60):
            for second in range(0, 60):
                meridiem = 'AM' if hour < 12 else 'PM'
                hour12 = hour if hour < 13 else hour - 12
                hour12 = hour12 if hour12 != 0 else 12
                hour24 = hour
                time24hr = f'{hour:>02d}:{minute:>02d}:{second:>02d}'
                quarter_hour_int = (minute // 15 + 1) * 15
                quarter_hour = f'{quarter_hour_int-15}–{quarter_hour_int-1}'
                second_seq = hour * 60 * 60 + minute * 60 + second + 1
                period_name = ''
                if 0 <= hour < 6:
                    period_name = '0 - After Midnight'
                elif 6 <= hour < 10:
                    period_name = '1 - Early Morning'
                elif 10 <= hour < 12:
                    period_name = '2 - Late Morning'
                elif 12 <= hour < 5+12:
                    period_name = '3 - Afternoon'
                elif 5+12 <= hour < 9+12:
                    period_name = '4 - Evening'
                else:
                    period_name = '5 - Late Night'
                tbl.append([
                    f'{hour:>02d}{minute:>02d}{second:>02d}',
                    time24hr,
                    hour12,
                    hour24,
                    quarter_hour,
                    minute,
                    second,
                    second_seq,
                    period_name,
                    meridiem,
                ])
    return tbl
