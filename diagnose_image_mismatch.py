import json
from collections import Counter, defaultdict
from pathlib import Path

QUESTIONS_PATH = Path("questions_all.json")
SRC_ROOT = Path("figure_extraction")  # 按你的实际路径改

def load_objects(path: Path):
    text = path.read_text(encoding="utf-8")
    t = text.lstrip()
    if t.startswith("["):
        return json.loads(text)
    objs = []
    for line in text.splitlines():
        line = line.strip()
        if line:
            objs.append(json.loads(line))
    return objs

def main():
    objs = load_objects(QUESTIONS_PATH)
    total = len(objs)

    img_paths = []
    no_img = 0

    for obj in objs:
        field = obj.get("field")
        paper = obj.get("paper")
        figure_name = obj.get("figure_name")
        images = obj.get("images", [])

        if not images:
            no_img += 1
            continue

        for img in images:
            rel = Path(field) / paper / figure_name / img
            img_paths.append(rel.as_posix())

    cnt = Counter(img_paths)
    unique_imgs = len(cnt)

    # 缺失文件检查（只检查唯一即可）
    missing = []
    for rel in cnt.keys():
        src = SRC_ROOT / rel
        if not src.exists():
            missing.append(rel)

    print("====== Image Copy Diagnosis ======")
    print(f"Total questions: {total}")
    print(f"Questions with NO images[]: {no_img}")
    print(f"Total image references (including duplicates, including multi-image): {len(img_paths)}")
    print(f"Unique image files referenced: {unique_imgs}")
    print(f"Missing image files on disk: {len(missing)}")

    print("\nTop 20 most-reused images (duplicates explain why file count < questions):")
    for p, c in cnt.most_common(20):
        if c <= 1:
            break
        print(f"  {c:3d}x  {p}")

    if missing:
        out = Path("missing_images.txt")
        out.write_text("\n".join(missing), encoding="utf-8")
        print(f"\nWrote missing list to: {out.resolve()}")

if __name__ == "__main__":
    main()