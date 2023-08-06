# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['tweetlytics']

package_data = \
{'': ['*']}

install_requires = \
['altair-saver>=0.5.0,<0.6.0',
 'altair>=4.2.0,<5.0.0',
 'arrow>=1.2.1,<2.0.0',
 'matplotlib>=3.5.1,<4.0.0',
 'pandas>=1.3.5,<2.0.0',
 'python-dotenv>=0.19.2,<0.20.0',
 'requests>=2.27.1,<3.0.0',
 'textblob>=0.17.1,<0.18.0',
 'tweepy>=4.4.0,<5.0.0',
 'wordcloud>=1.8.1,<2.0.0']

setup_kwargs = {
    'name': 'tweetlytics',
    'version': '0.1.6',
    'description': 'Retrieves tweets on a required topic and timeframe using the official twitter API, stores them as a .json and .csv file, performs data cleaning, data analysis and plotting.',
    'long_description': '[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n[![ci-cd](https://github.com/UBC-MDS/tweetlytics/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/UBC-MDS/tweetlytics/actions/workflows/ci-cd.yml)\n\n# tweetlytics\n\nThis package would retrieve tweets on a required topic and time frame, stores them, performs data cleaning, data analysis, and plotting.\n\n## Installation\n\n```bash\n$ pip install --index-url https://test.pypi.org/simple/ \\\n  --extra-index-url https://pypi.org/simple tweetlytics\n```\n\n## Features\n\nThe package tweetytics is a package intended to give insight about a topic on Tweeter through some functions. The intention is that a user with little knowledge about data science can quickly call a function to analyze how the topics and trends are on Twitter. Internally, the package uses the official twitter API, stores the data as a .json and .csv file, performs data cleaning, data analysis and plotting.\n\nThere are four main functions planned for development and they are outlined below.  Additional functions may be added if time permits.\n\n### Function 1: get_store\n\nUtilizes the official Twitter API to collect data based on a keyword, date range and number of results the user requires. The data is then stored as a .Json file and a .csv file(optional). The function will also give the user the option to return a pandas data frame based on the stored files.\n\n### Function 2: clean\n\nTakes the created pandas data frame from the get_store() function and clean the data frame based on the required_cols, keep_punctuation, only_words… arguments entered by the user.\n\n### Function 3: perform_analysis\n\nTakes the tidy data frame from the clean() function and returns an analysis dict report including mean_word_count, most used words, mean_likes, most_used_hashtags, word_hashtag_ratio …\n\n### Function 4: plotting\n\nTaking both the cleaned data frame from the clean() function and the returned dict from the perform_analysis() function, a range of plots such as likes_wordcount, likes_hashtags… will be generated and saved as files.\n\n### Note\n\n•As working with the Twitter API requires a personal ‘bearer token’ a user can create their own token and add it as a parameter to the get_store() function.\n•The package also include an example .Json and .csv file  based on the keyword ‘omicron’.\n\n## Dependencies\n\n • requests\n • pandas \n • dotenv\n • altair \n • numpy\n • textblob\n • string\n • matplotlib\n • wordcloud\n\n\n## Usage\n•To use to get_store() function, users will require to obtain a bearer token for the official Twitter API V2. The bearer token can be requested on developers.twitter.com.\n•To test the package output, we have added sample files returned from the get_store() function and users can run clean_tweets(), analytics() and the plot_freq() functions.\n\n### Sample outputs\n• analytics()\n  \n  ![Table1](https://github.com/UBC-MDS/tweetlytics/blob/main/output/media/df1.png)\n  \n• plot_freq()\n  \n  ![Table1](https://github.com/UBC-MDS/tweetlytics/blob/main/output/media/plot1.png)\n  \n  ![Table1](https://github.com/UBC-MDS/tweetlytics/blob/main/output/media/plot2.png)\n\n\n## Documentation\n\nThe official documentation is hosted on Read the Docs: https:// tweetytics.readthedocs.io/en/latest/\n\n## Contributing\n\nIWe welcome and recognize all contributions. You can see a list of current contributors in the [contributors tab]( https://github.com/UBC-MDS/tweetlytics/blob/main/CONTRIBUTING.md).\n\n* Amir Shojakhani: @amirshoja\n* Shiva Shankar Jena: @shivajena\n* Mahmood Rahman: @mahm00d27\n* Mahsa Sarafrazi: @mahsasarafrazi\n\n## License\n\n`tweetlytics` was created by group of students in UBC MDS program. It is licensed under the terms of the MIT license.\n\n## Credits\n\n`tweetlytics` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'DSCI_524_2022_Group8',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
