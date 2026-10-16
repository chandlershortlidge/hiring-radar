"""HTML → readable plain text, for job descriptions that arrive as markup.

Does: drop script/style/nav-type elements, turn block elements and <br> into line breaks,
collapse whitespace, unescape entities.

Does NOT: parse JSON-LD, pick the "main" part of a page, or handle non-HTML input specially
(plain text passes through unchanged apart from whitespace normalization).

Invariant: output has no tags, no runs of more than two newlines, no trailing whitespace.
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


def html_to_text(markup: str) -> str:
    if "<" not in markup:
        text = html.unescape(markup)
    else:
        p = _Extractor()
        p.feed(markup)
        p.close()
        text = "".join(p.parts)
    text = re.sub(r"[ \t\r\f\v]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()
