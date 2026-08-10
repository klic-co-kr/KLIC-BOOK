# Windows 설치 메모

## 권장 환경

- Python 3.11 또는 3.12
- WeasyPrint 68.x
- Poppler for Windows: `pdftoppm`, `pdftotext`, `pdffonts`
- NanumMyeongjo, NanumSquare 또는 Noto CJK 한국어 글꼴

## PowerShell 설치

```powershell
cd korean-ebook
powershell -ExecutionPolicy Bypass -File .\scripts\install.ps1
```

가상환경을 직접 만들려면:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r .\scripts\requirements.txt
```

## 실행 예

```powershell
python .\scripts\publish_book.py `
  --input "C:\work\manuscript.zip" `
  --output-dir "C:\work\out" `
  --config ".\assets\book-config.example.yaml"
```

Poppler가 PATH에 없으면 렌더 스크립트는 PyMuPDF로 대체한다. 다만 글꼴 임베딩과 `pdftotext` 기반 검수 일부는 제한될 수 있으며 검수 보고서에 `unverified`로 표시된다.


## FDE 편집본 재현

```powershell
python .\scripts\run_pipeline.py `
  --input "C:\work\포워드-디플로이드-엔지니어-한국어판.zip" `
  --output-dir "C:\work\fde-out" `
  --config ".\assets\book-config.fde-example.yaml"
```
