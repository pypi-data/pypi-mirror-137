# Authors: Mahsa Sarafrazi, Mahmood Rahman, Shiva Shankar Jena, Amir Shojakhani
# Jan 2022

# imports
import requests
import os
import json
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv
import altair as alt
import altair_saver
import numpy as np
from textblob import TextBlob
import ast
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

load_dotenv()  # load .env files in the project folder


def get_store(
    bearer_token,
    keyword,
    start_date,
    end_date,
    max_results=25,
    store_path="output/",
    store_csv=False,
    include_public_metrics=True,
    api_access_lvl="essential",
):
    """
    Retreives all tweets of a keyword provided by the user through the Twitter API.
    Alternatively the user can directly read from a structered Json response based
    on the Twitter API.
    If the user plans to access to the Twitter API they must have a personal bearer
    token and store it as an environement variable to access it.
    Parameters:
    -----------
    bearer_token : string
        The user's personal twitter API dev bearer token.
        It is recommended to add the token from an
        enviroment variable.
    keyword : string
        The keyword to search Twitter and retrieve tweets.
    start_date: string
        Starting date to collect tweets from. Dates should be
        entered in string format: YYYY-MM-DD
    end_date: string
        Ending date (Included) to collect tweets from. Dates should be
        entered in string format: YYYY-MM-DD
    max_results: int
        The maximum number of tweets to return. Default is 25.
        Must be between 10 and 100.
    store_path: string
        The string path to store the retrieved tweets in
        Json format. Default is working directory.
    store_csv: boolean
        Create .csv file with response data or not.
        Default is False.
    include_public_metrics : boolean
        Should public metrics regarding each tweet such as
        impression_count, like_count, reply_count, retweet_count,
        url_link_clicks and user_profile_clicks be downloaded
        and stored. Default is True.
    api_access_lvl : string
        The twitter API access level of the user's bearer token.
        Options are 'essential' or 'academic'.
        Default is 'essential'
    Returns:
    --------
    tweets_df : dataframe
        A pandas dataframe of retrieved tweets based on user's
        selected parameters. (Data will be stored as a Json file)
    Examples
    --------
    >>> bearer_token = os.getenv("BEARER_TOKEN")
    >>> tweets = get_store(
            bearer_token,
            keyword="vancouver",
            start_date="2022-01-12",
            end_date="2022-01-17")
    >>> tweets
    """

    # parameter tests
    if not isinstance(bearer_token, str):
        raise TypeError(
            "Invalid parameter input type: bearer_token must be entered as a string"
        )
    if not isinstance(keyword, str):
        raise TypeError(
            "Invalid parameter input type: keyword must be entered as a string"
        )
    if not isinstance(start_date, str):
        raise TypeError(
            "Invalid parameter input type: start_date must be entered as a string"
        )
    if not (
        datetime.strptime(end_date, "%Y-%m-%d")
        > datetime.strptime(start_date, "%Y-%m-%d")
        > (datetime.now() - timedelta(days=7))
    ) & (api_access_lvl == "essential"):
        raise ValueError(
            "Invalid parameter input value: api access level of essential can only search for tweets in the past 7 days"
        )
    if not isinstance(end_date, str):
        raise TypeError(
            "Invalid parameter input type: end_date must be entered as a string"
        )
    if not (
        datetime.now()
        >= datetime.strptime(end_date, "%Y-%m-%d")
        > datetime.strptime(start_date, "%Y-%m-%d")
    ):
        raise ValueError(
            "Invalid parameter input value: end date must be in the range of the start date and today"
        )
    if not isinstance(max_results, int):
        raise TypeError(
            "Invalid parameter input type: max_results must be entered as an integer"
        )
    if not isinstance(store_path, str):
        raise TypeError(
            "Invalid parameter input type: store_path must be entered as a string"
        )
    if not isinstance(store_csv, bool):
        raise TypeError(
            "Invalid parameter input type: store_csv must be entered as a boolean"
        )
    if not api_access_lvl in ["essential", "academic"]:
        raise ValueError(
            "Invalid parameter input value: api_access_lvl must be of either string essential or academic"
        )

    headers = {
        "Authorization": "Bearer {}".format(bearer_token)
    }  # set authorization header for API

    # check access level and switch url accordingly. recent will can only search the past 7 days.
    if api_access_lvl == "essential":
        search_url = "https://api.twitter.com/2/tweets/search/recent"
    elif api_access_lvl == "academic":
        search_url = "https://api.twitter.com/2/tweets/search/all"

    # set request parameters
    query_params = {
        "query": f"{keyword}",
        "start_time": f"{start_date}T00:00:00.000Z",
        "end_time": f"{end_date}T00:00:00.000Z",
        "max_results": f"{max_results}",
        "expansions": "author_id,in_reply_to_user_id",
        "tweet.fields": "id,text,author_id,in_reply_to_user_id,conversation_id,created_at,lang,public_metrics,referenced_tweets,reply_settings,source",
        "user.fields": "id,name,username,created_at,description,public_metrics,verified,entities",
        "place.fields": "full_name,id,country,country_code,name,place_type",
        "next_token": {},
    }

    # send request and store response
    tweet_response = requests.request(
        "GET", search_url, params=query_params, headers=headers
    )
    tweet_response_json = tweet_response.json()

    # check if path in store path exists. create folders if not and create .Json file
    if not os.path.exists(store_path):
        os.makedirs(store_path)
    with open(os.path.join(store_path, "tweets_response.json"), "w") as file:
        json.dump(tweet_response_json, file, indent=4, sort_keys=True)

    tweets_df = pd.DataFrame.from_dict(tweet_response_json["data"])

    # expand public_metrics and referenced_tweets column and store in separate columns.
    tweets_df[["retweetcount", "reply_count", "like_count", "quote_count"]] = tweets_df[
        "public_metrics"
    ].apply(pd.Series)

    tweets_df = tweets_df.explode("referenced_tweets").reset_index(drop=True)

    # fill missing referenced tweets
    tweets_df["referenced_tweets"] = tweets_df.apply(
        lambda x: x["referenced_tweets"]
        if isinstance(x["referenced_tweets"], dict)
        else {"type": "original", "id": x["id"]},
        axis=1,
    )

    tweets_df[["reference_type", "reference_id"]] = tweets_df[
        "referenced_tweets"
    ].apply(pd.Series)

    # add searched keyword titles to dataframe
    tweets_df["keyword"] = keyword

    if store_csv:
        tweets_df.to_csv(os.path.join(store_path, "tweets_response.csv"), index=False)

    return tweets_df


def clean_tweets(
    file_path, tokenization=True, word_count=True, store_csv=True, store_inplace=False
):
    """
    Cleans the text in the tweets and returns as new columns in the dataframe.

    The cleaning process includes converting into lower case, removal of punctuation, hastags and hastag counts
    Parameters:
    -----------
    file_path : string
        File path to csv file containing tweets data
    tokenization : Boolean
        Creates new column containing cleaned tweet word tokens when True
        Default is True
    word_count : Boolean
        Creates new column containing word count of cleaned tweets
        Default is True

    df_tweets : dataframe
        A pandas dataframe comprising cleaned data in additional columns

    Examples
    --------
    >>> clean_tweets("tweets_df.json")
    """

    # Checking for valid input parameters

    if not isinstance(file_path, str):
        raise Exception("'input_file' must be of str type")
    if not isinstance(tokenization, bool):
        raise Exception("'tokenization' must be of bool type")
    if not isinstance(word_count, bool):
        raise Exception("'word_count' must be of bool type")

    # Dropping irrelavant columns
    columns = ["public_metrics"]
    df = pd.read_csv(file_path).drop(columns=columns)

    # Checking for 'df' to be a dataframe
    if not isinstance(df, pd.DataFrame):
        raise Exception("'df' must be of DataFrame type.")

    df["text"] = df["text"].str.replace(r"RT\s@.*:\s", "", regex=True)
    df["text"] = df["text"].str.lower()
    df["hashtags"] = df["text"].str.findall(r"#.*?(?=\s|$)")

    # Cleaning hashtags and mentions in tweet text
    df["text"] = df["text"].str.replace(r"@[A-Za-z0-9_]+", "", regex=True)
    df["text"] = df["text"].str.replace(r"#[A-Za-z0-9_]+", "", regex=True)

    # Cleaning links in text
    df["text"] = df["text"].str.replace(r"http\S+", "", regex=True)
    df["text"] = df["text"].str.replace(r"#[A-Za-z0-9_]+", "", regex=True)

    # Cleaning all punctuations
    df["text"] = df["text"].str.replace("[^\w\s]", "", regex=True)

    # Adding clean_tokens column and remove duplicates
    if tokenization:
        df["tokens"] = df["text"].str.split()
        # Adding word_count column
        if word_count:
            df["word_count"] = df["tokens"].str.len()
        df["tokens"] = df["tokens"].map(lambda x: list(set(x)))

    # drop if text is empty
    df = df.query("text.str.len() > 0")

    if store_csv:
        if store_inplace:
            df.to_csv(file_path, index=False)
        else:
            folder_path = file_path.split("/")[0]
            df.to_csv(os.path.join(folder_path, "clean_tweets.csv"), index=False)

    return df


def analytics(input_file, store_json=True, store_csvs=False):
    """Analysis the tweets of specific keyword in term of
    average number of retweets, the total number of
    comments, most used hashtags and the average number
    of likes of these tweets.

    Parameters
    ----------
    input_file : dataframe
        pandas dataframe
    keyword: str
        The keyword that the original dataframe extracted
        based on.

    Returns
    -------
    analytics_df: dataframe
        Dataframe object where includes average number
        of retweets, the total number of comments, most
        used hashtags and the average number of likes

    Examples
    --------
    >>> from tweetlytics.tweetlytics import analytics
    >>> report = analytics(df,keyword)
    """

    # checking the input_file argument to be url path
    if not isinstance(input_file, str):
        raise TypeError(
            "Invalid parameter input type: input_file must be entered as a string of url"
        )
    if not isinstance(store_json, bool):
        raise TypeError(
            "Invalid parameter input type: store_json must be entered as a boolean"
        )
    if not isinstance(store_csvs, bool):
        raise TypeError(
            "Invalid parameter input type: store_csvs must be entered as a boolean"
        )

    df = pd.read_csv(input_file, converters={"tokens": ast.literal_eval})

    result = {}  # for storing the result from each part

    # group by keyword and get sums
    df_sum = df.groupby("keyword").sum()

    # add keyword to result
    result["keyword"] = df_sum.index.values[0]

    # add sum of like, comment and retweets
    result["total_number_of_tweets"] = len(df)
    result["total_number_of_likes"] = df_sum["like_count"].values[0]
    result["total_number_of_comments"] = df_sum["reply_count"].values[0]
    result["total_number_of_retweets"] = df_sum["retweetcount"].values[0]

    # determining the sentiment of the tweet
    df["sentiment_polarity"] = df["text"].map(lambda x: TextBlob(x).sentiment.polarity)
    df["sentiment_type"] = df["sentiment_polarity"].map(
        lambda x: "positive" if x > 0 else ("negative" if x < 0 else "neutral")
    )

    # adding all df to result
    all_tweets = df.to_json(orient="records")

    # adding sentiment group data
    df_sentiment_group = df.groupby("sentiment_type").agg(
        {
            "retweetcount": "sum",
            "reply_count": "sum",
            "like_count": "sum",
            "quote_count": "sum",
            "word_count": "sum",
            "sentiment_polarity": "sum",
        }
    )
    df_sentiment_group["tweet_count"] = df.groupby("sentiment_type").agg(
        {"sentiment_polarity": "count"}
    )["sentiment_polarity"]

    df_sentiment_group.reset_index(inplace=True)

    df_sentiment_group["tweet_group_percentage"] = (
        df_sentiment_group["tweet_count"] / sum(df_sentiment_group["tweet_count"]) * 100
    )

    sentiment_group_detail_json = df_sentiment_group.to_json(orient="records")

    # adding tokens and sentiment data
    df_tokens_sentiments = df[["tokens", "sentiment_type"]].explode("tokens")
    df_tokens_sentiments = (
        df_tokens_sentiments.groupby(["tokens", "sentiment_type"])
        .size()
        .sort_values(ascending=False)
        .reset_index(name="count")
    )

    tokens_sentiments = df_tokens_sentiments.to_json(orient="records")

    # get top tweet based on sum of likes + retweets
    df["sum_like_retweet"] = df["like_count"] + df["retweetcount"]
    df_top_tweets = (
        df.sort_values("sum_like_retweet")
        .drop_duplicates(["reference_id"])
        .nlargest(10, "sum_like_retweet")[
            [
                "text",
                "retweetcount",
                "like_count",
                "hashtags",
                "sentiment_polarity",
                "sentiment_type",
            ]
        ]
    )

    top_tweets_json = df_top_tweets.to_json(orient="records")

    # Saving analysis as json and csvs
    folder_path = input_file.split("/")[0]
    if store_json:
        with open(os.path.join(folder_path, "all_tweets.json"), "w") as file:
            json.dump(all_tweets, file, indent=4, sort_keys=True)

        with open(os.path.join(folder_path, "top_tweets.json"), "w") as file:
            json.dump(top_tweets_json, file, indent=4, sort_keys=True)

        with open(
            os.path.join(folder_path, "sentiment_group_detail_json.json"), "w"
        ) as file:
            json.dump(sentiment_group_detail_json, file, indent=4, sort_keys=True)

        with open(os.path.join(folder_path, "tokens_sentiments.json"), "w") as file:
            json.dump(tokens_sentiments, file, indent=4, sort_keys=True)

        with open(os.path.join(folder_path, "tweets_sums.json"), "w") as file:
            json.dump(result, file, indent=4, sort_keys=True)

    if store_csvs:
        df.to_csv(os.path.join(folder_path, "analysis_all_tweets.csv"), index=False)
        df_sum.to_csv(os.path.join(folder_path, "analysis_sums.csv"), index=False)
        df_top_tweets.to_csv(
            os.path.join(folder_path, "analysis_top_tweets.csv"), index=False
        )
        df_sentiment_group.to_csv(
            os.path.join(folder_path, "analysis_sentiment_group.csv"), index=False
        )
        df_tokens_sentiments.to_csv(
            os.path.join(folder_path, "analysis_tokens_sentiments.csv"), index=False
        )

    return (df, df_sum, df_top_tweets, df_sentiment_group, df_tokens_sentiments)


def plot_tweets(
    all_tweets_file,
    analysis_sums_file=None,
    analysis_top_tweets_file=None,
    analysis_sentiment_group_file=None,
    analysis_tokens_sentiments_file=None,
    save_plots=True,
):

    if not isinstance(all_tweets_file, str):
        raise TypeError(
            "Invalid parameter input type: all_tweets_file path must be entered as a string"
        )
    if not isinstance(analysis_tokens_sentiments_file, str):
        raise TypeError(
            "Invalid parameter input type: analysis_tokens_sentiments_file path must be entered as a string"
        )
    if not isinstance(save_plots, bool):
        raise TypeError(
            "Invalid parameter input type: save_plots must be entered as a boolean"
        )

    all_tweets_df = pd.read_csv(
        all_tweets_file, converters={"hashtags": ast.literal_eval}
    )
    tokens_sentiments_df = pd.read_csv(analysis_tokens_sentiments_file)
    folder_path = all_tweets_file.split("/")[0]

    # word clouds
    stopwords = set(STOPWORDS)

    # positive words
    words_string_positive = (
        " ".join(tokens_sentiments_df.query('sentiment_type == "positive"')["tokens"])
        + " "
    )

    wordcloud_positive = WordCloud(
        width=800,
        height=800,
        background_color="white",
        colormap="YlGn",
        stopwords=stopwords,
        min_font_size=10,
    ).generate(words_string_positive)

    plt.figure(figsize=(8, 8), facecolor=None)
    plt.imshow(wordcloud_positive)
    plt.axis("off")
    plt.tight_layout(pad=0)

    # Saving positive word cloud
    if save_plots:
        plt.savefig(os.path.join(folder_path, "word_cloud_positive.png"))

    # negative words
    words_string_negative = (
        " ".join(tokens_sentiments_df.query('sentiment_type == "negative"')["tokens"])
        + " "
    )

    wordcloud_negative = WordCloud(
        width=800,
        height=800,
        background_color="white",
        colormap="Reds",
        stopwords=stopwords,
        min_font_size=10,
    ).generate(words_string_negative)

    plt.figure(figsize=(8, 8), facecolor=None)
    plt.imshow(wordcloud_negative)
    plt.axis("off")
    plt.tight_layout(pad=0)

    # Saving negative word cloud
    if save_plots:
        plt.savefig(os.path.join(folder_path, "word_cloud_negative.png"))

    # plot top word distribution
    top_words = (
        tokens_sentiments_df.groupby("tokens")
        .sum()
        .reset_index()
        .sort_values("count", ascending=False)
    )
    top_words = (
        top_words.query("tokens.str.len() >= 4")
        .nlargest(20, "count")["tokens"]
        .to_list()
    )
    top_words_df = tokens_sentiments_df.query("tokens in @top_words")

    top_words_plot = (
        alt.Chart(data=top_words_df)
        .mark_bar()
        .encode(
            x="count",
            y="tokens",
            color=alt.Color("sentiment_type", scale=alt.Scale(scheme="redyellowgreen")),
        )
    )

    top_words_plot.save(
        os.path.join(folder_path, "top_words_plot.png"), scale_factor=2.0
    )

    # plot hashtag counts
    hash_tags_df = all_tweets_df["hashtags"].explode("hashtags").dropna().reset_index()
    top_hash_tags_df = (
        hash_tags_df.groupby("hashtags")
        .count()
        .sort_values("index", ascending=False)
        .reset_index()
        .nlargest(15, "index")
    )
    top_hash_tags_df.rename(columns={"index": "count"}, inplace=True)

    top_hashtags_plot = (
        alt.Chart(data=top_hash_tags_df)
        .mark_bar()
        .encode(alt.X("count"), alt.Y("hashtags", sort="-x"))
    )

    top_hashtags_plot.save(
        os.path.join(folder_path, "top_hashtags_plot.png"), scale_factor=2.0
    )

    return (wordcloud_positive, wordcloud_negative, top_words_plot, top_hashtags_plot)
