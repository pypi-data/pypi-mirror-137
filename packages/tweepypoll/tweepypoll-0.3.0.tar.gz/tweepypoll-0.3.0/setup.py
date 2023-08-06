# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['tweepypoll']

package_data = \
{'': ['*']}

install_requires = \
['Sphinx>=4.4.0,<5.0.0',
 'altair>=4.2.0,<5.0.0',
 'pandas>=1.3.5,<2.0.0',
 'python-dotenv>=0.19.2,<0.20.0',
 'tweepy>=4.4.0,<5.0.0']

setup_kwargs = {
    'name': 'tweepypoll',
    'version': '0.3.0',
    'description': 'Collect and visualize twitter poll data.',
    'long_description': '# tweepypoll\n\n## Overview\n\n`tweepypoll`\xa0is a Python package that allows users to extract and visualize poll data (poll questions, poll options, poll responses, etc.) from Twitter. Our goal is to make `tweepypoll` helpful and user-friendly; any Python beginner can effectively gain access to the data and make their own data-driven decisions. In particular, it could be a useful package for people doing social media journalism, or those studying social media interactions.\n\n**NOTE**: This package assumes that the user has signed up for Twitter API Developer account, acquired the bearer token and set the environmental variable "BEARER_TOKEN". To acquire the bearer token, please follow the instructions [here](https://developer.twitter.com/en/docs/authentication/oauth-2-0/bearer-tokens).\n\n## Functions\n\n- `get_polls_from_user`:\n    - This function retrieves a list of tweet IDs (where the tweet contains a poll) from a Twitter user. These ids can be fed into the `get_poll_by_id` function. \n    - The function will only search through the most 100 recent tweets per requested user. \n\n- `get_poll_by_id`:\n    - This function extracts poll information from Twitter given the tweet ID returned from the `get_polls_from_user` function.\n\n- `visualize_poll`:\n    - This function takes in the output of `get_poll_by_id` function and visualizes the poll information. \n\n## Related Packages\n\nThere are a few existing Python packages that have similar functionality for tweets from Twitter. For example, `pytweet` is a package that helps extract tweets, visualize user habit on tweet posting, and apply sentiment analysis to the data. However, there are no available packages that work specifically on polls from Twitter. \n\n## Installation\n\n```bash\n$ pip install tweepypoll\n```\n## Dependencies\n\n- python = "^3.9"\n- altair = "^4.2.0"\n- pandas = "^1.3.5"\n- tweepy = "^4.4.0"\n- python-dotenv = "^0.19.2"\n\n## Usage\n\n```Python\nfrom tweepypoll.tweepypoll import get_polls_from_user\nget_polls_from_user(\'username\')\n```\nwhere **username** is a string username, such as \'ElonMusk\'\n\n```Python\nfrom tweepypoll.tweepypoll import get_poll_by_id\nget_poll_by_id(tweet_id)\n```\n**tweet_id** is numeric, such as 1481040318325739523\n\n```Python\nfrom tweepypoll.tweepypoll import visualize_poll\nvisualize_poll(poll_obj, show_user=False, show_duration=False, show_date=False)\n```\n**poll_obj** is a list of dicts outputted by get_poll_by_id(), **show_user, show_duration, show_date** are optional booleans to display username, poll duration and poll end date, respectively\n\n<img src="https://raw.githubusercontent.com/UBC-MDS/tweepypoll/main/img/visualize_poll_plot.png" width="600">\n\n## Contributors\n\n- Wenxin Xiang\n- Rada Rudyak\n- Linh Giang Nguyen\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`tweepypoll` was created by Wenxin Xiang, Rada Rudyak, Linh Giang Nguyen. It is licensed under the terms of the MIT license.\n\n## Credits\n\n`tweepypoll` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'Wenxin Xiang, Rada Rudyak, Linh Giang Nguyen',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/UBC-MDS/tweepypoll',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
