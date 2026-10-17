"""Check the GitHub organization profile without third-party dependencies."""

from pathlib import Path
import re
import sys
from urllib.parse import urlparse
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / "profile" / "README.md"
BANNER = ROOT / "profile" / "assets" / "banner.svg"
OWNER = "Careti-tn"
SECRET = re.compile(r"(?:github_pat_[A-Za-z0-9_]{20,}|gh[pousr]_[A-Za-z0-9]{20,})")
EXCLUDED = {".git", ".work", "__pycache__"}


def check():
    errors = []
    for path in (PROFILE, BANNER):
        if not path.is_file():
            errors.append(f"Missing {path.relative_to(ROOT)}")
    if errors:
        return errors

    readme = PROFILE.read_text(encoding="utf-8")
    if not re.search(r'alt="[^\"]+"', readme):
        errors.append("The banner needs descriptive alt text.")
    if f"https://raw.githubusercontent.com/{OWNER}/.github/HEAD/profile/assets/banner.svg" not in readme:
        errors.append("The banner must use its public repository URL.")
    for url in re.findall(r'https://[^\s"<>)]*', readme):
        parsed = urlparse(url)
        if parsed.netloc not in {"github.com", "raw.githubusercontent.com", "careti.tn"}:
            errors.append(f"Review external destination: {parsed.netloc}")
        if parsed.netloc in {"github.com", "raw.githubusercontent.com"} and OWNER.lower() not in parsed.path.lower():
            errors.append(f"Profile link points outside {OWNER}: {url}")
    for path in ROOT.rglob("*"):
        if not path.is_file() or any(part in EXCLUDED for part in path.relative_to(ROOT).parts):
            continue
        if path.name.startswith(".env"):
            errors.append(f"Remove the environment file: {path.relative_to(ROOT)}")
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if SECRET.search(content):
            errors.append(f"Potential credential in {path.relative_to(ROOT)}")

    try:
        svg = ET.parse(BANNER).getroot()
        if svg.tag != "{http://www.w3.org/2000/svg}svg":
            errors.append("The banner must be an SVG document.")
        if svg.get("viewBox") != "0 0 1280 360":
            errors.append("The banner viewBox must match its intended dimensions.")
        for element in svg.iter():
            tag = element.tag.rsplit("}", 1)[-1]
            if tag in {"script", "foreignObject", "image", "animate", "set"}:
                errors.append(f"Unsupported or external SVG element: {tag}")
            for attribute in element.attrib:
                if attribute.lower().startswith("on"):
                    errors.append("The banner must not contain event handlers.")
    except ET.ParseError as error:
        errors.append(f"Invalid SVG: {error}")
    return errors


if __name__ == "__main__":
    failures = check()
    for failure in failures:
        print(f"FAIL: {failure}")
    if failures:
        sys.exit(1)
    print("PASS: profile assets, destination links, SVG safety, and credential scan.")
