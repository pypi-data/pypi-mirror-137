# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mytoyota', 'mytoyota.models', 'mytoyota.utils']

package_data = \
{'': ['*']}

install_requires = \
['arrow>=1.1,<2.0', 'httpx>=0.18.1', 'langcodes>=3.1,<4.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=1.0,<2.0']}

setup_kwargs = {
    'name': 'mytoyota',
    'version': '0.8.0',
    'description': 'Python client for Toyota Connected Services.',
    'long_description': '[![GitHub Workflow Status][workflow-shield]][workflow]\n[![GitHub Release][releases-shield]][releases]\n[![GitHub Activity][commits-shield]][commits]\n\n# Toyota Connected Services Python module\n\n### [!] **This is still in beta**\n\n## Description\n\nPython 3 package to communicate with Toyota Connected Services.\nThis is an unofficial package and Toyota can change their API at any point without warning.\n\n## Installation\n\nThis package can be installed through `pip`.\n\n```text\npip install mytoyota\n```\n\n## Usage\n\n```python\nimport json\nimport asyncio\nfrom mytoyota.client import MyT\n\nusername = "jane@doe.com"\npassword = "MyPassword"\n\n# Get supported regions, can be passed to the optional \'region\' argument of MyT\nprint(MyT.get_supported_regions())\n\nclient = MyT(username=username, password=password)\n\n\nasync def get_information():\n    print("Logging in...")\n    await client.login()\n\n    print("Retrieving cars...")\n    # Returns cars registered to your account + information about each car.\n    cars = await client.get_vehicles()\n\n    for car in cars:\n\n        # Returns live data from car/last time you used it as an object.\n        vehicle = await client.get_vehicle_status(car)\n\n        # You can either get them all async (Recommended) or sync (Look further down).\n        data = await asyncio.gather(\n            *[\n                client.get_driving_statistics(vehicle.vin, interval="day"),\n                client.get_driving_statistics(vehicle.vin, interval="isoweek"),\n                client.get_driving_statistics(vehicle.vin),\n                client.get_driving_statistics(vehicle.vin, interval="year"),\n            ]\n        )\n\n        # You can access odometer data like this:\n        mileage = vehicle.dashboard.odometer\n        # Or retrieve the energy level (electric or gasoline)\n        fuel = vehicle.dashboard.fuel_level\n        battery = vehicle.dashboard.batter_level\n        # Or Parking information:\n        latitude = vehicle.parkinglocation.latitude\n\n        # Daily stats\n        daily_stats = await client.get_driving_statistics(vehicle.vin, interval="day")\n\n        # ISO 8601 week stats\n        iso_weekly_stats = await client.get_driving_statistics(vehicle.vin, interval="isoweek")\n\n        # Monthly stats is returned by default\n        monthly_stats = await client.get_driving_statistics(vehicle.vin)\n\n        # Get year to date stats.\n        yearly_stats = await client.get_driving_statistics(vehicle.vin, interval="year")\n\n\nloop = asyncio.get_event_loop()\nloop.run_until_complete(get_information())\nloop.close()\n\n```\n\n## Known issues\n\n- Statistical endpoint will return `None` if no trip have been performed in the requested timeframe. This problem will often happen at the start of each week, month or year. Also daily stats will of course also be unavailable if no trip have been performed.\n\n## Docs\n\nComing soon...\n\n## Contributing\n\nThis python module uses poetry and pre-commit.\n\nTo start contributing, fork this repository and run `poetry install`. Then create a new branch. Before making a PR, please run pre-commit `poetry run pre-commit run --all-files` and make sure that all tests passes locally first.\n\n## Note\n\nAs I [@DurgNomis-drol](https://github.com/DurgNomis-drol) am not a professional programmer. I will try to maintain it as best as I can. If someone is interested in helping with this, they are more the welcome to message me to be a collaborator on this project.\n\n## Credits\n\nA huge thanks go to [@calmjm](https://github.com/calmjm) for making [tojota](https://github.com/calmjm/tojota).\n\n[releases-shield]: https://img.shields.io/github/release/DurgNomis-drol/mytoyota.svg?style=for-the-badge\n[releases]: https://github.com/DurgNomis-drol/mytoyota/releases\n[workflow-shield]: https://img.shields.io/github/workflow/status/DurgNomis-drol/mytoyota/Linting?style=for-the-badge\n[workflow]: https://github.com/DurgNomis-drol/mytoyota/actions\n[commits-shield]: https://img.shields.io/github/commit-activity/y/DurgNomis-drol/mytoyota.svg?style=for-the-badge\n[commits]: https://github.com/DurgNomis-drol/mytoyota/commits/master\n',
    'author': 'Simon Grud Hansen',
    'author_email': 'simongrud@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/DurgNomis-drol/mytoyota',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
