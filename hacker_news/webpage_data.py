from requests import Session as rqs
from requests import ConnectTimeout, ConnectionError, HTTPError
from bs4 import BeautifulSoup


class WebPageData():
    """
    Class named 'WebPageData', represents the webpage data from hacker news

    Attributes
    ----------
    url_hn : str
        The source 'url_hn' for getting data from hacker news webpage.
    """
    url_hn = "https://news.ycombinator.com/news"

    @classmethod
    def webpage_txt(cls):
        """
        Class method called "webpage_txt", fetch data from webpage by "GET"
        method.

        Returns
        -------
        r.text : str
            The 'r.text' is the string representation of the website.

        Raises
        ------
        ConnectionError
            If maximum numbers of calls is exceed or it there is genuine
            connection error to webpage.

        ConnectionTimeout
            If a server does not response within 3s of a call.

        HTTPError
            If a http error is prompted.

        See Also
        --------
        requests.session.Session:
            For more information about session instance object.

        requests.api.get:
            For more information about parameter 'timeout' and GET-method
            used.

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


    def html_parser(self, web_content:str) -> str:
        pass


    def data_filter(self, html, vote_count):
        pass

