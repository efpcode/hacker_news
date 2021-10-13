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

    def html_parser(self) -> BeautifulSoup:
        try:
            if not self.web_content:
                raise ValueError(
                    "Expected instance attribute: `web_content` " "to exists"
                )
        except ValueError as error:
            empty = f"<p>This did not work has expected:\n" f"{error}</p>"
            Warning(error)
            return BeautifulSoup(empty, "html.parser")
        else:
            return BeautifulSoup(f"{self.web_content}", "html.parser")

    def data_filter(self):
        """
        Test docstring
        """
        return
        pass

    # Class methods

    @classmethod
    def webpage_txt(cls) -> str:
        """Class method `webpage_txt`, fetches data from a webpage
        with "GET" method.

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
                if count > 5:
                    raise ConnectionError(
                        "Attempts exceeded threshold of "
                        "maximum number of calls to "
                        "webpage."
                    )
                response = connector.get(url=cls.url_hn, timeout=3)

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
