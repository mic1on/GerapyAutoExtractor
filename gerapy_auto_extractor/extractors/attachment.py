import re

from gerapy_auto_extractor.extractors.base import BaseExtractor
from lxml.html import HtmlElement
from gerapy_auto_extractor.patterns.title import METAS
from gerapy_auto_extractor.utils.element import children, a_descendants
from gerapy_auto_extractor.utils.lcs import lcs_of_2
from gerapy_auto_extractor.utils.similarity import similarity2, get_longest_common_sub_string


class AttachmentExtractor(BaseExtractor):
    """
    attachment Extractor which extract attachment of page
    """
    def process(self, element: HtmlElement):
        """
        extract attachment from element
        :param element:
        :return:
        """
        for linked_descendant in element.a_descendants:
            pass
        pass


attachment_extractor = AttachmentExtractor()


def extract_attachment(html):
    """
    extract attachment from html
    :param html:
    :return:
    """
    result = attachment_extractor.extract(html)
    return result
