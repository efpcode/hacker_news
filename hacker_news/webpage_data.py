"""The module webpage_data fetches data from hacker news.

Notes
-----
This module is not executable as script and class should be imported
as shown in `Example`

Example
-------
>>> from webpage_data import WebPageData

>>> web_obj = WebPageData(5, votes= 150)

>>> print(web_obj)
Fetched data from hacker news:
 [Title, Points, Link]

"""

from time import sleep
from requests import Session as rqs
from requests import ConnectTimeout, ConnectionError, HTTPError
from bs4 import BeautifulSoup


class WebPageData:
    """WebPageData, represents the webpage data from hacker news website.

    Attributes
    ----------
    web_content : WebResponse(web_content: int)
        The instance attribute called `web_content` is a class instance
        of WebResponse.
    votes : int
        The instance attribute `votes` is the threshold value
        for an article to be considered an item of interest. Default
        value = 100.

    See Also
    --------
    hacker_news.webpage_data.WebResponse : object
        For more information about instance methods.

    """

    def __init__(self, web_content: int, votes: int = 100) -> None:

        self.web_content = WebResponse(web_content)
        self.votes = votes

    def __str__(self):
        """A user friendly prompt of the instance."""
        return "Fetched data from hacker news:\n [Title, Points, Link]"

    def __repr__(self):
        """The representation of a instance object of class."""
        return (
            f"WebPageData(web_content=WebResponse("
            f"{self.web_content.nr_webpages}), "
            f"votes={self.votes})"
        )

    def get_articles(self):
        """Gets articles that meet filtering criteria.

        Returns
        -------
        articles : list
            The return value `articles` is a nested list.

        """

        articles = []
        for page in iter(self.web_content.get_response()):
            html_parse = WebPageData.html_parser(page)
            article = WebPageData.data_filter(html_parse, nr_points=self.votes)
            articles.append(article)

        return articles

    @staticmethod
    def _descending_order(data_list: list) -> list:
        """Reorders a list in descending order.

        Parameters
        ----------
        data_list : list
            A nested list data structure that is generated in
            staticmethod called data_filter.

        Returns
        -------
        data_list : list
            A descending ordered nested-list data type based on
            the number of points an article has.
        """
        data_list.sort(key=lambda x: x[1], reverse=True)

        return data_list

    @staticmethod
    def html_parser(web_content: str) -> BeautifulSoup:
        """Parses web content.

        The method parses the web content in url_hn and returns a
        BeautifulSoup object, that function like a css selector.

        Parameters
        ----------
        web_content : str
            The `web_content` parameter is a string object that
            contains html text.

        Returns
        -------
        BeautifulSoup : object
            The BeautifulSoup object returned, is an actual instance
            of a BeautifulSoup class.

        Raises
        ------
        TypeError
            This error is raised if `web_content` is passed as none
            or null.
        ValueError
             This error is raised if `web_content` is not passed with
             string content.

        See Also
        --------
        bs4.BeautifulSoup : object
            For more information a about css selector and parse
            methods used.

        """
        try:
            if not web_content:
                raise ValueError("Expected: to have string/web content")
        except ValueError as error:
            empty = f"<p>This did not work has expected:\n" f"{error}</p>"
            Warning(error)
            return BeautifulSoup(empty, "html.parser")

        else:
            return BeautifulSoup(f"{web_content}", "html.parser")

    @staticmethod
    def data_filter(data_parsed, nr_points=100, ordered_data=True) -> list:
        """Helper method that filter web content by threshold.

        The method filters the web content on an arbitrary threshold,
        that can be modified by user.

        Parameters
        ----------
        data_parsed : bs4.BeautifulSoup(object)
            The data_parsed parameter is the return value from
            static method called WebPageData.html_parser.
        nr_points: int
            The threshold that needs to be exceed for an article to be
            picked. Default value is set to 100.
        ordered_data : bool
            Sorts in descending order the generated nested list
            data structure. For unsorted returns change value from
            default to False. Default value is set to True.

        Returns
        -------
        news_list : list
            The `news_list` is a nested-list data type (see below).
            The items: [[title, score, link],[title, score, link]...]

        """
        news_list = []
        for i, v in enumerate(data_parsed.find_all("a", class_="titlelink")):
            # fmt: off
            score = (data_parsed.find_all("td", class_="subtext")[i].select(
                ".score")
            )
            # fmt: on
            if score:
                score = int(score[0].getText().split(" ")[0])
                if score < nr_points:
                    continue
                news_list.append([f"{v.text}", score, f"{v.get('href')}"])

        if ordered_data:
            news_list = WebPageData._descending_order(news_list)

        return news_list


class WebResponse:
    """The representation of hacker news get response.

    Attributes
    ----------
    url_hn : str
        The class attribute `url_hn` is for getting data from hacker
        news webpage.

    """

    url_hn = "https://news.ycombinator.com/news?p=0"

    def __init__(self, nr_webpages: int, get_data: list = None):

        self.nr_webpages = nr_webpages
        self.get_data = get_data

    @property
    def get_data(self):
        """list: Get current webcrawl response."""
        return self._get_data

    @get_data.setter
    def get_data(self, html_txt):
        self._get_data = html_txt

    @property
    def nr_webpages(self):
        """int: Get current number of pages to webcrawl.

        All values for`nr_webpages` <= 0, are converted to 1.
        """
        return self._nr_webpages

    @nr_webpages.setter
    def nr_webpages(self, nr_pages):
        if nr_pages <= 0:
            nr_pages = 1
        self._nr_webpages = nr_pages

    def get_response(self, pages=None) -> list:
        """Fetches data from a hacker news with GET method.

        Parameters
        ----------
        pages : int
            The number of `pages` that should be web crawled.

        Returns
        -------
        r_text : list
            The `r.text` is the list representation of the website.

        Raises
        ------
        ConnectionError
            If there is a genuine connection error to the webpage.
        ConnectionTimeout
            If a server does not response within 3s of a call.
        HTTPError
            If a http error is prompted.

        See Also
        --------
        requests.session.Session:
            For more information about session instance object.
        requests.api.get:
            For more information about parameter `timeout`.

        """
        connector = rqs()
        r_text = []
        stem = self.url_hn.split("=", maxsplit=1)[0]
        if not pages:
            pages = self.nr_webpages
        nr_pages = ["".join([stem, f"={i}"]) for i in range(pages)]
        for page in nr_pages:
            sleep(0.075)
            try:
                response = connector.get(url=page, timeout=3)

            except (ConnectionError, ConnectTimeout) as errors:
                print(f"{response.reason}:\n {errors}")
                continue

            except HTTPError as error:
                print(f"{response.reason}:\nHTTP error: {error}")
                continue

            else:
                connector.close()
                response.close()
                r_text.append(response.text)
            self._nr_webpages = pages
            self._get_data = r_text
        return r_text
