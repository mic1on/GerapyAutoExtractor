import re

from gerapy_auto_extractor.extractors.base import BaseExtractor
from lxml.html import HtmlElement
from gerapy_auto_extractor.patterns.title import METAS, TITLE_HTAG_XPATH
from gerapy_auto_extractor.utils.similarity import get_longest_common_sub_string


class TitleExtractor(BaseExtractor):
    """
    Title Extractor which extract title of page
    """

    def extract_by_xpath(self, element: HtmlElement) -> str:
        """
        extract title by xpath
        :param element:
        :return:
        """
        xpath = self.kwargs.get("title_xpath")
        if not xpath:
            return ''
        title = element.xpath(xpath)
        return title[0] if title else ''

    def extract_by_meta(self, element: HtmlElement) -> str:
        """
        extract according to meta
        :param element:
        :return: str
        """
        for xpath in METAS:
            title = element.xpath(xpath)
            if title:
                return ''.join(title)

    def extract_by_title(self, element: HtmlElement):
        """
        get title from <title> tag
        :param element:
        :return:
        """
        return ''.join(element.xpath('//title//text()')).replace('\t', '').strip()

    def extract_by_hs(self, element: HtmlElement):
        """
        get title from all h1-h3 tag
        :param element:
        :return:
        """
        hs = element.xpath('//h1//text()|//h2//text()|//h3//text()')
        return hs or []

    def extract_by_h(self, element: HtmlElement):
        """
        extract by h tag, priority h1, h2, h3
        :param elemeent:
        :return:
        """
        for xpath in ['//h1', '//h2', '//h3']:
            children = element.xpath(xpath)
            if not children:
                continue
            child = children[0]
            texts = child.xpath('./text()')
            if texts and len(texts):
                return texts[0].strip()

    def extract_by_htag_and_title(self, element: HtmlElement) -> str:
        h_tag_texts_list = element.xpath('(//h1//text() | //h2//text() | //h3//text() | //h4//text() | //h5//text())')
        title_text = ''.join(element.xpath('//title/text()'))
        title_text = title_text.strip().replace('\t', '')
        news_title = ''
        for h_tag_text in h_tag_texts_list:
            lcs = get_longest_common_sub_string(title_text, h_tag_text)
            if len(lcs) > len(news_title):
                news_title = lcs
        return news_title if len(news_title) > 4 else ''

    def extract_by_title(self, element):
        title_list = element.xpath('//title/text()')
        if not title_list:
            return ''
        title = re.split('[-_|]', title_list[0])
        return max(title, key=lambda x: len(x))

    def extract_by_htag(self, element):
        title_list = element.xpath(TITLE_HTAG_XPATH)
        if not title_list:
            return ''
        return title_list[0]

    def process(self, element: HtmlElement):
        """
        extract title from element
        :param element:
        :return:
        """
        title = (self.extract_by_xpath(element)
                 or self.extract_by_meta(element)
                 or self.extract_by_htag_and_title(element)
                 or self.extract_by_title(element)
                 or self.extract_by_htag(element)
                 )
        title = title.strip()
        return title


title_extractor = TitleExtractor()


def extract_title(html, **kwargs):
    """
    extract title from html
    :param html:
    :return:
    """
    result = title_extractor.extract(html, **kwargs)
    return result
