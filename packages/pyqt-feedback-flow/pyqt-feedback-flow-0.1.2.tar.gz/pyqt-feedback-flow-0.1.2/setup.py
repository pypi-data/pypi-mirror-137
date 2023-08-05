# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyqt_feedback_flow']

package_data = \
{'': ['*']}

install_requires = \
['PyQt5>=5.15.6,<6.0.0', 'emoji>=1.6.1,<2.0.0']

setup_kwargs = {
    'name': 'pyqt-feedback-flow',
    'version': '0.1.2',
    'description': 'Show feedbacks in toast-like notifications',
    'long_description': '# pyqt-feedback-flow --- Show feedbacks in toast-like notifications\n\n## Motivation\nThis is a very simple module that was developed as a part of our [AST application](https://arxiv.org/pdf/2109.13334.pdf) for showing simple notifications during the cycling training sessions, in order to pass on a cyclist`s essential information, as well as information that can be submitted by a sport trainer.\n\nThis software allows us to show notification in the realm of a text or a picture. It was shown that flowing feedback is\nmore appropriate for a cyclist than static notification or pop up windows. It was tailored to our project, but the project can easily be adjusted for particular special needs. It can also be integrated into existing PyQt projects very easily.\n\nIt was not intended to be released as a separate module, but it may inspire someone to provide updates\nor extensions to this module. Currently, the project is still very immature. It was just used in simple\npractical tests with our AST-GUI.\n\n## Installation\n\n### pip3\n\nInstall this software with pip3:\n\n```sh\npip3 install pyqt-feedback-flow\n```\n\n## License\n\nThis package is distributed under the MIT License. This license can be found online at <http://www.opensource.org/licenses/MIT>.\n\n## Disclaimer\n\nThis framework is provided as-is, and there are no guarantees that it fits your purposes or that it is bug-free. Use it at your own risk!\n',
    'author': 'Iztok Fister Jr.',
    'author_email': 'iztok@iztok-jr-fister.eu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
