"""HTML → readable plain text, for job descriptions that arrive as markup.

Does: drop script/style/nav-type elements, turn block elements and <br> into line breaks,
collapse whitespace, unescape entities.

Also: `clean_posting_text`, the one check every posting passes on its way into the database
and on its way out to a reader (HIR-420). A source that says it sends plain text sometimes
sends markup, and markup sometimes arrives with its tags entity-escaped (`&lt;p&gt;`), which
has no `<` in it and so used to be unescaped into visible tags instead of parsed.

Does NOT: parse JSON-LD, pick the "main" part of a page, or handle non-HTML input specially
(plain text passes through unchanged apart from whitespace normalization).

Invariant: output has no tags, no runs of more than two newlines, no trailing whitespace.
Text counts as markup only when it holds two or more formatting tags (`looks_like_markup`),
so "experience < 3 years", `List<String>` or one mention of "<br>" in a plain posting is
left alone.
"""

import html
import re
from html.parser import HTMLParser

_BLOCK = {"p", "div", "li", "ul", "ol", "br", "h1", "h2", "h3", "h4", "h5", "h6",
          "tr", "section", "article", "header", "footer", "blockquote", "pre"}
_SKIP = {"script", "style", "noscript", "svg", "head"}


class _Extractor(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self._skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in _SKIP:
            self._skip += 1
        elif tag in _BLOCK:
            self.parts.append("\n")
            if tag == "li":
                self.parts.append("- ")

    def handle_endtag(self, tag):
        if tag in _SKIP:
            self._skip = max(0, self._skip - 1)
        elif tag in _BLOCK:
            self.parts.append("\n")

    def handle_data(self, data):
        if not self._skip:
            self.parts.append(data)


# Tags a job posting's markup is made of. Deliberately not "anything in angle brackets":
# plain postings contain `<`, generics and placeholders like <your name>.
_TAG = re.compile(
    r"</?(?:p|div|span|br|li|ul|ol|h[1-6]|strong|em|b|i|u|a|font|table|tbody|tr|td|th|"
    r"section|article|blockquote)(?:\s[^<>]*)?/?>", re.IGNORECASE)
MIN_TAGS = 2


def looks_like_markup(text: str) -> bool:
    """True when the text is HTML rather than a posting's words: MIN_TAGS or more
    formatting tags, written out or entity-escaped once."""
    return (len(_TAG.findall(text)) >= MIN_TAGS
            or ("&lt;" in text and len(_TAG.findall(html.unescape(text))) >= MIN_TAGS))


def clean_posting_text(text: str) -> str:
    """A posting's text as plain text. Text that is not markup comes back untouched, so
    this is safe on every posting, stored or new. Twice, because markup sometimes carries
    more markup inside it with the tags escaped, which the first pass turns into tags."""
    for _ in range(2):
        if not looks_like_markup(text):
            break
        text = html_to_text(text)
    return text


def html_to_text(markup: str) -> str:
    parse = "<" in markup
    if not parse:
        markup = html.unescape(markup)     # plain text, or markup whose tags were escaped
        parse = looks_like_markup(markup)
    if parse:
        p = _Extractor()
        p.feed(markup)
        p.close()
        text = "".join(p.parts)
    else:
        text = markup
    text = re.sub(r"[ \t\r\f\v]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()
