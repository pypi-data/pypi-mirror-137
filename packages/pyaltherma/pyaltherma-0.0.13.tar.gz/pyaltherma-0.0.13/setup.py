# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyaltherma']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.4,<4.0.0']

setup_kwargs = {
    'name': 'pyaltherma',
    'version': '0.0.13',
    'description': 'Python scripts for controlling Daikin Altherma heat pump using BRP069A62 LAN adapter.',
    'long_description': '# pyaltherma\nPython library to control Daikin Altherma heat pump\nTested only with BRP069A62\n\n# Usage\n\n```python3\nasync with aiohttp.ClientSession() as session:\n    conn = DaikinWSConnection(session, \'IP_ADDRESS\')\n    device = AlthermaController(conn)\n    await device.discover_units()\n    tank = device.hot_water_tank\n    climate = device.climate_control\n    print(f\'Tank / Target temperature: {await tank.tank_temperature} / {await tank.target_temperature}\')\n    print(f"Indoor/outdoor temperature: {await climate.indoor_temperature}/{await climate.outdoor_temperature}")\n    await climate.turn_off()\n    await climate.turn_on()\n    await conn.close()\n```\nsee example.py for more details.\n\n# Status\nCurrently, the implementation is in early stage. At the moment it does not support schedules and energy consumption.\n',
    'author': 'Tadas Danielius',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tadasdanielius/pyaltherma',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
