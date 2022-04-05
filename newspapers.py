import csv
from newspaper import Config
from newspaper import Article


# wall streat journals
def newspaper():
    USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0'

    config = Config()
    config.browser_user_agent = USER_AGENT
    config.request_timeout = 10

    base_url = 'https://wjs.com'
    article = Article(base_url, config=config)
    article.download()
    article.parse()
    article_meta_data = article.meta_data

    published_date = {value for (key, value) in article_meta_data.items() if key == 'article.published'}
    article_published_date = " ".join(str(x) for x in published_date)

    authors = sorted({value for (key, value) in article_meta_data.items()if key == 'author'})
    article_author = ', '.join(authors)

    title = {value for (key, value) in article_meta_data.items() if key == 'article.headline'}
    article_title = " ".join(str(x) for x in title)

    summary = {value for (key, value) in article_meta_data.items() if key == 'article.summary'}
    article_summary = " ".join(str(x) for x in summary)

    keywords = ''.join({value for (key, value) in article_meta_data.items() if key == 'news_keywords'})
    keywords_list = sorted(keywords.lower().split(','))
    article_keywords = ', '.join(keywords_list)

    with open('wsj_extraction_results.csv', 'a', newline='') as csvfile:
        headers = ['date published', 'article authors', 'article title', 'article summary', 'article keywords']
        writer = csv.DictWriter(csvfile, delimiter=',', lineterminator='\n', fieldnames=headers)
        writer.writeheader()

        writer.writerow({'date published': article_published_date,
                         'article authors': article_author,
                         'article title': article_title,
                         'article summary': article_summary,
                         'article keywords': article_keywords})
        print(article_published_date)
        print(article_author)
        print(article_title)
        #print(article_keywords)
        print(article_summary)

#newspaper()

import json
import pandas as pd
from datetime import datetime
from newspaper import Config
from newspaper import Article
from newspaper.utils import BeautifulSoup

def htmlppr():


    USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0'

    config = Config()
    config.browser_user_agent = USER_AGENT
    config.request_timeout = 10

    def path_to_image_html(link):
        """
        Converts image links to HTML tags
        :param link: image URL
        :return: URL wrapped in clickable HTML tag
        """
        return f'<a href="{link}"> <img src="{link}" width="60" > </a>'

    def harvest_article_content(website):
        """
        Queries and extracts specific content from a LA Times article.
        :param website: URL for a LA Times article
        :return: pandas dataframe
        """
        df_latimes_extraction = pd.DataFrame(columns=['Date Published', 'URL', 'Author', 'Title',
                                                      'Summary', 'Text', 'Main Image'])

        article = Article(website, config=config)
        article.download()
        article.parse()

        soup = BeautifulSoup(article.html, 'html.parser')
        la_times_dictionary = json.loads("".join(soup.find("script", {"type": "application/ld+json"}).contents))

        date_published = ''.join([value for (key, value) in la_times_dictionary.items() if key == 'datePublished'])
        clean_date = datetime.strptime(date_published, "%Y-%m-%dT%H:%M:%S.%f%z").strftime('%Y-%m-%d')

        article_author = ''.join([value[0]['name'] for (key, value) in la_times_dictionary.items() if key == 'author'])
        article_title = ''.join([value for (key, value) in la_times_dictionary.items() if key == 'headline'])
        article_url = ''.join([value for (key, value) in la_times_dictionary.items() if key == 'url'])
        article_description = ''.join([value for (key, value) in la_times_dictionary.items() if key == 'description'])
        article_body = ''.join([value.replace('\n', ' ') for (key, value) in la_times_dictionary.items() if key ==
                                'articleBody'])

        local_df = save_article_data(df_latimes_extraction, clean_date,
                                     f'<a href="{article_url}">{article_url}</a>',
                                     article_author,
                                     article_title,
                                     article_description,
                                     article_body,
                                     article.top_image)
        return local_df

    def save_article_data(df, published_date, website, authors, title, summary, text, main_image):
        """
        Writes extracted article content to a pandas dataframe.

        :param df: pandas dataframe
        :param published_date: article's published date
        :param website: article's URL
        :param authors: article's author
        :param title: article's title
        :param summary: article's summary
        :param text: article's text
        :param main_image: article's top image
        :return: pandas dataframe
        """
        local_df = df.append({'Date Published': published_date,
                              'URL': website,
                              'Author': authors,
                              'Title': title,
                              'Summary': summary,
                              'Text': text,
                              'Main Image': path_to_image_html(main_image)}, ignore_index=True)
        return local_df

    def create_html_file(df):
        """
        Writes a pandas dataframe that contains extracted article content to a HTML file.

        :param df: pandas dataframe
        :return:
        """
        pd.set_option('colheader_justify', 'center')

        html_string = '''
        <html>
          <head>
          <meta charset="utf-8">
          <title>Los Angeles Times Article Information</title></head>
          <link rel="stylesheet" type="text/css" href="df_style.css"/>
          <body>
            {table}
          </body>
        </html>.
        '''

        with open('latimes_results.html', 'w') as f:
            f.write(html_string.format(table=df.to_html(index=False, escape=False, classes='mystyle')))

        return None

    # List used to store pandas content extracted
    # from articles.
    article_data = []

    urls = ['https://www.latimes.com/environment/story/2021-02-10/earthquakes-climate-change-threaten-california-dams',
            'https://www.latimes.com/business/story/2021-02-08/tesla-invests-in-bitcoin',
            'https://www.latimes.com/business/story/2021-02-09/joe-biden-wants-100-clean-energy-will-california-show-that-its-possible']

    for url in urls:
        results = harvest_article_content(url)
        article_data.append(results)

    # concat all the article content into a new pandas dataframe.
    df_latimes = pd.concat(article_data)

    # Create the HTML file
    create_html_file(df_latimes)

#htmlppr()








import newspaper
from newspaper import Config
from newspaper import news_pool

def multiplenews():
    USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0'

    config = Config()
    config.browser_user_agent = USER_AGENT
    config.request_timeout = 10

    wsj_news = newspaper.build('https://timesofindia.indiatimes.com/india/modi-us-visit-live-updates-september-24-united-states-joe-biden-kamala-harris/liveblog/86465269.cms', config=config, memoize_articles=False, language='en')
    cnn_news = newspaper.build('https://www.wsj.com/', config=config, memoize_articles=False, language='en')
    news_sources = [wsj_news, cnn_news]

    # the parameters number_threads and thread_timeout_seconds are adjustable
    news_pool.config.number_threads = 4
    news_pool.config.thread_timeout_seconds = 1
    news_pool.set(news_sources)
    news_pool.join()

    article_urls = set()
    for source in news_sources:
        for article_extract in source.articles:
            if article_extract.url not in article_urls:
                article_urls.add(article_extract.url)
                print(article_extract.title)

multiplenews()