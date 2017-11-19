import requests, re
from bs4 import BeautifulSoup
from collections import namedtuple

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

    def getNewsArticlesParsed(self, keywordsList, numPage):
        pass

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

        trueLinks = [getLink(link   ) for link in responseLinks]
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

if __name__ == "__main__":
    scrapper = NewsScrapperG1()
    results = scrapper.getNewsArticlesParsed(["temer", "pmdb"], 1)
    print(results)