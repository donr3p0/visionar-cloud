#!/usr/bin/env python3
"""Regenerates models.json from the current contents of assets/models/.

assets/models/ is the single source of truth for the VisionAR cloud catalog.
This script never reads the existing models.json — the output is derived
purely from the current directory listing, so renamed/deleted files never
linger as stale entries and the same folder contents always produce the
same output.
"""

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MODELS_DIR = REPO_ROOT / "assets" / "models"
CATALOG_PATH = REPO_ROOT / "models.json"
CATALOG_NAME = "VisionAR Cloud"


def derive_display_name(stem: str) -> str:
    """house -> House, garden_table -> Garden Table, my-model -> My Model."""
    words = [word for word in re.split(r"[_\-]+", stem) if word]
    if not words:
        return stem
    return " ".join(word.capitalize() for word in words)


def main() -> int:
    if not MODELS_DIR.is_dir():
        print(f"ERROR: models folder not found: {MODELS_DIR}", file=sys.stderr)
        return 1

    glb_files = sorted(
        (
            path
            for path in MODELS_DIR.iterdir()
            if path.is_file() and path.suffix.lower() == ".glb"
        ),
        key=lambda path: path.name,
    )

    if not glb_files:
        print(f"ERROR: no .glb files found in {MODELS_DIR}", file=sys.stderr)
        return 1

    seen_ids: dict[str, str] = {}
    models = []

    for glb_path in glb_files:
        model_id = glb_path.stem

        if model_id in seen_ids:
            print(
                f"ERROR: duplicate model id '{model_id}' produced by "
                f"'{seen_ids[model_id]}' and '{glb_path.name}'",
                file=sys.stderr,
            )
            return 1

        seen_ids[model_id] = glb_path.name

        model_path = f"assets/models/{glb_path.name}"
        if not (REPO_ROOT / model_path).is_file():
            print(
                f"ERROR: generated model path does not exist: {model_path}",
                file=sys.stderr,
            )
            return 1

        models.append(
            {
                "id": model_id,
                "name": derive_display_name(model_id),
                "model": model_path,
            }
        )

    catalog = {
        "version": 1,
        "catalogName": CATALOG_NAME,
        "models": models,
    }

    CATALOG_PATH.write_text(
        json.dumps(catalog, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print(f"Generated {CATALOG_PATH} with {len(models)} model(s):")
    for model in models:
        print(f"  - {model['id']} -> {model['model']}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
