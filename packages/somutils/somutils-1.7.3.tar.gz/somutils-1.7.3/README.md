# somenergia-utils

This module includes different Python modules and scripts
ubiquiously used on scripts in SomEnergia cooperative
but with no entity by themselves to have their own repository.


- `venv`: run a command under a Python virtual enviroment
- `sql2csv.py`: script to run parametrized sql queries and get the result as (tab separated) csv.
- `dbutils.py`: module with db related functions
	- `fetchNs`: a generator that wraps db cursors to fetch objects with attributes instead of psycopg arrays
	- `nsList`: uses the former to build a list of such object (slower but maybe convinient)
	- `csvTable`: turns the results of a query into a tab separated table with proper header names
- `isodates`: String to time/date/datetime objects with naive/timezoned handling
- `sheetfetcher.py`: convenience class to retrieve data from gdrive spreadshets
- `trace`: quickly enable and disable tracing function calling by decorating them with `@trace`
- `testutils`: module with common test utilities
	- `testutils.assertNsEqual`: structure equality assertion using sorted key yaml dumps
	- `testutils.destructiveTest`: decorator to avoid running destructive tests in production
- `erptree`: extracts an object and its children from the erp (erppeek, odoo)
	with controlled recursion

## `venv` script

Simplifies running a Python script under a given virtual environtment.
This is specially useful to run Python scripts from crontab lines.

```bash
usage: venv /PATH/TO/PYTHON/VIRTUALENV COMMAND [PARAM1 [PARAM2...]]
```

## `sql2csv.py` script

Runs an SQL file and outputs the result of the query as tabulator separated csv.a

A local dbconfig.py file is required, or you should provide it as `-C file.py`
It should contain a dict named `pyscopg` with the keyword parameters to
[psycopg2.connect](https://www.psycopg.org/docs/module.html#psycopg2.connect).

You can provide query parameters either as yamlfile or as commandline options.

```bash
 sql2csv.py <sqlfile> [<yamlfile>] [--<var1> <value1> [--<var2> <value2> ..] ]
```

## `dbutils` Python module

Convenient cursor wrappers to make the database access code more readable.

Example:

```python
import psycopg2, dbutils
db = psycopg2.connect(**dbconfiguration)
with db.cursor() as cursor :
	cursor.execute("SELECT name, age FROM people")
	for person as dbutils.fetchNs(cursor):
		if person.age < 21: continue
		print("{name} is {age} years old".format(person))
```

## `sheetfetcher` Python module

Convenient wraper for gdrive.

```python
from sheetfetcher import SheetFetcher

fetcher = SheetFetcher(
	documentName='My Document',
	credentialFilename='drive-certificate.json',
	)
table = fetcher.get_range("My Sheet", "A2:F12")
fulltable = fetcher.get_fullsheet("My Sheet")
```

- Document selectors can be either an uri or the title
- Sheet selectors can be either an index, a name or an id.
- Range selectors can be either a named range, index tuple or a "A2:F5" coordinates.
- You should [Create a certificate and grant it access to the document](http://gspread.readthedocs.org/en/latest/oauth2.html)

## trace

This decorator is a fast helper to trace calls to functions and methods.
It will show the name of the functions the values of the parameters and the returned values.

```python
from trace import trace

@trace
def factorial(n):
    if n<1: return 1
    return n*factorial(n-1)

factorial(6)

('> factorial', (6,))
('> factorial', (5,))
('> factorial', (4,))
('> factorial', (3,))
('> factorial', (2,))
('> factorial', (1,))
('> factorial', (0,))
('< factorial', (0,), '->', 1)
('< factorial', (1,), '->', 1)
('< factorial', (2,), '->', 2)
('< factorial', (3,), '->', 6)
('< factorial', (4,), '->', 24)
('< factorial', (5,), '->', 120)
('< factorial', (6,), '->', 720)

```

## `testutils.assertNsEqual`

Allows to assert equality on json/yaml like structures combining
dicts, lists, numbers, strings, dates...
The comparision is done on the YAML output so that differences are
spoted as text diffs.
Also keys in dicts are alphabetically sorted.


## `testutils.destructiveTest`

An utility to avoid running destrutive tests in production.
It is a decorator that checks wheter the erp configured in `dbconfig`
has the testing flag and skips the test if it doesn't.

The script `enable_destructive_test.py` is also provided to set/unset
that testing flag which is not defined by default.

## `isodates`

Module for simplified isodate parsing and timezone handling.


## `sequence`

Interprets strings like the ones the standard Print Dialog
uses to specify pages to be printed.
ie. "2,4,6-9,13" means "2, 4, from 6 to 9 and 13"

## `erptree`

Creates an structure from ERP objects that you can navigate
or dump as yaml.
You can select fields to expand, taking just the name or the id,
anonymize or removing.
You can use dot notation to specify fields in related objects.
For multiple relations, a subfield refers to the subfield in
all related objects.


```python
from somutils.erptree import erptree

O = Client(....)

partner = erptree(partnerAddress_id, O.ResPartnerAddress,
	expand = {
		'partner_id': O.ResPartner,
		'partner_id.company': O.ResPartner,
	},
	pickName = [
		'partner_id.state_id',
		'partner_id.country_id',
	],
	anonymize = [
		'email',
	],
	remove = [
		'superfluous_field',
	],
)
	
```







