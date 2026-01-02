import json
import shutil
from pathlib import Path

QUESTIONS_PATH = Path("questions_table.json")  # 改成你的实际路径
SRC_ROOT = Path("table_extraction")         # 改成你的实际路径（包含 figure_extraction 目录）
DST_ROOT = Path("mturk_assets_site")         # 要上传到 GitHub Pages 的目录

def load_objects(path: Path):
    # 兼容：JSON array 或 JSONL
    text = path.read_text(encoding="utf-8")
    text_strip = text.lstrip()
    if text_strip.startswith("["):
        return json.loads(text)
    else:
        objs = []
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            objs.append(json.loads(line))
        return objs

def main():
    objs = load_objects(QUESTIONS_PATH)

    missing = []
    copied = 0

    for obj in objs:
        field = obj["field"]
        paper = obj["paper"]
        table_name = obj["table_name"]
        images = obj.get("images", [])

        for img in images:
            src = SRC_ROOT / field / paper / table_name / img
            dst = DST_ROOT / "figure_extraction" / field / paper / table_name / img
            dst.parent.mkdir(parents=True, exist_ok=True)

            if not src.exists():
                missing.append(str(src))
                continue

            shutil.copy2(src, dst)
            copied += 1

    print(f"Copied {copied} image files into: {DST_ROOT.resolve()}")
    if missing:
        print("\n[WARNING] Missing files (will 404 if not fixed):")
        for p in missing[:50]:
            print(" -", p)
        if len(missing) > 50:
            print(f" ... and {len(missing)-50} more")

if __name__ == "__main__":
    main()