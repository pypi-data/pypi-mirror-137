# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['FoldingAtHomeControl']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pyfoldingathomecontrol',
    'version': '2.1.1',
    'description': 'Python library to get stats from your Folding@Home Clients',
    'long_description': '# PyFoldingAtHomeControl\n\nPython library to get stats from your Folding@Home Clients\n\n[![GitHub Actions](https://github.com/eifinger/PyFoldingAtHomeControl/workflows/Python%20package/badge.svg)](https://github.com/eifinger/PyFoldingAtHomeControl/actions?workflow=Python+package)\n[![PyPi](https://img.shields.io/pypi/v/PyFoldingAtHomeControl.svg)](https://pypi.python.org/pypi/PyFoldingAtHomeControl)\n[![PyPi](https://img.shields.io/pypi/l/PyFoldingAtHomeControl.svg)](https://github.com/eifinger/PyFoldingAtHomeControl/blob/master/LICENSE)\n[![codecov](https://codecov.io/gh/eifinger/PyFoldingAtHomeControl/branch/master/graph/badge.svg)](https://codecov.io/gh/eifinger/PyFoldingAtHomeControl)\n[![Downloads](https://pepy.tech/badge/pyfoldingathomecontrol)](https://pepy.tech/project/pyfoldingathomecontrol)\n\n## Installation\n\n```bash\npip install PyFoldingAtHomeControl\n```\n\n## Usage\n\n```python\nimport asyncio\nfrom FoldingAtHomeControl import FoldingAtHomeController\nfrom FoldingAtHomeControl import PyOnMessageTypes\n\n\ndef callback(message_type, data):\n    print(f"callback for: {message_type}: ", data)\n\n\nasync def cancel_task(task_to_cancel):\n    task_to_cancel.cancel()\n    await task_to_cancel\n\n\nif __name__ == "__main__":\n    Controller = FoldingAtHomeController("localhost")\n    Controller.register_callback(callback)\n    loop = asyncio.get_event_loop()\n    task = loop.create_task(Controller.start())\n    try:\n        loop.run_until_complete(task)\n    except KeyboardInterrupt:\n        pass\n    finally:\n        print("Cancelling task")\n        try:\n            loop.run_until_complete(cancel_task(task))\n        except asyncio.CancelledError:\n            print("Closing Loop")\n            loop.close()\n```\n',
    'author': 'Kevin Stillhammer',
    'author_email': 'kevin.stillhammer@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://github.com/eifinger/PyFoldingAtHomeControl',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
