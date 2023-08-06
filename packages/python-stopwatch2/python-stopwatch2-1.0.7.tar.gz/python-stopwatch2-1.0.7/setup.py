# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['stopwatch', 'stopwatch.contextmanagers']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.4,<0.5.0']

setup_kwargs = {
    'name': 'python-stopwatch2',
    'version': '1.0.7',
    'description': 'A simple stopwatch for measuring code performance with static typing.',
    'long_description': "# Python-Stopwatch2\n\nA simple stopwatch for measuring code performance. This is a fork from [python-stopwatch](https://pypi.org/project/python-stopwatch/), which adds static typing and a few other things.\n\n## Installing\n\nTo install the library, you can just run the following command:\n\n```shell\n# Linux/macOS\npython3 -m pip install git+https://github.com/devRMA/python-stopwatch2.git\n\n# Windows\npy -3 -m pip install git+https://github.com/devRMA/python-stopwatch2.git\n```\n\n## Examples\n\n```python\nimport time\nfrom stopwatch import Stopwatch, profile\n\nstopwatch = Stopwatch()\nstopwatch.start()\ntime.sleep(3.0)\nstopwatch.stop()\nprint(stopwatch.elapsed) # 3.003047182224691\n\nwith Stopwatch() as stopwatch2:\n    time.sleep(3)\nprint(f'Time elapsed: {stopwatch2}') # Time elapsed: 3.0030s\n\nwith Stopwatch(name='outer') as outer_stopwatch:\n    with Stopwatch(name='inner') as inner_stopwatch:\n        for i in range(5):\n            with inner_stopwatch.lap():\n                time.sleep(i / 10)\nprint(inner_stopwatch.elapsed) # 1.0013675531372428\nprint(inner_stopwatch.laps) # [3.256136551499367e-05, 0.10015189787372947, 0.20030939625576138, 0.3003752687945962, 0.40049842884764075]\nprint(outer_stopwatch.report()) # [Stopwatch#outer] total=1.0015s\nprint(inner_stopwatch.report()) # [Stopwatch#inner] total=1.0014s, mean=0.2003s, min=0.0000s, median=0.2003s, max=0.4005s, dev=0.1416s\n\n\n@profile()\ndef wait_for(ts):\n    if not ts:\n        return\n\n    time.sleep(ts[0])\n    wait_for(ts[1:])\n\nwait_for([0.1, 0.2, 0.3, 0.4, 0.5])\n# [__main__#wait_for] hits=1, mean=0.02ms, min=0.02ms, median=0.02ms, max=0.02ms, dev=0.00ms\n# [__main__#wait_for] hits=2, mean=0.2507s, min=0.02ms, median=0.2507s, max=0.5014s, dev=0.2507s\n# [__main__#wait_for] hits=3, mean=0.4680s, min=0.02ms, median=0.5014s, max=0.9026s, dev=0.3692s\n# [__main__#wait_for] hits=4, mean=0.6519s, min=0.02ms, median=0.7020s, max=1.2036s, dev=0.4513s\n# [__main__#wait_for] hits=5, mean=0.8024s, min=0.02ms, median=0.9026s, max=1.4046s, dev=0.5036s\n# [__main__#wait_for] hits=6, mean=0.9196s, min=0.02ms, median=1.0531s, max=1.5055s, dev=0.5291s\n# [__main__#wait_for] hits=6, mean=0.9196s, min=0.02ms, median=1.0531s, max=1.5055s, dev=0.5291s\n\n\n@profile(name='wait for ts')\ndef wait_for(ts):\n    if not ts:\n        return\n\n    time.sleep(ts[0])\n    wait_for(ts[1:])\n\nwait_for([0.1, 0.2, 0.3, 0.4, 0.5])\n# [__main__#wait for ts] hits=1, mean=0.01ms, min=0.01ms, median=0.01ms, max=0.01ms, dev=0.00ms\n# [__main__#wait for ts] hits=2, mean=0.2505s, min=0.01ms, median=0.2505s, max=0.5009s, dev=0.2505s\n# [__main__#wait for ts] hits=3, mean=0.4675s, min=0.01ms, median=0.5009s, max=0.9017s, dev=0.3689s\n# [__main__#wait for ts] hits=4, mean=0.6513s, min=0.01ms, median=0.7013s, max=1.2024s, dev=0.4509s\n# [__main__#wait for ts] hits=5, mean=0.8016s, min=0.01ms, median=0.9017s, max=1.4031s, dev=0.5031s\n# [__main__#wait for ts] hits=6, mean=0.9186s, min=0.01ms, median=1.0521s, max=1.5037s, dev=0.5286s\n# [__main__#wait for ts] hits=6, mean=0.9186s, min=0.01ms, median=1.0521s, max=1.5037s, dev=0.5286s\n\n\n\n@profile(name='wait for ts', report_every=2)\ndef wait_for(ts):\n    if not ts:\n        return\n\n    time.sleep(ts[0])\n    wait_for(ts[1:])\n\nwait_for([0.1, 0.2, 0.3, 0.4, 0.5])\n# [__main__#wait for ts] hits=2, mean=0.2504s, min=0.01ms, median=0.2504s, max=0.5007s, dev=0.2503s\n# [__main__#wait for ts] hits=4, mean=0.6513s, min=0.01ms, median=0.7014s, max=1.2025s, dev=0.4510s\n# [__main__#wait for ts] hits=6, mean=0.9188s, min=0.01ms, median=1.0523s, max=1.5039s, dev=0.5287s\n# [__main__#wait for ts] hits=6, mean=0.9176s, min=0.01ms, median=1.0510s, max=1.5018s, dev=0.5279s\n\n\n@profile(name='wait for ts', report_every=None)\ndef wait_for(ts):\n    if not ts:\n        return\n\n    time.sleep(ts[0])\n    wait_for(ts[1:])\n\nwait_for([0.1, 0.2, 0.3, 0.4, 0.5])\n# [__main__#wait for ts] hits=6, mean=0.9188s, min=0.01ms, median=1.0523s, max=1.5039s, dev=0.5287s\n\n\nwith stopwatch():\n    for i in range(5):\n        time.sleep(i / 10)\n# [__main__:<module>:1] ~ 1.0013s\n\n\nwith stopwatch('with message'):\n    for i in range(5):\n        time.sleep(i / 10)\n# [__main__:<module>:1] ~ 1.0013s - with message\n```\n",
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
