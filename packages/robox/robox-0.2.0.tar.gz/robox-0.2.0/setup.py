# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['robox']

package_data = \
{'': ['*']}

install_requires = \
['aiofiles>=0.8.0,<0.9.0',
 'beautifulsoup4>=4.9.3,<5.0.0',
 'httpx-cache>=0.4.0,<0.5.0',
 'httpx>=0.21.1,<0.22.0',
 'tenacity>=8.0.1,<9.0.0']

setup_kwargs = {
    'name': 'robox',
    'version': '0.2.0',
    'description': 'Robox is a simple library for exploring/scraping the web or testing a website you’re developing.',
    'long_description': '[![codecov](https://codecov.io/gh/danclaudiupop/robox/branch/main/graph/badge.svg?token=2DR9K7DR0V)](https://codecov.io/gh/danclaudiupop/robox)\n[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/danclaudiupop/robox.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/danclaudiupop/robox/context:python)\n[![Run tests](https://github.com/danclaudiupop/robox/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/danclaudiupop/robox/actions/workflows/ci.yml)\n[![view examples](https://img.shields.io/badge/learn%20by-examples-0077b3.svg)](https://github.com/danclaudiupop/robox/tree/main/examples)\n[![PyPI version](https://badge.fury.io/py/robox.svg)](https://badge.fury.io/py/robox)\n\n## Overview\nRobox is a simple library with a clean interface for exploring/scraping the web or testing a website you’re developing. Robox can fetch a page, click on links and buttons, and fill out and submit forms. Robox is built on top of two excelent libraries: [httpx](https://www.google.com) and [beautifulsoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/).\n\n---\nRobox has all the standard features of httpx, including async, plus:\n- clean api\n- caching\n- downloading files\n- history\n- retry\n- understands robots.txt\n\n\n## Examples\n\n```python\nfrom robox import Robox\n\n\nwith Robox() as robox:\n    page = robox.open("https://httpbin.org/forms/post")\n    form = page.get_form()\n    form.fill_in("custname", value="foo")\n    form.check("topping", values=["Onion"])\n    form.choose("size", option="Medium")\n    form.fill_in("comments", value="all good in the hood")\n    form.fill_in("delivery", value="13:37")\n    page = page.submit_form(form)\n    assert page.url == "https://httpbin.org/post"\n```\n\nor use async version:\n\n```python\nimport asyncio\n\nfrom pprint import pprint\nfrom robox import AsyncRobox\n\n\nasync def main():\n    async with AsyncRobox(follow_redirects=True) as robox:\n        page = await robox.open("https://www.google.com")\n        form = page.get_form()\n        form.fill_in("q", value="python")\n        consent_page = await page.submit_form(form)\n        form = consent_page.get_form()\n        page = await consent_page.submit_form(form)\n        pprint(list(page.get_links_by_text("python")))\n\n\nasyncio.run(main())\n```\n\nCaching can be easily configured via [httpx-cache](https://obendidi.github.io/httpx-cache/)\n\n```python\nfrom robox import Robox, DictCache, FileCache\n\n\nwith Robox(options=Options(cache=DictCache())) as robox:\n    p1 = robox.open("https://httpbin.org/get")\n    assert not p1.from_cache\n    p2 = robox.open("https://httpbin.org/get")\n    assert p2.from_cache\n```\n\nFailed requests that are potentially caused by temporary problems such as a connection timeout or HTTP 500 error can be retried:\n\n```python\nwith Robox(\n    options=Options(\n        retry=True,\n        retry_max_attempts=2,\n        raise_on_4xx_5xx=True,\n    )\n) as robox:\n    page = robox.open("https://httpbin.org/status/503,200")\n    assert page.status_code == 200\n```\n\nSee [examples](https://github.com/danclaudiupop/robox/tree/main/examples) folder for more detailed examples.\n\n## Installation\n\nUsing pip:\n\n```sh\npip install robox\n```\n\nRobox requires Python 3.8+.\nSee [Changelog](https://github.com/danclaudiupop/robox/blob/main/CHANGELOG.md) for changes.\n',
    'author': 'Dan Claudiu Pop',
    'author_email': 'danclaudiupop@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/danclaudiupop/robox',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
