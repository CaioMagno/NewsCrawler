import requests, re
from bs4 import BeautifulSoup
from collections import namedtuple
import unicodedata
import re

from collections import namedtuple

class Article:
    def __init__(self, url, title, publishDate, content):
        self.url = url
        self.title = title
        self.publishDate = publishDate
        self.content = content

class NewsScrapper:
    def __init__(self):
        pass

    def buildSearchRequest(self, keywordsList, numPage):
        pass

    def httpRequest(self, request):
        pass

    def getLinksInResponseContent(self, response):
        pass

    def getTrueLinks(self, responseLinks):
        pass

    def getNewsContent(self, link):
        pass

    def getNewsHeadline(self, link):
        pass

    def getPublishDate(self, link):
        pass

    def getNewsArticlesParsed(self, keywordsList, numPage):
        pass


class NewsParser:
    def getNewsContent(self, pageSoup):
        pass

    def getNewsHeadline(self, pageSoup):
        pass

    def getSubtitle(self, pageSoup):
        pass

    def getPublishDate(self, pageSoup):
        pass

    def parsePage(self):
        response = requests.get(self.url)
        response.encoding = "utf-8"
        page_soup = BeautifulSoup(response.text, "lxml")
        Article = namedtuple("Article", "url date headline subtitle content")
        article = Article(url=self.url, date=self.getPublishDate(page_soup), headline=self.getNewsHeadline(page_soup),
                subtitle= self.getSubtitle(page_soup), content=self.getNewsContent(page_soup))

        return article

class NewsParserG1(NewsParser):
    def __init__(self, url):
        self.contentTextTagClass = "content-text__container"
        self.headlineTagClass = "content-head__title"
        self.url = url

    def getNewsContent(self, pageSoup):
        # page = self.httpRequest(link)
        # news_article_soup = BeautifulSoup(page.text, "lxml")
        paragraphsList = [p.text for p in pageSoup.find_all("p", class_=self.contentTextTagClass)]
        return paragraphsList

    def getNewsHeadline(self, pageSoup):
        if pageSoup.select("h1.content-head__title"):
            return pageSoup.select("h1.content-head__title")[0].text.strip()

    def getSubtitle(self, pageSoup):
        if pageSoup.find(name="h2", itemprop="alternativeHeadline") == None:
            return ""

        subtitle = pageSoup.find(name="h2", itemprop="alternativeHeadline").text.strip()
        return subtitle

    def getPublishDate(self, pageSoup):
        time_format = "%d/%m/%Y %Hh%M"
        timestamp = pageSoup.find(name="time", itemprop="datePublished")
        if timestamp:
            return timestamp.text.strip()


class NewsParserFolha(NewsParser):
    def __init__(self, url):
        self.url = url
        self.contentTextTagClass = "content-text__container"
        self.headlineTagClass = "content-head__title"

    def getNewsHeadline(self, pageSoup):
        headline = pageSoup.find(name="h1", itemprop="headline").text
        return headline

    def getSubtitle(self, pageSoup):
        subtitle = pageSoup.find(name="h2", itemprop="alternativeHeadline").text.strip()
        return subtitle

    def getPublishDate(self, pageSoup):
        date_published = pageSoup.article.time.text.strip()
        return date_published

    def getNewsContent(self, pageSoup):
        article_body = pageSoup.find(name="div", itemprop="articleBody")
        if article_body:
            paragraphs = article_body.find_all(name="p")
            paragraphsText = [paragraph.text.strip("\n") for paragraph in paragraphs]
            return paragraphsText
        else:
            return None


class NewsParserEstadao(NewsParser):
    def __init__(self, url):
        self.url = url

    def getNewsHeadline(self, pageSoup):
        headline = pageSoup.find(name="h1", class_="n--noticia__title").text
        return headline

    def getSubtitle(self, pageSoup):
        subtitle = pageSoup.find(name= "h2", class_="n--noticia__subtitle").text
        return subtitle

    def getPublishDate(self, pageSoup):
        date = list(pageSoup.find(name="div", class_="n--noticia__state").children)[3].text.strip()
        return date

    def getNewsContent(self, pageSoup):
        content_container = pageSoup.find(name="div", class_="n--noticia__content")
        content = [unicodedata.normalize("NFKD", paragraph.text.strip()) for paragraph in
                   content_container.find_all(name="p")]
        return content

class NewsParserUolPolitica(NewsParser):
    def __init__(self, url):
        self.url = url

    def getNewsHeadline(self, pageSoup):
        return pageSoup.find_all("h1")[1].text

    def getSubtitle(self, pageSoup):
        #Não possui subtitulo
        return ""

    def getPublishDate(self, pageSoup):
        date = pageSoup.find(name="span", class_="color1").text
        date = re.findall("(\d{2}/\d{2}/\d{4})", date)[0]
        return date

    def getNewsContent(self, pageSoup):
        content = [p.text for p in pageSoup.find(name = "div", attrs={"id": "texto"}).find_all("p", class_ = "")]
        return content




class NewsScrapperG1 (NewsScrapper):
    Tag = namedtuple("tag", "tag_name class_")

    def __init__(self):
        self.request = "https://g1.globo.com/busca/?q=KEYWORDS&species=notícias&page=PAGE_NUM"
        self.urlLinksTagClass = "busca-titulo"
        self.contentTextTagClass = "content-text__container"
        self.headlineTagClass = "content-head__title"

    def buildSearchRequest(self, keywordsList, numPage):
        query = "+".join(keywordsList)
        request = self.request.replace("KEYWORD", query)
        request = request.replace("PAGE_NUM", str(numPage))
        return request

    def httpRequest(self, request):
        return requests.get(request)

    def getLinksInResponseContent(self, response):
        soup = BeautifulSoup(response.text, "lxml")
        a_tags = soup.find_all("a", class_=self.urlLinksTagClass)
        links = ["https:" + a["href"] for a in a_tags]
        return links

    def getTrueLinks(self, responseLinks):
        def getLink(responseLink):
            response = requests.get(responseLink)
            link_extractor = ".+replace\(\"(.+)\"\).+"
            matches = re.match(link_extractor, response.text)
            return matches.group(1)

        trueLinks = [getLink(link) for link in responseLinks]
        return trueLinks

    def getNewsContent(self, pageSoup):
        # page = self.httpRequest(link)
        # news_article_soup = BeautifulSoup(page.text, "lxml")
        paragraphsList = [p.text for p in pageSoup.find_all("p", class_=self.contentTextTagClass)]
        return paragraphsList

    def getNewsHeadline(self, pageSoup):
        if pageSoup.select("h1.content-head__title"):
            return pageSoup.select("h1.content-head__title")[0].text

    def getPublishDate(self, pageSoup):
        time_format = "%d/%m/%Y %Hh%M"
        timestamp = pageSoup.find(name="time", itemprop="datePublished")
        if timestamp:
            return timestamp.text.strip()

    def getNewsArticlesParsed(self, keywordsList, numPage):
        request = self.buildSearchRequest(keywordsList, numPage)
        response = self.httpRequest(request)
        responselinks = self.getLinksInResponseContent(response)
        trueLinks = self.getTrueLinks(responselinks)
        pages = [self.httpRequest(link) for link in trueLinks]
        pagesSoup = [BeautifulSoup(page.text, "lxml") for page in pages]
        Article = namedtuple("Article", "url date headline texts")
        parsedLinks = {index: Article(url= page[0], date= self.getPublishDate(page[1]), headline= self.getNewsHeadline(page[1]), texts=self.getNewsContent(page[1])) for index, page in enumerate(zip(trueLinks, pagesSoup))}

        return parsedLinks

class NewsScrapperFolha(NewsScrapper):
    def __init__(self):
        self.request = "http://search.folha.uol.com.br/?q="
        self.urlLinksTagClass = "busca-titulo"
        self.contentTextTagClass = "content-text__container"
        self.headlineTagClass = "content-head__title"

    def buildSearchRequest(self, keywordsList, numPage):
        query = '+'.join(keywordsList)
        request = self.request + query
        return request

    def getLinksInResponseContent(self, response):
        soup = BeautifulSoup(response.text, "lxml")
        h3 = soup.find_all(name="h3", class_="search-results-title")
        urls = [htmlBlock.find("a")["href"] for htmlBlock in h3]
        return urls

    def getNewsHeadline(self, pageSoup):
        headline = pageSoup.find(name="h1", itemprop="headline").text
        return headline

    def getPublishDate(self, pageSoup):
        date_published = pageSoup.article.time.text.strip()
        return date_published

    def getNewsContent(self, pageSoup):
        article_body = pageSoup.find(name="div", class_="content", itemprop="articleBody")
        if article_body:
            paragraphs = article_body.find_all(name="p")
            paragraphsText = [paragraph.text.strip("\n") for paragraph in paragraphs]
            return paragraphsText
        else:
            return None

    def getNewsArticlesParsed(self, keywordsList, numPage):
        url = self.buildSearchRequest(keywordsList, numPage)
        response = requests.get(url)
        links = self.getLinksInResponseContent(response)
        pages = [requests.get(link) for link in links]
        pagesSoup = [BeautifulSoup(page.text, "lxml") for page in pages]
        Article = namedtuple("Article", "url date headline texts")
        parsedLinks = {index: Article(url=page[0], date=self.getPublishDate(page[1]), headline=self.getNewsHeadline(page[1]), texts=self.getNewsContent(page[1])) for index, page in enumerate(zip(links, pagesSoup))}
        return parsedLinks


if __name__ == "__main__":
    scrapper = NewsScrapperFolha()
    results = scrapper.getNewsArticlesParsed(["temer", "pmdb"], 1)
    print(results)