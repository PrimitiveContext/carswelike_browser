#!/usr/bin/env python3

import os
import undetected_chromedriver as uc

_already_fixed = False

def fix_undetected_chromedriver():

    #Patch undetected_chromedriver's patcher.py for Python 3.12+ only once.

    global _already_fixed
    if _already_fixed:
        return

    uc_dir = os.path.dirname(uc.__file__)
    patcher_file = os.path.join(uc_dir, "patcher.py")

    if not os.path.isfile(patcher_file):
        print(f"[fix_undetected_chromedriver] ERROR: patcher.py not found at {patcher_file}")
        _already_fixed = True
        return

    print(f"[fix_undetected_chromedriver] Located patcher.py at: {patcher_file}")

    with open(patcher_file, "r", encoding="utf-8") as f:
        original_content = f.read()

    content = original_content

    # distutils -> packaging
    content = content.replace(
        "from distutils.version import LooseVersion",
        "from packaging.version import Version as LooseVersion"
    )

    # .version -> .release
    content = content.replace(".version[", ".release[")

    # .vstring -> .public
    content = content.replace(".vstring", ".public")

    if content != original_content:
        backup_path = patcher_file + ".bak"
        print(f"[fix_undetected_chromedriver] Backing up original to {backup_path}")
        with open(backup_path, "w", encoding="utf-8") as bf:
            bf.write(original_content)

        print("[fix_undetected_chromedriver] Applying replacements...")
        with open(patcher_file, "w", encoding="utf-8") as pf:
            pf.write(content)

        print("[fix_undetected_chromedriver] Done patching.")
    else:
        print("[fix_undetected_chromedriver] No changes needed (already patched?).")

    _already_fixed = True
