from __future__ import annotations


from getthenews.utils.soup import Scrape


def argument() -> None:
    scrape = Scrape()
    scrape.scrape()
