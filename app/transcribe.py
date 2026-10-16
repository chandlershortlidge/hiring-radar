"""Stage 1: job-posting screenshot → verbatim transcript.

Does: send the image to the vision model and return the posting's text, with section
headings and bullets preserved as plain text, UI chrome left out. Also sniffs the image
media type and computes its SHA-256 so callers can store the bytes.

Does NOT: extract skills (that's stage 2, which only ever sees text), retry, store
anything, or decide what to do with a screenshot that isn't a job posting (it returns
whatever the model transcribed; the title filter and a zero-skill extraction catch junk).

Invariants: output is plain text; a response that is empty, truncated (max_tokens), or
a refusal raises TranscriptionError rather than returning partial text; the prompt is
general — nothing about specific sites or postings.
"""

import base64
import hashlib
import os
from dataclasses import dataclass

DEFAULT_MODEL = os.environ.get("HIRING_RADAR_VISION_MODEL", os.environ.get("HIRING_RADAR_MODEL", "claude-sonnet-5-5"))
MAX_TOKENS = 4096

PROMPT = """\
This image is a screenshot of a job posting. Transcribe the posting's text verbatim.

- Keep section headings on their own line and keep bullet points as lines starting with "- ".
- Keep the company name, job title and location if they are visible.
- Leave out anything that is not part of the posting itself: navigation, apply/save/share
  buttons, "similar jobs", applicant counts, ads, cookie banners, browser chrome.
- Do not summarize, translate, correct, or add anything. If text is cut off at the edge of
  the image, transcribe what is visible and stop.

Output only the transcript."""

_MAGIC = {b"\x89PNG": "image/png", b"\xff\xd8\xff": "image/jpeg", b"RIFF": "image/webp", b"GIF8": "image/gif"}


class TranscriptionError(RuntimeError):
    pass


@dataclass(frozen=True)
class Transcript:
    text: str
    sha256: str
    media_type: str
    usage: dict


def media_type_of(data: bytes) -> str:
    for magic, mt in _MAGIC.items():
        if data.startswith(magic):
            if mt == "image/webp" and data[8:12] != b"WEBP":
                continue
            return mt
    raise TranscriptionError("unsupported image type (need PNG, JPEG, WebP or GIF)")


def build_request(data: bytes, model: str) -> dict:
    return {
        "model": model,
        "max_tokens": MAX_TOKENS,
        "messages": [{"role": "user", "content": [
            {"type": "image", "source": {"type": "base64", "media_type": media_type_of(data),
                                         "data": base64.b64encode(data).decode("ascii")}},
            {"type": "text", "text": PROMPT},
        ]}],
    }


def parse_response(response) -> str:
    if response.stop_reason == "max_tokens":
        raise TranscriptionError("transcript truncated (max_tokens)")
    if response.stop_reason == "refusal":
        raise TranscriptionError("model refused")
    text = "\n".join(b.text for b in response.content if getattr(b, "type", None) == "text").strip()
    if not text:
        raise TranscriptionError("empty transcript")
    return text


def make_client():
    import anthropic
    return anthropic.Anthropic()


def transcribe(data: bytes, client, model: str = DEFAULT_MODEL) -> Transcript:
    response = client.messages.create(**build_request(data, model))
    usage = getattr(response, "usage", None)
    return Transcript(
        text=parse_response(response),
        sha256=hashlib.sha256(data).hexdigest(),
        media_type=media_type_of(data),
        usage={k: getattr(usage, k, None) for k in ("input_tokens", "output_tokens")} if usage else {},
    )
