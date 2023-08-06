================
datefns Overview
================

Seems like I constantly need some kind of date functions that aren't found (or
aren't found easily enough anyway) in the standard library or in 3rd party
packages that I use regularly. This library attempts to remedy that so I know
where to add the functions when I build them and know where to look for them
when I need them.

Getting Started
===============

There are no dependancies to install. You just need to::

    pip install datefns

or::

    git clone git@github.com:ktr/datefns.git
    cd datefns
    python setup.py install


Once installed, you can iterate through the entire file without using much
memory by doing the following::

    import datefns, datetime
    d1 = datetime.date(2018, 7, 10)
    d2 = datetime.date(2018, 12, 31)
    we = datefns.week_ending(d1, week_ends_on='Sun')
    ds = datefns.date_table(d1, d2)
    me = datefns.eomonth(d1, 5) # datetime.date(2018, 12, 31)

    datefns.date_table_to_csv(ds, '/path/to/file.csv', overwrite=True)

    import sqlite3
    conn = sqlite3.connect(':memory:')
    datefns.load_date_table(conn, start_date=d1, end_date=d2)

    ds = datefns.date_range(d1, d2, datefns.by_month)

Running Tests
=============

To run tests::

    python -m tests.test_datefns

License
=======

The project is licensed under the MIT License - see the LICENSE.md_ file for
details

.. _license.md: /LICENSE.txt
