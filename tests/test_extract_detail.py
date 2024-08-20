import os
from pprint import pprint

from gerapy_auto_extractor.utils.element import html2element

os.environ['APP_DEBUG'] = 'true'

import unittest
from tests.settings import SAMPLES_DETAIL_DIR
from tests.test_base import TestBase
from gerapy_auto_extractor.extractors.title import title_extractor
from gerapy_auto_extractor.extractors.content import content_html_extractor
from gerapy_auto_extractor.extractors import extract_detail


class TestExtractDetail(TestBase):
    samples_dir = SAMPLES_DETAIL_DIR

    def test_extract_title(self):
        html = self.html('gov_news.html')
        element = html2element(html)
        title = title_extractor.process(element)
        print('Title', title)
        self.assertEqual(title, '凯里市教育系统2024年公开招聘事业单位工作人员实施方案')

    def test_extract_content(self):
        html = self.html('gov_news.html')
        element = html2element(html)
        content = content_html_extractor.process(element)
        print('Content', content)

    def test_extract_detail(self):
        html = self.html('gov_news.html')
        # element = html2element(html)
        detail = extract_detail(html, content_xpath="//div[@class='mainbox']")
        detail['content_html'] = detail['content_html'][:120]
        pprint(detail)


if __name__ == '__main__':
    unittest.main()
