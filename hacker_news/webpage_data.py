"""The module webpage_data fetches data from hacker news.

Notes
-----
This module is not executable as script and class should be imported
as shown in `Example`

See Also
--------
hacker_news.webpage_data.WebPageData :
    For more information on how data fetch from source webpage.

Example
-------
>>> from webpage_data import WebPageData

>>> web_obj = WebPageData(WebPageData.webpage_txt(), vote_count= 150)

>>> print(web_obj)
Fetched data from https://news.ycombinator.com/news:
 [Title, Points, Link]

"""


from requests import Session as rqs
from requests import ConnectTimeout, ConnectionError, HTTPError
from bs4 import BeautifulSoup


class WebPageData:
    """'WebPageData', represents the webpage data from hacker news website.

    Attributes
    ----------
    url_hn : str
        The class attribute `url_hn` is for getting data from hacker
        news webpage.
    web_content : str
        The instance attribute called `web_content` is the string
        output from hacker news website.
    vote_count : int
        The instance attribute `vote_count` is the threshold value
        for an article to be considered an item of interest. Default
        value = 100.

    """

    url_hn = "https://news.ycombinator.com/news"

    def __init__(self, web_content: str, vote_count: int = 100) -> None:

        self.web_content = web_content
        self.vote_count = vote_count

    def __str__(self):
        """A user friendly prompt of the instance."""
        return f"Fetched data from {self.url_hn}:\n [Title, Points, Link]"

    def __repr__(self):
        """The representation of a instance object of class."""
        return (
            f"WebPageData(web_content=WebPageData.webpage_txt(), "
            f"vote_count= {self.vote_count})"
        )

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
        news_list_sorted : list
            A descending ordered nested-list data type based on
            the number of points an article has.
        """
        news_list_sorted = data_list.sort(key=lambda x: x[1], reverse=True)

        return news_list_sorted

    @staticmethod
    def html_parser(web_content: str) -> BeautifulSoup:
        """Parses web content.

        The method parses the web content in `url_hn` and returns a
        BeautifulSoup object, that function like a css selector.

        Parameters
        ----------
        web_content : str
            The `web_content` parameter is a string object that
            contains html text.

        Returns
        -------
        BeautifulSoup : object
            The `BeautifulSoup` object returned, is an actual instance
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
    def data_filter(data_parsed, nr_points=100, ordered_data=True) -> dict:
        """Helper method that filter web content by threshold.

        The method filters the web content on an arbitrary threshold,
        that can be modified by user.

        Parameters
        ----------
        data_parsed : bs4.BeautifulSoup(object)
            The `data_parsed` parameter is the return value from
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

    # Class methods

    @classmethod
    def webpage_txt(cls) -> str:
        """Fetches data from a webpage with "GET" method.

        Returns
        -------
        r.text : str
            The `r.text` is the string representation of the website.

        Raises
        ------
        ConnectionError
            If maximum numbers of calls is exceed or there is a
            genuine connection error to the webpage.
        ConnectionTimeout
            If a server does not response within 3s of a call.
        HTTPError
            If a http error is prompted.

        See Also
        --------
        requests.session.Session:
            For more information about session instance object.
        requests.api.get:
            For more information about parameter 'timeout' and
            GET-method used.

        """
        connector = rqs()
        count = 0
        while count <= 5:
            count += 1
            try:
                response = connector.get(url=cls.url_hn, timeout=3)
                if count > 5:
                    raise ValueError(
                        "Attempts exceeded threshold of "
                        "maximum number of calls to "
                        "webpage."
                    )

            except ValueError as error:
                print(error)
                continue

            except (ConnectionError, ConnectTimeout) as errors:
                print(f"{response.reason}:\n {errors}")
                continue

            except HTTPError as error:
                print(f"{response.reason}:\nHTTP error: {error}")
                continue

            else:
                connector.close()
                response.close()
                return response.text
