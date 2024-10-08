import numpy as np
from gerapy_auto_extractor.schemas.element import Element
from gerapy_auto_extractor.utils.preprocess import preprocess4content_extractor
from gerapy_auto_extractor.extractors.base import BaseExtractor
from gerapy_auto_extractor.utils.element import descendants_of_body


class BaseContentExtractor(BaseExtractor):
    """
    extract content from detail page
    """
    
    def process(self, element: Element):
        """
        extract content from html
        :param element:
        :return:
        """
        if content_xpath := self.kwargs.get("content_xpath"):
            descendants = element.xpath(content_xpath)
            descendant_first = descendants[0] if descendants else None
            if descendant_first is not None:
                return descendant_first
        # preprocess
        preprocess4content_extractor(element)
        
        # start to evaluate every child element
        element_infos = []
        descendants = descendants_of_body(element)
        
        # get std of density_of_text among all elements
        density_of_text = [descendant.density_of_text for descendant in descendants]
        density_of_text_std = np.std(density_of_text, ddof=1)
        
        # get density_score of every element
        for descendant in descendants:
            score = np.log(density_of_text_std) * \
                    descendant.density_of_text * \
                    np.log10(descendant.number_of_p_descendants + 2) * \
                    np.log(descendant.density_of_punctuation)
            descendant.density_score = score
        
        # sort element info by density_score
        descendants = sorted(descendants, key=lambda x: x.density_score, reverse=True)
        descendant_first = descendants[0] if descendants else None
        if descendant_first is None:
            return None
        return descendant_first


class ContentExtractor(BaseContentExtractor):

    def process(self, element: Element):
        """
        extract content from html
        :param element:
        :return:
        """
        element = super().process(element)
        if element is None:
            return None
        paragraphs = element.xpath('.//p//text()')
        paragraphs = [paragraph.strip() if paragraph else '' for paragraph in paragraphs]
        paragraphs = list(filter(lambda x: x, paragraphs))
        text = '\n'.join(paragraphs)
        text = text.strip()
        return text


class ContentHTMLExtractor(BaseContentExtractor):
    def process(self, element: Element):
        """
        extract content from html
        :param element:
        :return:
        """
        element = super().process(element)
        if element is None:
            return None
        return self.to_string(element)


content_extractor = ContentExtractor()
content_html_extractor = ContentHTMLExtractor()


def extract_content(html, **kwargs):
    """
    extract content from detail html
    :return:
    """
    return content_extractor.extract(html, **kwargs)


def extract_content_html(html, **kwargs):
    """
    extract content from detail html
    :return:
    """
    return content_html_extractor.extract(html, **kwargs)
