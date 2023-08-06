# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['timeless']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.3.4,<2.0.0', 'python-dateutil>=2.8.2,<3.0.0']

setup_kwargs = {
    'name': 'timeless',
    'version': '0.1.5',
    'description': 'A datetime toolkit for people in a hurry.',
    'long_description': '# Timeless: datetime for people in a hurry\n\nA datetime toolkit for people in a hurry. It provides a simple API, heavily inspired by [Pendulum](https://github.com/sdispater/pendulum).\n\nTimeless is a work in progress.\n\n## 🧠 Features\n\n- ✔️ very simple API\n- ✔️ easy to extend and use with other packages\n- ✔️ built on top of standard packages and [dateutil](https://github.com/dateutil/dateutil)\n\n## 📦 Installation\n\n```bash\npip install timeless\n```\n\n## 📝 Why Timeless?\n\nI love Pendulum, although since last year it doesn\'t seem to be actively maintained. If you like Pendulum, you will like Timeless. If you want a easy to adopt, integrate and expand package, you will like Timeless.\n\n## 💻 Examples of usage\n\nTimeless use two main concepts: `Datetime` and `Period`. A datetime is a point in Time, and a Period is a duration.\n\nTimeless doesn`t differentiate between datetime and date objects.\n\nAll datetimes are assumed to be in the UTC+00:00 timezone if any other timezone isn`t specified.\n\n---\n\n### Datetime\n\n```python\nimport timeless\n\nstart = timeless.datetime(1900, 1, 1, zone="UTC")\nend = start.add(years=1)\n\nend.subtract(months=1)\n\nstart.set(year=2099, month=2, day=26, hour=5, zone="America/Sao_Paulo")\n\nstart.is_past()  # True\nstart.is_future()  # False\nstart.set(year=2099).is_future()  # True\n```\n\nSurely, you can get the current time:\n\n```python\ntimeless.today()\ntimeless.now()\n```\n\nTimeless heavily uses [dateutil](https://github.com/dateutil/dateutil). The difference between two dates gives you a relativedelta object:\n\n```python\nstart.diff(end)\n```\n\n### Periods\n\nCreate a date range with `Period`:\n\n```python\nperiod_1 = timeless.period(start, end, freq="days")\nperiod_2 = period_1.compute()\n```\n\nPeriods are always yielded. Use compute or just list(period) to get the list of datetimes.\n\nTo easily change the frequency of a date range, use `to`:\n\n```python\nperiod_1.to("hours")\n```\n\n### Using Timeless and Pandas\n\nWho else loves Pandas? The ones who says doens`t like Pandas probabily never used it for real. Timeless has some basic Pandas Timestamp compatibility methods.\n\n```python\nimport pandas as pd\n\npd_timestamp = pd.Timestamp(\'1900-01-01 00:00:00\', tz=None)\npd_daterange = pd.date_range(pd_timestamp, periods=2, freq="MS")\n\ntimeless.from_pandas(pd_timestamp)\ntimeless.from_pandas(pd_daterange)\n\ntimeless.to_pandas(period_1)\n```\n\nNote that only the main Pandas freqs are implemented: D, W, M, A/ Y, H, T/min, S and U/ US. Freqs like MS, AS and YS are coerced to months and years, respectively.\n\n### Utilitaries\n\nParse some strings to datetime:\n\n```python\nfill_date = timeless.datetime(2099, 2, 26, zone="UTC")\ntimeless.parse("1900", zone="America/Sao_Paulo", fill=fill_date)\n```\n\nOr get it as a ISO 8601 string or any other format:\n\n```python\ntimeless.now().format()\ntimeless.now().format("%Y-%m-%d %H:%M:%S")\n```\n\nOr find the next friday!\n\n```python\ntimeless.now().get_next("friday")\n```\n\nTimeless tries to be as flexible as possible. You can create some quite cool chain operations easily:\n\n```python\ntimeless.period(start, end.add(days=7), freq="days").to("weeks").compute()\n```\n\n## 🏗️ Development\n\nTimeless relies on [Poetry](https://github.com/python-poetry/poetry).\n\nInstall the Python dependencies with:\n\n```bash\npoetry install\n```\n\n## ⚗️ Testing\n\n```bash\npoetry run pytest --cov=timeless tests/\n```\n',
    'author': 'ericmiguel',
    'author_email': 'ericmiguel@id.uff.br',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ericmiguel/timeless',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
