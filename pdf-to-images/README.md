# PDF to Images

PDF의 각 페이지를 PNG 이미지로 저장합니다. **Windows PowerShell 기준**입니다.

## 1. 최초 설치 — PC에서 한 번만

Python 3.10~3.14가 설치된 PC에서 진행하세요.

**아래 명령을 순서대로 한 줄씩 입력하고 Enter를 누르세요. 앞 명령이 끝난 뒤 다음 명령을 실행합니다.**

### 1-1. 도구 폴더로 이동

아래 경로를 본인 PC의 `pdf-to-images` 폴더 경로로 바꾸세요.

```powershell
cd "C:\tools\pdf-to-images"
```

### 1-2. 실행 환경 만들기

다음 명령은 그대로 입력하세요.

```powershell
python -m venv .venv
```

### 1-3. 필요한 라이브러리 설치

다음 명령도 그대로 입력하고, 설치가 끝날 때까지 기다리세요.

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

> **참고:** 가상환경을 활성화하지 않고 `.\.venv\Scripts\python.exe`를 직접 사용하므로 PowerShell 실행 정책을 바꿀 필요가 없습니다.

## 2. PDF 변환 — 사용할 때마다

### 2-1. 도구 폴더로 이동

본인 PC의 도구 폴더 경로로 바꾸세요. 이미 이 폴더에 있다면 생략하세요.

```powershell
cd "C:\tools\pdf-to-images"
```

### 2-2. PDF 경로와 저장 폴더를 바꿔 실행

아래 두 경로를 본인 PC의 경로로 바꾼 뒤, 명령을 한 줄로 입력하고 Enter를 누르세요.

```powershell
.\.venv\Scripts\python.exe .\pdf_to_images.py "C:\documents\보고서.pdf" --out "C:\documents\보고서_이미지"
```

**명령에서 아래 두 곳만 바꾸세요.**

| 명령의 예시 경로 | 여기에 입력할 내용 |
| --- | --- |
| `C:\documents\보고서.pdf` | **변환할 PDF 파일**의 전체 경로 |
| `C:\documents\보고서_이미지` | **이미지를 저장할 폴더**의 경로. 폴더가 없으면 자동 생성합니다. |

**결과:** 지정한 저장 폴더에 `보고서_p1.png`, `보고서_p2.png`처럼 페이지별 이미지가 저장됩니다. 기본 해상도는 300 DPI입니다.

> **참고**
>
> - 경로에 공백이나 한글이 있어도 사용할 수 있습니다. 경로 양쪽의 큰따옴표는 **하나씩만** 유지하세요.
> - **PDF 원본은 수정하지 않습니다.**
> - 같은 저장 폴더에 같은 이름의 이미지가 있으면 덮어씁니다. 이전 결과를 보관하려면 다른 저장 폴더를 지정하세요.

## 필요한 경우에만 확인

<details>
<summary>추가 옵션: 저장 위치, 페이지, 이미지 형식, 해상도</summary>

기본 실행 명령의 PDF 경로 뒤에 필요한 옵션을 붙입니다.

| 목적 | 추가할 옵션 |
| --- | --- |
| 저장 폴더 지정 | `--out "C:\documents\변환결과"` |
| 특정 페이지만 변환 | `--pages "1,3,5-7"` |
| JPG로 저장 | `--format jpg` |
| 해상도 변경 | `--dpi 150` |

예를 들어 1~3페이지만 JPG로 변환하려면:

```powershell
.\.venv\Scripts\python.exe .\pdf_to_images.py "C:\documents\보고서.pdf" --pages "1-3" --format jpg
```

- 페이지 번호는 1부터 시작합니다. 잘못된 번호나 역순 범위는 오류로 처리합니다.
- 여러 PDF는 각 경로를 큰따옴표로 감싸 공백으로 구분합니다. `--pages`는 모든 PDF에 동일하게 적용합니다.
- 여러 PDF에 `--out`을 사용하면 같은 폴더에 저장합니다. 동명 PDF는 출력 경로를 달리하여 따로 실행하세요.
- DPI가 높을수록 처리 시간과 메모리 사용량이 커질 수 있습니다. JPG 품질은 95입니다.
- 다른 페이지나 형식으로 이전에 저장한 이미지는 자동 삭제하지 않습니다.
- 전체 도움말은 `.\.venv\Scripts\python.exe .\pdf_to_images.py --help`로 확인합니다.

</details>

<details>
<summary>실행이 안 될 때</summary>

- **`python` 명령을 찾지 못하면:** 설치 단계 1-2를 `py -m venv .venv`로 실행하세요. `py`도 없다면 Python을 먼저 설치하세요.
- **`.\.venv\Scripts\python.exe`를 찾지 못하면:** 도구 폴더로 이동했는지, 최초 설치 단계 1-2를 완료했는지 확인하세요.
- **PyMuPDF를 불러올 수 없으면:** 최초 설치 단계 1-3을 다시 실행하세요.
- **PDF 파일을 찾지 못하면:** PDF의 전체 경로와 파일명, 확장자를 확인하세요.
- **암호가 필요한 PDF라면:** 열기 암호를 해제한 사본을 사용하세요.

여러 PDF 중 하나가 실패해도 나머지는 계속 처리합니다. 오류 전에 저장된 이미지는 남을 수 있습니다. 종료 코드는 성공 `0`, 변환 실패 `1`, 명령 입력 오류 `2`이며, 실행 직후 `$LASTEXITCODE`로 확인합니다.

</details>

## 팀원에게 공유할 때

`README.md`, `pdf_to_images.py`, `requirements.txt`, `LICENSE`가 포함된 이 폴더를 전달하세요. `.venv`는 전달하지 않고, 팀원 PC에서 최초 설치를 진행합니다.

## 라이선스

이 폴더의 직접 작성한 코드와 문서는 **GNU Affero General Public License v3.0 only (AGPL-3.0-only)**로 제공합니다. 전체 조건은 함께 제공하는 [LICENSE](LICENSE)를 확인하세요.

외부 라이브러리는 해당 저작권자의 라이선스를 따릅니다. PyMuPDF 1.28.2는 AGPL 또는 Artifex 상용 라이선스로 제공됩니다. 이 도구에 적용한 라이선스가 PyMuPDF의 라이선스 조건을 대체하지 않습니다.

- [PyMuPDF 라이선스 안내](https://pymupdf.readthedocs.io/en/latest/about.html#license-and-copyright)
- [PyMuPDF 1.28.2 배포 및 소스 정보](https://pypi.org/project/pymupdf/1.28.2/)

팀원에게 폴더를 공유할 때는 README, 소스 코드, requirements.txt와 LICENSE를 함께 전달하세요.

## 공식 참고 문서

- [PyMuPDF 1.28.2](https://pypi.org/project/pymupdf/1.28.2/)
- [PyMuPDF 설치](https://pymupdf.readthedocs.io/en/latest/installation.html)
- [페이지 이미지 렌더링](https://pymupdf.readthedocs.io/en/latest/page.html#Page.get_pixmap)
