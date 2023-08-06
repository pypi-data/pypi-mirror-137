# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['stopwatch']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.4,<0.5.0']

setup_kwargs = {
    'name': 'python-stopwatch2',
    'version': '1.0.10',
    'description': 'A simple stopwatch for measuring code performance with static typing.',
    'long_description': "# Python-Stopwatch2\n\nA simple stopwatch for measuring code performance. This is a fork from [python-stopwatch](https://pypi.org/project/python-stopwatch/), which adds static typing and a few other things.\n\n## Usage\n\n### Installation\n\nTo install the library, you can just run the following command:\n\n```shell\npoetry add python-stopwatch2\n```\n\nOr, using pip:\n\n```shell\npip install python-stopwatch2\n```\n\n### Basic usage\n\n#### stopwatch.Stopwatch\n\nYou can use the [start()](https://github.com/devRMA/python-stopwatch2/tree/main/docs#stopwatchstart) and [stop](https://github.com/devRMA/python-stopwatch2/tree/main/docs#stopwatchstop) methods to starts or stops the stopwatch counter.\n\n```python\nfrom time import sleep\n\nfrom stopwatch import Stopwatch\n\nmy_stopwatch = Stopwatch()\nsleep(2)\nmy_stopwatch.stop()\nprint(my_stopwatch.elapsed)  # 2.00027129999944\nsleep(1)\nprint(my_stopwatch.elapsed)  # 2.00027129999944\nmy_stopwatch.start()\nsleep(1)\nmy_stopwatch.stop()\nprint(my_stopwatch.elapsed)  # 3.0158972999997786\nprint(f'Time elapsed: {my_stopwatch}')  # Time elapsed: 3.02s\n```\n\nIt is also possible to use [Stopwatch](https://github.com/devRMA/python-stopwatch2/tree/main/docs#stopwatchstopwatch) with the [with statement](https://www.geeksforgeeks.org/with-statement-in-python/).\n\n```python\nfrom time import sleep\n\nfrom stopwatch import Stopwatch\n\nwith Stopwatch() as my_stopwatch:\n    sleep(3)\nprint(my_stopwatch.elapsed)  # 3.0012330539993854\nprint(f'Time elapsed: {my_stopwatch}')  # Time elapsed: 3.00s\n```\n\nIf you want to print the elapsed time at the end of [with statement](https://www.geeksforgeeks.org/with-statement-in-python/), you can pass the second parameter at stopwatch startup, as True\n\n```python\nfrom time import sleep\n\nfrom stopwatch import Stopwatch\n\nwith Stopwatch('my custom message', True):\n    sleep(3)\n# [__main__:<module>:5] ~ 3.00s - my custom message\n```\n\n#### stopwatch.profile\n\nThis decorator is used to profile a function. It will print a report every time the function is called and, at the end of the execution, the final report will be printed.\n\n```python\nfrom time import sleep\n\nfrom stopwatch import profile\n\n\n@profile(name='My function')\ndef wait_for(time: float) -> None:\n    sleep(time)\n\n\nfor time in [0.1, 0.2, 0.3, 0.4, 0.5]:\n    wait_for(time)\nprint('end')\n\n# [__main__#My function] hits=1, mean=100.14ms, min=100.14ms, median=100.14ms, max=100.14ms, dev=0.00μs\n# [__main__#My function] hits=2, mean=150.20ms, min=100.14ms, median=150.20ms, max=200.26ms, dev=50.06ms\n# [__main__#My function] hits=3, mean=200.25ms, min=100.14ms, median=200.26ms, max=300.35ms, dev=81.74ms\n# [__main__#My function] hits=4, mean=250.30ms, min=100.14ms, median=250.30ms, max=400.44ms, dev=111.92ms\n# [__main__#My function] hits=5, mean=300.35ms, min=100.14ms, median=300.35ms, max=500.55ms, dev=141.56ms\n# end\n# [__main__#My function] hits=5, mean=300.35ms, min=100.14ms, median=300.35ms, max=500.55ms, dev=141.56ms\n```\n\nIf the ``name`` parameter is not informed, it will use the function name.\n\nIt is also possible to pass the ``report_every`` parameter (which by default is 1) which informs how many times the report should be printed. If ``None`` is passed, the report will only be printed at the end of the execution.\n\n```python\nfrom time import sleep\n\nfrom stopwatch import profile\n\n\n@profile(report_every=2)\ndef report_every2(time: float) -> None:\n    sleep(time)\n\n\n@profile(report_every=None)\ndef no_report(time: float) -> None:\n    sleep(time)\n\n\nfor time in [0.1, 0.2, 0.3, 0.4, 0.5]:\n    report_every2(time)\n    no_report(time)\nprint('end')\n\n# [__main__#report_every2] hits=2, mean=150.20ms, min=100.15ms, median=150.20ms, max=200.25ms, dev=50.05ms\n# [__main__#report_every2] hits=4, mean=250.30ms, min=100.15ms, median=250.30ms, max=400.46ms, dev=111.92ms\n# end\n# [__main__#no_report] hits=5, mean=300.36ms, min=100.15ms, median=300.36ms, max=500.58ms, dev=141.57ms\n# [__main__#report_every2] hits=5, mean=300.43ms, min=100.15ms, median=300.36ms, max=500.94ms, dev=141.68ms\n```\n\n#### stopwatch.stopwatch\n\nThis class is to be used with [with statement](https://www.geeksforgeeks.org/with-statement-in-python/) and will print the time it took to execute the code.\n\n```python\nfrom time import sleep\n\nfrom stopwatch import stopwatch\n\nwith stopwatch():\n    sleep(0.5)\n\n# [__main__:<module>:5] ~ 500.27ms\n```\n",
    'author': 'Rafael',
    'author_email': 'contact.devrma@gmail.com',
    'maintainer': 'Rafael',
    'maintainer_email': 'contact.devrma@gmail.com',
    'url': 'https://github.com/devRMA/python-stopwatch2',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
