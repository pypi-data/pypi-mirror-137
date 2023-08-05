# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['jack_server']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'jack-server',
    'version': '0.0.2',
    'description': 'Control JACK server with Python',
    'long_description': '# Control JACK Server with Python\n\n📝 Project is in alpha stage.\n\n## Installation\n\n```bash\npip install jack_server\n```\n\n## Usage\n\n```python\nimport time\n\nfrom jack_server import Server\n\nserver = Server(\n    driver="coreaudio",\n    device="BuiltInSpeakerDevice",\n    rate=48000,\n    sync=True,\n)\nserver.start()\n\nwhile True:\n    time.sleep(1)\n```\n',
    'author': 'Lev Vereshchagin',
    'author_email': 'mail@vrslev.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
