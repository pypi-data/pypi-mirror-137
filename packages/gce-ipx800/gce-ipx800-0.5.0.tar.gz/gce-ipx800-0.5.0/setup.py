# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ipx800']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.26,<3.0']

setup_kwargs = {
    'name': 'gce-ipx800',
    'version': '0.5.0',
    'description': 'Library to interact with the GCE Electronics IPX800 device',
    'long_description': 'GCE-IPX800\n==========\n\n.. image:: https://img.shields.io/pypi/v/gce-ipx800?color=blue\n   :alt: Pypi version\n   :target: https://pypi.org/project/gce-ipx800/\n\n.. image:: https://github.com/marcaurele/gce-ipx800/workflows/Build%20status/badge.svg\n   :alt: Build Status\n   :target: https://github.com/marcaurele/gce-ipx800/actions\n\n.. image:: https://codecov.io/gh/marcaurele/gce-ipx800/branch/master/graph/badge.svg\n   :alt: Code coverage\n   :target: https://codecov.io/gh/marcaurele/gce-ipx800\n\n.. image:: https://img.shields.io/pypi/l/gce-ipx800.svg\n   :alt: License\n   :target: https://pypi.org/project/gce-ipx800/\n\n.. image:: https://img.shields.io/pypi/pyversions/gce-ipx800.svg\n   :alt: Python versions\n   :target: https://pypi.org/project/gce-ipx800/\n\nA python library to control a GCE-Electronics IPX800 V4 device through its API.\n\n* Python 3.8+ support\n* Apache License\n\nIPX800 features implemented\n---------------------------\n\n* Analog sensors (``ipx.analogs[]``)\n* Control:\n\n  - relays (``ipx.relays[]``)\n  - virtual inputs (``ipx.virtual_inputs[]``)\n  - virtual outputs (``ipx.virtual_outputs[]``)\n\n* Counters (``ipx.counters[]``)\n\nInstallation\n------------\n\n.. code-block:: console\n\n    > pip install gce-ipx800\n\nUsage\n-----\n\n.. note:: The default API key of the device is `apikey`.\n\n.. code-block:: python\n\n    from ipx800 import ipx800\n\n    ipx = ipx800("http://your-device-ip", "apikey")\n\n    r4 = ipx.relays[3]\n\n    r4.status  # => return a Boolean\n\n    r4.on()\n\n    r4.off()\n\n    r4.togle()\n\n    len(ipx.relays)  # => 56\n\nLinks\n-----\n\n* GCE IPX800 V4 API: https://gce.ovh/wiki/index.php?title=API_V4\n\nLicence\n-------\n\nLicensed under Apache License Version 2.0\n',
    'author': 'Marc-Aurèle Brothier',
    'author_email': 'm@brothier.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/marcaurele/gce-ipx800',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
