# korean_ebook_to_skill/anthology.py
"""ANTHOLOGY 서브청크 — ch8 완결사례집을 케이스(N.M절) 단위로 분할.

``## N.M <제목>`` 헤더를 기준으로 원문을 분할한다. 각 청크는 하나의 완결 사례
(Palantir/OpenAI/...)에 대응하며, ``### 방법론 환원`` 블록은 다음 ``## `` 헤더
직전까지 한 청크 내에 보존된다(분할 정규식이 ``## `` 에만 lookaround).

v1 단일청크 대비 이득: 5개 사례가 각각 독립 후보(id/source_ref)로 추출되어
회상률 가시성 확보. ``id``는 ``"{chapter}-{N.M}"`` (예 ``"08-8.1"``) →
``source_refs`` 의 ``chNN§N.M`` 와 대응.
"""
import re
from .models import ChapterFile, Chunk

# ``## 8.1 `` 같은 절 헤더 직전 위치에서 분할 (헤더 자체는 청크에 포함).
_SPLIT_RE = re.compile(r"(?=^## \d+\.\d+\s)", re.MULTILINE)
# 분할된 각 파트에서 헤더 번호(N.M)와 제목을 추출.
_HEAD_RE = re.compile(r"^## (?P<h>\d+\.\d+)\s+(?P<t>.+)$", re.MULTILINE)


def subchunk_anthology(cf: ChapterFile) -> list:
    """ANTHOLOGY 챕터를 ``## N.M`` 절 단위 청크로 분할.

    헤더가 없는 서두(도입단락)는 청크로 만들지 않는다 — 사례 단위 추출이 목적이므로.
    """
    parts = _SPLIT_RE.split(cf.raw_text)
    chunks = []
    for p in parts:
        m = _HEAD_RE.search(p)
        if m:
            chunks.append(
                Chunk(
                    id=f"{cf.number}-{m.group('h')}",
                    heading=m.group("h"),
                    title=m.group("t").strip(),
                    text=p,
                )
            )
    return chunks
