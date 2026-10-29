# SPDX-FileCopyrightText: 2026 rootnode-lab
# SPDX-License-Identifier: AGPL-3.0-only

"""PDF의 각 페이지를 PNG 또는 JPG 이미지로 저장하는 명령행 도구.

설치: python -m pip install -r requirements.txt
실행: python pdf_to_images.py "report.pdf" --out "images"
상세 사용법은 같은 폴더의 README.md를 참고하세요.
"""

import argparse
import os
import re
import sys
from pathlib import Path


def parse_pages(spec, total):
    """1부터 시작하는 페이지 지정 문자열을 검증하고 중복 없는 인덱스를 반환."""
    if total < 1:
        raise ValueError("PDF에 변환할 페이지가 없습니다.")
    if spec is None:
        return list(range(total))

    pages = []
    seen = set()
    for part in spec.split(","):
        match = re.fullmatch(r"\s*([0-9]+)(?:\s*-\s*([0-9]+))?\s*", part)
        if not match:
            raise ValueError("페이지 형식이 잘못되었습니다. 예: --pages \"1,3,5-7\"")
        start = int(match.group(1))
        end = int(match.group(2)) if match.group(2) else start
        if start > end:
            raise ValueError(f"페이지 범위는 오름차순이어야 합니다: {part.strip()}")
        if start < 1 or end > total:
            raise ValueError(f"페이지는 1~{total} 범위여야 합니다: {part.strip()}")
        for page in range(start - 1, end):
            if page not in seen:
                pages.append(page)
                seen.add(page)
    return pages


def positive_int(value):
    """argparse에서 사용하는 양의 정수 검증."""
    number = int(value)
    if number < 1:
        raise argparse.ArgumentTypeError("DPI는 1 이상의 정수여야 합니다.")
    return number


def load_pymupdf():
    """미설치와 설치된 라이브러리의 DLL 로딩 실패를 구분한다."""
    try:
        import pymupdf
    except (ImportError, OSError) as exc:
        if isinstance(exc, ModuleNotFoundError) and exc.name == "pymupdf":
            raise RuntimeError(
                "PyMuPDF가 설치되지 않았습니다. 도구 폴더에서 설치: "
                ".\\.venv\\Scripts\\python.exe -m pip install -r requirements.txt"
            ) from exc

        # PyMuPDF의 대체 import가 최초 DLL 오류를 가릴 수 있다.
        causes = []
        current = exc
        seen = set()
        while current is not None and id(current) not in seen:
            seen.add(id(current))
            causes.append(f"{type(current).__name__}: {current}")
            current = current.__cause__ or (
                None if current.__suppress_context__ else current.__context__
            )
        details = "\n    ".join(reversed(causes))
        raise RuntimeError(
            "PyMuPDF가 설치되어 있지만 불러오지 못했습니다.\n"
            f"    {details}\n"
            "    Windows에서 파일 차단 메시지가 나오면 이벤트 뷰어의 "
            "Microsoft-Windows-CodeIntegrity/Operational 로그를 확인하고, "
            "보안 정책 관리자에게 해당 파일의 실행 허용을 요청하세요."
        ) from exc
    return pymupdf


def convert(pdf_path, dpi=300, fmt="png", out_dir=None, pages_spec=None):
    """PDF 한 개를 변환하고 출력 폴더 경로를 반환. 기존 출력 파일은 덮어쓴다."""
    pdf_path = Path(pdf_path).expanduser().resolve()
    if not pdf_path.is_file():
        raise FileNotFoundError(f"PDF 파일을 찾을 수 없습니다: {pdf_path}")
    if pdf_path.suffix.lower() != ".pdf":
        raise ValueError(f".pdf 파일만 입력할 수 있습니다: {pdf_path.name}")
    if dpi < 1:
        raise ValueError("DPI는 1 이상의 정수여야 합니다.")
    if fmt not in ("png", "jpg"):
        raise ValueError("이미지 형식은 png 또는 jpg여야 합니다.")

    # 도움말과 페이지 지정 검증은 PyMuPDF 설치 전에도 사용할 수 있게 한다.
    fitz = load_pymupdf()

    output = (
        Path(out_dir).expanduser().resolve()
        if out_dir
        else pdf_path.parent / f"{pdf_path.stem}_images"
    )
    with fitz.open(pdf_path) as doc:
        if not doc.is_pdf:
            raise ValueError("입력 파일의 내용이 PDF 형식이 아닙니다.")
        if doc.needs_pass:
            raise ValueError("열기 암호가 필요한 PDF입니다. 암호를 해제한 파일을 사용하세요.")
        targets = parse_pages(pages_spec, doc.page_count)
        # 입력 및 페이지 검증이 끝난 뒤에만 출력 폴더를 생성한다.
        output.mkdir(parents=True, exist_ok=True)
        width = len(str(doc.page_count))
        for idx in targets:
            pix = doc[idx].get_pixmap(dpi=dpi, colorspace=fitz.csRGB, alpha=False)
            out_file = output / f"{pdf_path.stem}_p{idx + 1:0{width}d}.{fmt}"
            if fmt == "jpg":
                pix.save(out_file, jpg_quality=95)
            else:
                pix.save(out_file)
            print(f"  저장: {out_file.name}  ({pix.width}x{pix.height})")

    print(f"완료: {len(targets)}장 -> {output}")
    return output


def main(argv=None):
    parser = argparse.ArgumentParser(description="PDF를 페이지별 PNG/JPG 이미지로 변환")
    parser.add_argument("pdfs", nargs="+", help="변환할 PDF 파일 경로 (여러 개 가능)")
    parser.add_argument("--dpi", type=positive_int, default=300, help="해상도 (기본 300)")
    parser.add_argument("--format", choices=["png", "jpg"], default="png", help="이미지 형식 (기본 png)")
    parser.add_argument("--out", help="출력 폴더 (기본: PDF 옆 <파일명>_images)")
    parser.add_argument("--pages", help='페이지 지정 (1부터 시작). 예: "1,3,5-7"')
    args = parser.parse_args(argv)

    # 같은 출력 위치를 사용하는 동명 PDF가 서로의 이미지를 덮어쓰지 않게 한다.
    jobs = []
    destinations = set()
    for pdf in args.pdfs:
        source = Path(pdf).expanduser().resolve()
        output = (
            Path(args.out).expanduser().resolve()
            if args.out
            else source.parent / f"{source.stem}_images"
        )
        key = (os.path.normcase(str(output)), os.path.normcase(source.stem))
        if key in destinations:
            parser.error(
                f"출력 파일명이 겹치는 입력입니다: {pdf}. "
                "중복 입력을 제거하거나 PDF별로 다른 --out 경로를 지정해 따로 실행하세요."
            )
        destinations.add(key)
        jobs.append(source)

    failures = 0
    for pdf in jobs:
        print(f"[{pdf}]", flush=True)
        try:
            convert(pdf, args.dpi, args.format, args.out, args.pages)
        except Exception as exc:
            failures += 1
            print(f"  오류: {exc}", file=sys.stderr)

    if failures:
        print(f"결과: {len(jobs)}개 PDF 중 {failures}개 실패", file=sys.stderr)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
