"""test_assets.py — Step 3 이미지 추출 TDD."""
import fitz


def _make_img_pdf(path):
    doc = fitz.open()
    p = doc.new_page()
    pix = fitz.Pixmap(fitz.csRGB, fitz.IRect(0, 0, 4, 4))   # 4x4 빈 RGB
    p.insert_image(fitz.Rect(72, 72, 144, 144), pixmap=pix)
    doc.save(str(path))
    doc.close()


def test_extract_image(tmp_path):
    from scripts.extract_assets import extract
    pdf = tmp_path / "img.pdf"
    _make_img_pdf(pdf)
    out = tmp_path / "out"
    n = extract(str(pdf), str(out))
    assert n >= 1
    imgs = list((out / "assets" / "images").glob("fig-*.png"))
    assert len(imgs) >= 1
    assert (out / "assets" / "tables").is_dir()   # 예약 디렉토리


def test_extract_no_image(tmp_path):
    from scripts.extract_assets import extract
    pdf = tmp_path / "empty.pdf"
    doc = fitz.open(); doc.new_page(); doc.save(str(pdf)); doc.close()
    out = tmp_path / "out"
    n = extract(str(pdf), str(out))
    assert n == 0
    assert (out / "assets" / "images").is_dir()   # 디렉토리는 항상 생성
