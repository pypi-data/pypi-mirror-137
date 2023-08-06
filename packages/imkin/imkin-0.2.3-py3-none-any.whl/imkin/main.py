#!/usr/bin/env python3
import time
from collections import namedtuple
from urllib.parse import urljoin, quote
from .parsers import ImdbSearchParser, KinopoiskSearchParser, \
    KinopoiskParser, ImdbParser, KinopoiskSeriesParser, ImdbSeriesParser
from .utils import isallow, getd, getr, geth, parser_run_and_stop


def new(url):
    if not url.endswith("/"):
        url += "/"
    if not isallow(url):
        return None
    if "kinopoisk" in url:
        p = KinopoiskParser()
    else:
        p = ImdbParser()
    html = geth(url)
    parser_run_and_stop(p, html)
    Film = namedtuple("Film", "title alternate year time age isfilm url")
    return Film(p.title, p.alternate, p.year, p.time, p.age, p.isfilm, url)


def gettitles(url):
    titles = {}
    if not url.endswith("/"):
        url += "/"
    if not isallow(url):
        return {}
    if "kinopoisk" in url:
        parser = KinopoiskSeriesParser
    else:
        parser = ImdbSeriesParser
    html = geth(urljoin(url, "episodes/"))
    p = parser()
    parser_run_and_stop(p, html)
    titles = p.titles
    if "imdb" in url:
        uj = urljoin(url, "episodes?season=")
        try:
            season_last = int(p._season)
        except ValueError:
            return titles
        for i in range(1, season_last):
            time.sleep(1)
            html = geth(uj + str(i))
            if not html:
                continue
            ps = parser()
            parser_run_and_stop(ps, html)
            titles.update(ps.titles)
    return titles


def search(word):
    if len(word) < 2:
        return []
    key = quote(word.lower())
    result = []
    for url, parser in (("https://www.imdb.com/find?q=", ImdbSearchParser),
      ("https://www.kinopoisk.ru/index.php?kp_query=", KinopoiskSearchParser)):
        r = getr(url + key)
        if not r:
            continue
        data = getd(r.read())
        html = data.decode("utf8", errors="ignore")
        if "kinopoisk" in url and ("film" in r.url or "series" in r.url):
                p = KinopoiskParser()
                parser_run_and_stop(p, html)
                name = f"{p.title} / {p.alternate} ({p.year})"
                found = [(name, r.url)]
        else:
            p = parser()
            parser_run_and_stop(p, html)
            found = [(i, urljoin(url, j)) for i, j in p.found]
        result += found
    return result
