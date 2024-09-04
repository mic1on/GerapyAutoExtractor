import re
from dateparser import parse
from lxml.html import HtmlElement
from gerapy_auto_extractor.patterns.datetime import METAS_CONTENT, REGEXES
from loguru import logger
from gerapy_auto_extractor.extractors.base import BaseExtractor


class DatetimeExtractor(BaseExtractor):
    """
    Datetime Extractor which auto extract datetime info.
    """

    def extract_by_xpath(self, element: HtmlElement) -> str:
        """
        extract datetime by xpath
        :param element:
        :return:
        """
        xpath = self.kwargs.get("datetime_xpath")
        if not xpath:
            return ''
        text = ''.join(element.xpath(xpath))
        for regex in REGEXES:
            result = re.search(regex, text)
            if result:
                return result.group(1)

    def extract_by_regex(self, element: HtmlElement) -> str:
        """
        extract datetime according to predefined regex
        :param element:
        :return:
        """
        text = ''.join(element.xpath('.//text()'))
        for regex in REGEXES:
            result = re.search(regex, text)
            if result:
                return result.group(1)
    
    def extract_by_meta(self, element: HtmlElement) -> str:
        """
        extract according to meta
        :param element:
        :return: str
        """
        for xpath in METAS_CONTENT:
            datetime = element.xpath(xpath)
            if datetime:
                return ''.join(datetime)
    
    def process(self, element: HtmlElement):
        """
        extract datetime
        :param element:
        :return:
        """
        return (
                self.extract_by_xpath(element)
                or self.extract_by_meta(element)
                or self.extract_by_regex(element)
        )


datetime_extractor = DatetimeExtractor()


def parse_datetime(datetime):
    """
    parse datetime using dateparser lib
    :param datetime:
    :return:
    """
    if not datetime:
        return None
    try:
        return parse(datetime)
    except TypeError:
        logger.exception(f'Error Occurred while parsing datetime extracted. datetime is {datetime}')


def extract_datetime(html, **kwargs):
    """
    extract datetime from html
    :param html:
    :return:
    """
    parse = kwargs.get('parse', True)
    result = datetime_extractor.extract(html, **kwargs)
    if not parse:
        return result
    return parse_datetime(result)
