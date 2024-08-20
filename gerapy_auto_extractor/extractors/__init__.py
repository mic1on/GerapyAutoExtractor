from gerapy_auto_extractor.extractors.content import extract_content, extract_content_html
from gerapy_auto_extractor.extractors.title import extract_title
from gerapy_auto_extractor.extractors.datetime import extract_datetime
from gerapy_auto_extractor.extractors.attachment import extract_attachment
from gerapy_auto_extractor.extractors.list import extract_list


def extract_detail(html, **kwargs):
    """
    extract detail information
    :param html:
    :return:
    """
    return {
        'title': extract_title(html, **kwargs),
        'datetime': extract_datetime(html, **kwargs),
        # 'content': extract_content(html),
        'content_html': extract_content_html(html, **kwargs),
        'attachment': extract_attachment(html, **kwargs)
    }
