from __future__ import annotations

from getthenews.utils.command_line import command_line_arg

import requests
from typing import (Dict, List)
from fake_headers import Headers


from rich.console import Console

from bs4 import BeautifulSoup
from requests.models import Response


class Requests:
    def __init__(self) -> None:
        self.req = requests.Session()

    def get_headers(self) -> Dict[str, str]:
        headers = Headers(
            browser="random_browser",
            os="random_os",
            headers=True
        ).generate()
        return headers

    def make_call(self) -> Response:
        headers = self.get_headers()
        cli_args = command_line_arg()
        url = f"https://google.com/search?q={cli_args.query.lower()}&tbm=nws&lr=lang_{cli_args.lang}&hl={cli_args.lang}&sort=date&num={cli_args.size}"
        return self.req.get(url, headers=headers)


class Scrape:

    def __init__(self) -> None:
        self.console = Console()
        self.req = Requests()
        self.soup = BeautifulSoup(self.req.make_call().content, "lxml")

    def scrape(self) -> None:
        soup = self._scrape_data()
        divs_list = self._get_div(soup)
        return self._scrape(divs_list)

    def _scrape(self, divs_list: List[str]) -> None:
        for div in divs_list:
            title = div.find("span").text
            text = div.text.replace(title, "")
            link = div.find("a", href=True)['href']
            self.console.print("Source: ", title, style="bold green")
            self.console.print("Text: ", text, style="bold cyan")
            self.console.print("Read more : ", link)
            self.console.print("\n")

    def _get_div(self, soup: BeautifulSoup) -> List[str]:
        class_ = ".ftSUBd"
        div_ = soup.select(class_)
        return div_

    def _scrape_data(self) -> BeautifulSoup:
        return self.soup
