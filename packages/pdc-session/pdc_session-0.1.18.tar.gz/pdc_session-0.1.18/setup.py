# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pdc_session',
 'pdc_session.api',
 'pdc_session.helpers',
 'pdc_session.storage',
 'pdc_session.types']

package_data = \
{'': ['*']}

install_requires = \
['ecceran==0.1.1', 'requests>=2,<3']

setup_kwargs = {
    'name': 'pdc-session',
    'version': '0.1.18',
    'description': 'simple shopee session manager',
    'long_description': "# Shopee Session\n\nsimple shopee session manager\n\n### Install\n`$ python -m pip install pdc-session`\n\n### configure\n\n ```python\nfrom pdc_session.session_config import configure_client\n\napi_uri = 'http://localhost:51016'\napi_key = '0234a45a4d4c34f1849638f****'\nbotname = 'test'\n\n\nconfigure_client(\n    api_uri = api_uri, # api_uri default http://localhost:4000\n    api_key = api_key, # api_key format string hex\n    botname = botname # botname format string\n)\n\n```\n\n### A Simple Example\n\n```python\nfrom requests import Session\nfrom pdc_session.session_persist import SessionPersist\n\n# SessionPersist need username to run\nSessionPersist.username = 'test'\n\n\nwith SessionPersist() as sp:\n    # when entering class will find available sessions and lock them\n    \n    # create new session\n    session = Session() # session from requests\n    sp.create(lock=True) # lock is optional, defaults as True\n\n    # get avaliable session\n    # by default it is called when on enter\n    sp.get_session()\n    sp.session_id # when id is not 0, then session is valid\n    sp.session_valid # or check with session_valid\n\n    # if get_session() is falied, method all_locked() will be called\n\n    # lock session\n    # by default you need to change the session_id property and call lock_session()\n    sp.session_id = 'someid'\n    sp.lock_session() # but this is not recommended\n\n    # release session\n    # set session to unlocked\n    sp.release_session()\n\n    # update session\n    # by default it is called when on exit\n    sp.session.cookies.set('test', 'test')\n    sp.update_session()\n```\n\n### Best Practice\n\n```python\nfrom pdc_session.session_persist import SessionPersist\n\nclass Auth(SessionPersist):\n    \n    username: str\n    password:str\n\n    def __init__(self, username, password):\n        self.username = username\n        self.password = password\n\n\nwith Auth('test', 'test') as auth:\n    auth.session.get('/getinfo')\n    auth.session.get('/product')\n    auth.session.post('/upload_product')\n```\n\n### Blocking Code\n\n```python\nfrom pdc_session.session_persist import SessionPersist\n\nclass Auth(SessionPersist):\n    \n    username: str\n    password:str\n\n    def __init__(self, username, password):\n        self.username = username\n        self.password = password\n\nuser = Auth('test', 'test')\nuser._acquire()\nauth.session.get('/getinfo')\nauth.session.get('/product')\nauth.session.post('/upload_product')\nuser._release()\n```\n",
    'author': 'Hfrada',
    'author_email': 'madefrada@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
