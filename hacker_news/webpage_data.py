from requests import Session as rqs
from requests import ConnectTimeout, ConnectionError, HTTPError
from bs4 import BeautifulSoup


class WebPageData:
    """
    Class named 'WebPageData', represents the webpage data from hacker
    news website.

    Attributes
    ----------
    url_hn : str
        The source 'url_hn' for getting data from hacker news webpage.
    """
    url_hn = "https://news.ycombinator.com/news"

    def __init__(self, web_content: str, vote_count: int = 100) -> None:
        """
        The needed arguments to create an instance of WebPageData.

        Parameters
        ----------
        web_content: str
            The 'web_content'the string output from hacker news
            website i.e. all html elements.

        vote_count: int
            The 'vote_count' parameter is the threshold data needs to
             be exceeded or equal to for an article to be considered
             an item of interest.
        """
        self.web_content = web_content
        self.vote_count = vote_count

    def html_parser(self):
        return BeautifulSoup(f"{self.web_content}", "html.parser")

    def data_filter(self):
        pass

    # Class methods

    @classmethod
    def webpage_txt(cls):
        """
        Class method called "webpage_txt", fetch data from webpage
        by "GET" method.

        Returns
        -------
        r.text : str
            The 'r.text' is the string representation of the website.

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
                if count > 5:
                    raise ConnectionError("Attempts exceeded threshold of "
                                          "maximum number of calls to "
                                          "webpage.")
                r = connector.get(url=cls.url_hn, timeout=3)

            except (ConnectionError, ConnectTimeout) as errors:
                print(f"{r.reason}:\n {errors}")
                continue
            except HTTPError as error:
                print(f"{r.reason}:\nHTTP error: {error}")
                continue
            else:
                return r.text
