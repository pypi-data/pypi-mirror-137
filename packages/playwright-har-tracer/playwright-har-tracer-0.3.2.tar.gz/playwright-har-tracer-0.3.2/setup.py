# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['playwright_har_tracer', 'playwright_har_tracer.dataclasses']

package_data = \
{'': ['*']}

install_requires = \
['dataclasses-json>=0.5.6,<0.6.0', 'python-dateutil>=2.8.2,<3.0.0']

setup_kwargs = {
    'name': 'playwright-har-tracer',
    'version': '0.3.2',
    'description': "A Python implementation version of Playwright's HAR tracer",
    'long_description': '# playwright-har-tracer\n\n[![PyPI version](https://badge.fury.io/py/playwright-har-tracer.svg)](https://badge.fury.io/py/playwright-har-tracer)\n[![Python CI](https://github.com/ninoseki/playwright-har-tracer/actions/workflows/test.yml/badge.svg)](https://github.com/ninoseki/playwright-har-tracer/actions/workflows/test.yml)\n[![Coverage Status](https://coveralls.io/repos/github/ninoseki/playwright-har-tracer/badge.svg?branch=main)](https://coveralls.io/github/ninoseki/playwright-har-tracer?branch=main)\n\nA Python implementation version of Playwright\'s HAR tracer.\nIt is equivalent to playwright `v0.13.x`’s HAR tracer implementation.\n\n## Motivation\n\nPlaywright\'s HAR tracer is implemented to generate HAR as a file. I need to get HAR as a Python object rather than a file.\n\n- `playwright-har-tracer`\'s HarTracer generates HAR as a dataclass object.\n\n## ⚠️ Limitations\n\n- Tested with Python 3.8+\n- Tested with Chromium only\n- Supports the async API only\n\n## Installation\n\n```bash\npip install playwright-har-tracer\n```\n\n## Usage\n\n```python\nimport asyncio\nfrom playwright.async_api import async_playwright\nfrom playwright_har_tracer import HarTracer\n\n\nasync def main():\n    async with async_playwright() as p:\n        browser = await p.chromium.launch()\n        context = await browser.new_context()\n\n        tracer = HarTracer(context=context, browser_name=p.chromium.name)\n\n        page = await context.new_page()\n\n        await page.goto("http://whatsmyuseragent.org/")\n\n        har = await tracer.flush()\n\n        await context.close()\n        await browser.close()\n\n    print(har.to_json())\n\n\nasyncio.run(main())\n```\n',
    'author': 'Manabu Niseki',
    'author_email': 'manabu.niseki@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ninoseki/playwright-har-tracer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
