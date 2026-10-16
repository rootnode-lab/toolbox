# PDF to Images

PDF의 각 페이지를 PNG 또는 JPG 이미지 한 장으로 저장하는 도구입니다. 폴더를 전달받은 팀원은 최초 설치 후, 실행 명령의 **입력 PDF 경로와 출력 폴더 경로**만 바꿔 사용할 수 있습니다. Python 코드 안의 경로를 수정할 필요는 없습니다.

PDF 안에 삽입된 그림만 추출하는 도구가 아니라, 글자·표·그림이 포함된 페이지 전체를 이미지로 렌더링합니다.

## 공유할 파일

```text
pdf-to-images/
├── README.md
├── LICENSE
├── pdf_to_images.py
└── requirements.txt
```

위 네 파일이 포함된 폴더를 공유합니다. 각 사용자가 자신의 PC에서 설치하므로 `.venv` 폴더와 원본 PDF, 변환 결과는 함께 전달할 필요가 없습니다.

## 실행 환경

- Python 3.10~3.14
- PyMuPDF: `requirements.txt`에 버전 고정
- 검증 환경: Windows, Python 3.14.3, PyMuPDF 1.28.2

아래 예시는 Windows PowerShell 기준입니다. Adobe Acrobat이나 Poppler를 별도로 설치할 필요는 없습니다.

## 1. 최초 설치

전달받은 폴더의 실제 경로로 이동합니다.

```powershell
cd "C:\tools\pdf-to-images"
python --version
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

`python` 명령이 없고 `py`가 설치된 PC에서는 첫 두 Python 명령을 `py --version`, `py -m venv .venv`로 실행합니다. 둘 다 없다면 Python을 먼저 설치해야 합니다.

가상환경을 활성화하지 않고 `.\.venv\Scripts\python.exe`를 직접 사용하므로 PowerShell 실행 정책을 바꿀 필요가 없습니다.

## 2. 실행: 입력·출력 경로만 변경

설치한 폴더 안에서 다음 명령을 실행합니다.

```powershell
.\.venv\Scripts\python.exe .\pdf_to_images.py "C:\documents\보고서.pdf" --out "C:\documents\보고서_이미지"
```

바꿀 값:

| 값 | 의미 |
| --- | --- |
| `C:\documents\보고서.pdf` | 변환할 PDF 파일의 실제 경로 |
| `C:\documents\보고서_이미지` | 결과 이미지를 저장할 폴더. 없으면 자동 생성 |

경로에 공백이나 한글이 있어도 사용할 수 있습니다. 예시처럼 경로를 큰따옴표로 감싸세요.

PDF 원본은 수정하지 않습니다.

### 결과 예시

`보고서.pdf`가 3페이지인 경우:

```text
C:\documents\보고서_이미지\
├── 보고서_p1.png
├── 보고서_p2.png
└── 보고서_p3.png
```

파일명에는 PDF의 실제 페이지 번호를 사용합니다. 전체 페이지 수가 10~99이면 `p01`, 100~999이면 `p001`처럼 자릿수를 맞춥니다.

## 3. 자주 사용하는 명령

### 출력 경로 자동 지정

`--out`을 생략하면 PDF와 같은 위치의 `<PDF파일명>_images` 폴더에 저장합니다.

```powershell
.\.venv\Scripts\python.exe .\pdf_to_images.py "C:\documents\보고서.pdf"
```

### 특정 페이지만 변환

페이지 번호는 **1부터** 시작합니다. 쉼표와 범위를 함께 사용할 수 있습니다.

```powershell
.\.venv\Scripts\python.exe .\pdf_to_images.py "C:\documents\보고서.pdf" --pages "1,3,5-7"
```

지정한 순서로 처리하며 중복 페이지는 한 번만 변환합니다. 잘못된 형식, 역순 범위, 실제 페이지 수를 벗어난 번호는 해당 PDF의 변환을 시작하기 전에 오류로 처리합니다.

### JPG로 저장

```powershell
.\.venv\Scripts\python.exe .\pdf_to_images.py "C:\documents\보고서.pdf" --format jpg
```

JPG 저장 품질은 코드에서 95로 설정되어 있습니다. 글자와 도표 중심의 문서는 기본 PNG를 우선 사용하면 됩니다.

### 해상도 변경

기본 해상도는 300 DPI입니다.

```powershell
.\.venv\Scripts\python.exe .\pdf_to_images.py "C:\documents\보고서.pdf" --dpi 150
```

더 큰 이미지가 필요한 경우 `--dpi 400`처럼 지정할 수 있습니다. DPI가 높을수록 일반적으로 메모리 사용량, 처리 시간과 출력 크기가 증가합니다. 스캔 원본에 없는 세부 정보가 복원되지는 않습니다.

### 여러 PDF를 한 번에 변환

```powershell
.\.venv\Scripts\python.exe .\pdf_to_images.py "C:\documents\a.pdf" "C:\documents\b.pdf"
```

기본적으로 PDF별 `a_images`, `b_images` 폴더에 저장합니다.

- `--out`을 함께 지정하면 모든 PDF의 이미지를 같은 폴더에 저장합니다.
- 서로 다른 위치에 있는 동명 PDF는 같은 `--out`으로 한 번에 처리할 수 없습니다. PDF마다 다른 출력 경로를 지정하여 따로 실행하세요.
- `--pages`는 모든 PDF에 동일하게 적용합니다. 해당 범위가 없는 PDF는 실패하고 나머지 PDF는 계속 처리합니다.

### 도움말

```powershell
.\.venv\Scripts\python.exe .\pdf_to_images.py --help
```

## 4. 옵션

| 옵션 | 기본값 | 설명 |
| --- | --- | --- |
| `pdfs` | 필수 | 하나 이상의 PDF 파일 경로 |
| `--out` | PDF 옆 `<파일명>_images` | 출력 폴더 |
| `--dpi` | `300` | 1 이상의 정수 |
| `--format` | `png` | `png` 또는 `jpg` |
| `--pages` | 전체 페이지 | `"1,3,5-7"` 형식의 페이지 지정 |
| `--help` | — | 사용법 표시 |

상대 경로는 명령을 실행하는 현재 폴더 기준입니다. 혼동을 줄이려면 입력·출력에 절대 경로를 사용하세요.

## 5. 재실행 및 오류 처리

- 같은 출력 파일이 있으면 **덮어씁니다**. 이전 결과를 보관하려면 다른 `--out` 경로를 사용하세요.
- 이전 실행에서 만든 다른 페이지나 다른 형식의 이미지는 자동 삭제하지 않습니다.
- 암호 입력이 필요한 PDF는 지원하지 않습니다. 열기 암호를 해제한 사본을 사용하세요.
- 읽기 권한이 있는 PDF 경로와 쓰기 권한이 있는 출력 폴더를 지정하세요.
- 처리 중 오류가 나면 이미 저장된 이미지는 남을 수 있습니다. 결과 목록과 오류 메시지를 함께 확인하세요.
- 여러 PDF 중 일부가 실패해도 나머지 PDF의 변환은 계속합니다.

종료 코드:

| 코드 | 의미 |
| --- | --- |
| `0` | 모든 PDF 변환 성공 또는 도움말 표시 |
| `1` | 하나 이상의 PDF 변환 실패 |
| `2` | 잘못된 명령행 옵션 또는 입력 간 출력 파일명 충돌 |

PowerShell에서는 실행 직후 `$LASTEXITCODE`로 확인할 수 있습니다.

### PyMuPDF 설치 오류

스크립트 실행에 사용하는 것과 같은 Python으로 라이브러리를 설치합니다.

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

설치된 Python이 없어 명령을 찾지 못하는 문제와, PyMuPDF가 설치되지 않은 문제를 구분하세요.


## 6. 라이선스

이 폴더의 직접 작성한 코드와 문서는 **GNU Affero General Public License v3.0 only (AGPL-3.0-only)**로 제공합니다. 전체 조건은 함께 제공하는 [LICENSE](LICENSE)를 확인하세요.

외부 라이브러리는 해당 저작권자의 라이선스를 따릅니다. PyMuPDF 1.28.2는 AGPL 또는 Artifex 상용 라이선스로 제공됩니다. 이 도구에 적용한 라이선스가 PyMuPDF의 라이선스 조건을 대체하지 않습니다.

- [PyMuPDF 라이선스 안내](https://pymupdf.readthedocs.io/en/latest/about.html#license-and-copyright)
- [PyMuPDF 1.28.2 배포 및 소스 정보](https://pypi.org/project/pymupdf/1.28.2/)

팀원에게 폴더를 공유할 때는 README, 소스 코드, requirements.txt와 LICENSE를 함께 전달하세요.

## 공식 참고 문서

- [PyMuPDF 1.28.2](https://pypi.org/project/pymupdf/1.28.2/)
- [PyMuPDF 설치](https://pymupdf.readthedocs.io/en/latest/installation.html)
- [페이지 이미지 렌더링](https://pymupdf.readthedocs.io/en/latest/page.html#Page.get_pixmap)
