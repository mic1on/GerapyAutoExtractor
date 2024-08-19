import os
from pprint import pprint

from gerapy_auto_extractor.utils.element import html2element

os.environ['APP_DEBUG'] = 'true'

import unittest
from tests.settings import SAMPLES_DETAIL_DIR
from tests.test_base import TestBase
from gerapy_auto_extractor.extractors.attachment import attachment_extractor


class TestExtractAttachment(TestBase):
    samples_dir = SAMPLES_DETAIL_DIR

    def test_extract_attachment(self):
        html = self.html('gov_news.html')
        element = html2element(html)
        attachment = attachment_extractor.process(element)
        print('attachment', attachment)


if __name__ == '__main__':
    unittest.main()
