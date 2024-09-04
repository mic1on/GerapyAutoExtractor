METAS = [
    '//meta[starts-with(@property, "og:title")]/@content',
    '//meta[starts-with(@name, "og:title")]/@content',
    '//meta[starts-with(@property, "title")]/@content',
    '//meta[starts-with(@name, "title")]/@content',
    '//meta[starts-with(@property, "page:title")]/@content',
    '//meta[starts-with(@name, "ArticleTitle")]/@content',
    '//meta[starts-with(@name, "article_title")]/@content',
]

TITLE_HTAG_XPATH = '//h1//text() | //h2//text() | //h3//text() | //h4//text()'