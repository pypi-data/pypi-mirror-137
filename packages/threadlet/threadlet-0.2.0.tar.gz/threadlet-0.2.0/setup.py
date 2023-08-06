# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['threadlet']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'threadlet',
    'version': '0.2.0',
    'description': 'Improved `Thread` and `ThreadPoolExecutor` classes.',
    'long_description': '# Threadlet\n\nImproved `Thread` and `ThreadPoolExecutor` classes.\n\n---\n\n### Installation\n`pip3 install threadlet`\n\n### Features\n\n- ThreadPoolExecutor with improved workers performance (fixed IDLE semaphore) and new features:\n```python\nimport time\nimport threading\nfrom threadlet.executor import ThreadPoolExecutor\n\nMAX_WORKERS = 4\nMIN_WORKERS = 2\nWORK_TIME = 0.5\nIDLE_TIMEOUT = 1\n\n# "idle_timeout" argument:\n# workers are going to die after doing nothing for "idle_timeout" time.\nwith ThreadPoolExecutor(MAX_WORKERS, idle_timeout=IDLE_TIMEOUT) as tpe:\n    assert threading.active_count() == 1\n    for _ in range(2):\n        for _ in range(MAX_WORKERS):\n            tpe.submit(time.sleep, WORK_TIME)\n        assert threading.active_count() == MAX_WORKERS + 1\n        time.sleep(WORK_TIME + IDLE_TIMEOUT + 1)  # wait until workers die on timeout\n        assert threading.active_count() == 1\n\n# "min_workers" argument:\n# amount of workers which are pre-created at start and not going to die ever in despite of "idle_timeout".\nwith ThreadPoolExecutor(MAX_WORKERS, min_workers=MIN_WORKERS, idle_timeout=IDLE_TIMEOUT) as tpe:\n    assert threading.active_count() == MIN_WORKERS + 1\n    for _ in range(MAX_WORKERS):\n        tpe.submit(time.sleep, WORK_TIME)\n    assert threading.active_count() == MAX_WORKERS + 1\n    time.sleep(WORK_TIME + MIN_WORKERS + 1)  # wait until workers die on timeout\n    assert threading.active_count() == MIN_WORKERS + 1\n```\n\n- Threads with results:\n\n```python\nfrom threadlet.thread import Thread\n\n# threads now have "future" attribute of type concurrent.futures.Future.\n# usage:\nthread = Thread(target=sum, args=([1, 1],))\nthread.start()\ntry:\n    assert thread.future.result(1) == 2\nfinally:\n    thread.join()  # pay attention that "future" attribute won\'t be available after joining\n    # thread.future.result(1) #  raises AttributeError\n\n# equals to:\nwith Thread(target=sum, args=([1, 1],)) as thread:\n    assert thread.future.result(1) == 2\n\n# equals to:\nwith Thread.submit(sum, [1, 1]) as thread:\n    assert thread.future.result(1) == 2\n```\n\n### Benchmarks\n\n```bash\n$ poetry run python bench.py\nsubmit(sum, [1, 1]) max_workers=1 times=1000000:\n---\nconcurrent.ThreadPoolExecutor\ttime spent: 51.68451470899163 sec\nthreadlet.ThreadPoolExecutor\ttime spent: 14.034955328999786 sec\n\nsubmit(sum, [1, 1]) max_workers=2 times=1000000:\n---\nconcurrent.ThreadPoolExecutor\ttime spent: 30.85988494398771 sec\nthreadlet.ThreadPoolExecutor\ttime spent: 14.149454248996335 sec\n\nsubmit(sum, [1, 1]) max_workers=3 times=1000000:\n---\nconcurrent.ThreadPoolExecutor\ttime spent: 23.788395736002713 sec\nthreadlet.ThreadPoolExecutor\ttime spent: 14.243532117005088 sec\n\nsubmit(sum, [1, 1]) max_workers=4 times=1000000:\n---\nconcurrent.ThreadPoolExecutor\ttime spent: 24.605877805995988 sec\nthreadlet.ThreadPoolExecutor\ttime spent: 14.26560322700243 sec\n\nfutures.wait(<1000000 futures>) max_workers=1\n---\nconcurrent.ThreadPoolExecutor\ttime spent: 7.2795372900000075 sec\nthreadlet.ThreadPoolExecutor\ttime spent: 5.727786898991326 sec\n\nfutures.wait(<1000000 futures>) max_workers=2\n---\nconcurrent.ThreadPoolExecutor\ttime spent: 21.606328508001752 sec\nthreadlet.ThreadPoolExecutor\ttime spent: 18.455558971996652 sec\n\nfutures.wait(<1000000 futures>) max_workers=3\n---\nconcurrent.ThreadPoolExecutor\ttime spent: 22.43454322699108 sec\nthreadlet.ThreadPoolExecutor\ttime spent: 21.441624792001676 sec\n\nfutures.wait(<1000000 futures>) max_workers=4\n---\nconcurrent.ThreadPoolExecutor\ttime spent: 25.23331410800165 sec\nthreadlet.ThreadPoolExecutor\ttime spent: 21.244171070997254 sec\n\nsubmit(sum, [1, 1]) 1000000 times then futures.wait(<1000000 futures>) max_workers=1\n---\nconcurrent.ThreadPoolExecutor\ttime spent: 18.50262119299441 sec\nthreadlet.ThreadPoolExecutor\ttime spent: 11.705895610997686 sec\n\nsubmit(sum, [1, 1]) 1000000 times then futures.wait(<1000000 futures>) max_workers=2\n---\nconcurrent.ThreadPoolExecutor\ttime spent: 15.47274379299779 sec\nthreadlet.ThreadPoolExecutor\ttime spent: 11.893112275007297 sec\n\nsubmit(sum, [1, 1]) 1000000 times then futures.wait(<1000000 futures>) max_workers=3\n---\nconcurrent.ThreadPoolExecutor\ttime spent: 17.14120809501037 sec\nthreadlet.ThreadPoolExecutor\ttime spent: 11.979401491989847 sec\n\nsubmit(sum, [1, 1]) 1000000 times then futures.wait(<1000000 futures>) max_workers=4\n---\nconcurrent.ThreadPoolExecutor\ttime spent: 16.178104474005522 sec\nthreadlet.ThreadPoolExecutor\ttime spent: 12.229133631990408 sec\n```\n\n---\n\n- Free software: MIT license\n',
    'author': 'Andrii Kuzmin',
    'author_email': 'jack.cvr@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
