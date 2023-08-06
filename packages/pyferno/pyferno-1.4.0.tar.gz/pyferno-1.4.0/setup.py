# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyferno', 'pyferno.tests', 'pyferno.tests.unit']

package_data = \
{'': ['*']}

install_requires = \
['tqdm>=4.62.3,<5.0.0']

setup_kwargs = {
    'name': 'pyferno',
    'version': '1.4.0',
    'description': 'PyFerno - the async/promise library for running Python 3 async tasks',
    'long_description': '# PyFerno - library for working with Python 3 async/await tasks\n\nThe idea of this library is to provide simple methods for working with Lists and Dicts in a simple\n[async/await](https://docs.python.org/3/library/asyncio.html) way in Python. Very important feature is control over\nconcurrency that is implemented by using\n[async Semaphores](https://docs.python.org/3/library/asyncio-sync.html?highlight=semaphore#asyncio.Semaphore).\nControlling concurrency is crucial in case of async tasks because it\'s easy to consume all available IO on your own\nserver or - even worse - on a remote API. It also provides optional progress bar so that user knows what\'s going on and\nhow long it takes.\n\nThe history behind creating this library is my background from Node.js development. Node.js has excellent support for\nasync/await because of its event-based nature.\n\nThere\'s a really great Javascript Promise library [Bluebird](https://github.com/petkaantonov/bluebird). It\'s been used\nas source for inspiration.\n\nThe name "Promise" is also brought over from Javascript world, and it reflects pretty wall what async tasks are -\npromises that may or may not fulfill.\n\nFor those who haven\'t used Javascript promises - you can think of these as "methods that may or may not finish its job\nsome time in the future. But until then lets (a)wait for it. And it doesn\'t block/mess with others in the same time" :)\n\nCurrently, this library exports 2 methods for working with lists and dicts in an async way:\n\n- Promise.all() for working with Lists of tasks\n- Promise.props() for working with Dicts of tasks\n\n# Usage\n\n## With a List of tasks\n\n```\n# this is a working example of await/async with progress bar and controlled concurrency\nimport random\nimport asyncio\nfrom typing import List\nfrom datetime import datetime\nfrom pyferno.promise import Promise\n \nasync def fn() -> List: \n    _start = datetime.utcnow()\n    async def _internal_worker(i:int) -> float:\n        # do something asynchronously\n        _delay = round(random.uniform(0.6, 6.6), 2)\n        await asyncio.sleep(_delay)\n        print(f"Hi, I\'m task #{i} and I slept for {_delay} seconds.")\n        # do some calculations here or whatever and return value ...\n        # for now we just return random float\n        return _delay\n    \n    # let\'s say there is a huge list with data that needs some work to be done\n    some_list_with_data = range(66)\n    tasks = list()\n    for i in some_list_with_data:\n        task = _internal_worker(i)\n        tasks.append(task)\n        \n    out = await Promise.all(tasks, concurrency=8)\n    # try what happens if all tasks are executed in parallel\n    #out = await Promise.all(tasks, concurrency=len(tasks))\n    _end = datetime.utcnow()\n    print(f"All {len(tasks)} tasks done in {_end-_start}.")\n    print(out)\n    return out\n    \nasyncio.run(fn())\n```\n\n## With a Dict of tasks\n\n```\nfrom pyferno.promise import Promise\n\nasync def async_worker_fn():\n    # do something asynchronously\n    return something\n    \ntasks = {\n    "task1": async_worker_fn(),\n    "task2": async_worker_fn(),\n    "task3": async_worker_fn()\n}\nout = await Promise.props(tasks, concurrency=2, progress="A nice progressbar")\nprint(out)\n```\n\n## With a bit more asyncio context\n\n```\nimport asyncio\nfrom pyferno.promise import Promise\n\nasync def async_worker_fn():\n    # do something asynchronously\n    return something\n    \n# this function wraps the main logic into async method   \nasync def main_async_wrapper():\n    tasks = [\n        async_worker_fn(),\n        async_worker_fn(),\n        async_worker_fn()\n    ]\n    out = await Promise.all(tasks, progress="A nice progressbar")\n    return out\n\n# note, this is "normal" synchronous function\ndef main():\n    loop = asyncio.get_event_loop()\n    out = loop.run_until_complete(main_async_wrapper())\n    loop.close()\n    print(out)\n  \nif __name__ == "__main__":\n    main()  \n```\n\n# API\n\n## Promise.all(_Promise__tasks: list, concurrency: int = 10, progress: object = None) -> list\n\nRuns through the list of tasks asynchronously by limiting the concurrency by using a semaphore\n\n    :param __tasks: List of tasks\n    :param concurrency: Concurrency of running tasks, integer. Defaults to 10\n    :param progress: Progress bar message or boolean True to display default progress bar\n    :return: Returns list of finished tasks (fulfilled promises)\n\n## Promise.props(_Promise__props: dict, concurrency: int = 10, progress: object = None) -> dict\n\nRuns through the dict of key,task asynchronously by limiting the concurrency b using a semaphore. Map results back to the\ndictionary with same keys with all tasks fulfilled. It will fail if any task fails\n\n    :param __tasks: Dict with name:task pairs. Task is an async function\n    :param concurrency: Concurrency of running tasks, integer. Defaults to 10\n    :param progress: Progress bar message or boolean True to display default progress bar\n    :return: Returns dict with name:<finished task> pairs.\n\n\n# License\n\nThis library is licensed with MIT license.\n',
    'author': 'Sven Varkel',
    'author_email': 'sven@prototypely.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/pyferno/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
