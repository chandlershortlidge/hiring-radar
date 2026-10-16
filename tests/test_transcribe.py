import base64
import hashlib
from types import SimpleNamespace

import pytest

from app import transcribe as tr

PNG = b"\x89PNG\r\n\x1a\n" + b"\x00" * 16
JPEG = b"\xff\xd8\xff\xe0" + b"\x00" * 16
WEBP = b"RIFF\x00\x00\x00\x00WEBP" + b"\x00" * 8


def test_media_type_sniffing():
    assert tr.media_type_of(PNG) == "image/png"
    assert tr.media_type_of(JPEG) == "image/jpeg"
    assert tr.media_type_of(WEBP) == "image/webp"
    with pytest.raises(tr.TranscriptionError):
        tr.media_type_of(b"RIFF\x00\x00\x00\x00WAVE")
    with pytest.raises(tr.TranscriptionError):
        tr.media_type_of(b"%PDF-1.4")


def test_request_carries_image_and_general_prompt():
    req = tr.build_request(PNG, "m")
    img, text = req["messages"][0]["content"]
    assert img["source"]["media_type"] == "image/png"
    assert base64.b64decode(img["source"]["data"]) == PNG
    assert "Transcribe" in text["text"] and "linkedin" not in text["text"].lower()


def response(text="Hello", stop="end_turn", blocks=None):
    content = blocks if blocks is not None else [SimpleNamespace(type="text", text=text)]
    return SimpleNamespace(stop_reason=stop, content=content, usage=SimpleNamespace(input_tokens=1, output_tokens=2))


class FakeClient:
    def __init__(self, resp):
        self.resp, self.calls = resp, 0
        self.messages = self

    def create(self, **kw):
        self.calls += 1
        return self.resp


def test_transcribe_returns_text_hash_and_type():
    t = tr.transcribe(PNG, FakeClient(response("AI Engineer\n- Python")), "m")
    assert t.text == "AI Engineer\n- Python"
    assert t.sha256 == hashlib.sha256(PNG).hexdigest()
    assert t.media_type == "image/png" and t.usage == {"input_tokens": 1, "output_tokens": 2}


@pytest.mark.parametrize("resp", [response(stop="max_tokens"), response(stop="refusal"),
                                  response(text="   "), response(blocks=[])])
def test_transcribe_raises_on_bad_responses(resp):
    with pytest.raises(tr.TranscriptionError):
        tr.transcribe(PNG, FakeClient(resp), "m")
