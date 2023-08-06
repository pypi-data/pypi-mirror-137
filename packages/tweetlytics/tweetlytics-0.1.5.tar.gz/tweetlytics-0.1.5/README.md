[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# tweetlytics

This package would retrieve tweets on a required topic and time frame, stores them, performs data cleaning, data analysis, and plotting.

## Installation

```bash
$ pip install --index-url https://test.pypi.org/simple/ \
  --extra-index-url https://pypi.org/simple tweetlytics
```

## Features

The package tweetytics is a package intended to give insight about a topic on Tweeter through some functions. The intention is that a user with little knowledge about data science can quickly call a function to analyze how the topics and trends are on Twitter. Internally, the package uses the official twitter API, stores the data as a .json and .csv file, performs data cleaning, data analysis and plotting.

There are four main functions planned for development and they are outlined below.  Additional functions may be added if time permits.

### Function 1: get_store

Utilizes the official Twitter API to collect data based on a keyword, date range and number of results the user requires. The data is then stored as a .Json file and a .csv file(optional). The function will also give the user the option to return a pandas data frame based on the stored files.

### Function 2: clean

Takes the created pandas data frame from the get_store() function and clean the data frame based on the required_cols, keep_punctuation, only_words… arguments entered by the user.

### Function 3: perform_analysis

Takes the tidy data frame from the clean() function and returns an analysis dict report including mean_word_count, most used words, mean_likes, most_used_hashtags, word_hashtag_ratio …

### Function 4: plotting

Taking both the cleaned data frame from the clean() function and the returned dict from the perform_analysis() function, a range of plots such as likes_wordcount, likes_hashtags… will be generated and saved as files.

### Note

•As working with the Twitter API requires a personal ‘bearer token’ a user can create their own token and add it as a parameter to the get_store() function.
•The package also include an example .Json and .csv file  based on the keyword ‘omicron’.

## Dependencies

 • arrow
 • requests
 • pandas 
 • dotenv
 • altair 
 • numpy
 • collections
 • re
 • tweepy
 • textblob
 • string

## Usage
•To use to get_store() function, users will require to obtain a bearer token for the official Twitter API V2. The bearer token can be requested on developers.twitter.com.
•To test the package output, we have added sample files returned from the get_store() function and users can run clean_tweets(), analytics() and the plot_freq() functions.

### Sample outputs
• analytics()
  
  ![Table1](https://github.com/UBC-MDS/tweetlytics/blob/main/output/media/df1.png)
  
• plot_freq()
  
  ![Table1](https://github.com/UBC-MDS/tweetlytics/blob/main/output/media/plot1.png)
  
  ![Table1](https://github.com/UBC-MDS/tweetlytics/blob/main/output/media/plot2.png)


## Documentation

The official documentation is hosted on Read the Docs: https:// tweetytics.readthedocs.io/en/latest/

## Contributing

IWe welcome and recognize all contributions. You can see a list of current contributors in the [contributors tab]( https://github.com/UBC-MDS/tweetlytics/blob/main/CONTRIBUTING.md).

* Amir Shojakhani: @amirshoja
* Shiva Shankar Jena: @shivajena
* Mahmood Rahman: @mahm00d27
* Mahsa Sarafrazi: @mahsasarafrazi

## License

`tweetlytics` was created by group of students in UBC MDS program. It is licensed under the terms of the MIT license.

## Credits

`tweetlytics` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
